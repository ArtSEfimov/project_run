import openpyxl
from django.http import JsonResponse
from openpyxl.reader.excel import load_workbook
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .validation_url import validate_url
from ..models import CollectibleItem
from ..serializers import CollectibleItemSerializer, FileUploadSerializer, CollectibleItemShowSerializer


class CollectibleItemView(ListAPIView):
    queryset = CollectibleItem.objects.all()
    serializer_class = CollectibleItemShowSerializer
#
#
# class UploadFileView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#
#     def post(self, request, *args, **kwargs):
#         input_serializer = FileUploadSerializer(data=request.data)
#         input_serializer.is_valid(raise_exception=True)
#         file_object = input_serializer.validated_data["file"]
#
#         workbook = load_workbook(file_object)
#         worksheet = workbook.active
#
#         # header_row = next(worksheet.iter_rows(min_row=1, max_row=1, values_only=True))
#         # headers = list(h.lower() for h in header_row if h is not None)
#         headers = ["name", "uid", "value", "latitude", "longitude", "url"]
#
#         wrong_rows = list()
#
#         for row in worksheet.iter_rows(min_row=2, values_only=True):
#             row_serializer = CollectibleItemSerializer(data=dict(zip(headers, row)))
#             if row_serializer.is_valid(raise_exception=False):
#                 row_serializer.save()
#             else:
#                 wrong_rows.append(list(row))
#
#         return Response(wrong_rows, status=status.HTTP_200_OK)



class UploadFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        file_object = request.FILES.get('file')


        if not file_object:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # Open the workbook
        workbook = openpyxl.load_workbook(file_object)

        # Select the active worksheet
        worksheet = workbook.active

        # Read the contents
        data = []
        to_create = []
        for i, row in enumerate(worksheet.iter_rows(values_only=True)):
            if i == 0:
                continue
            valid = True
            row = list(row)[:6]
            try:
                row[3] = float(row[3])
                row[4] = float(row[4])
            except Exception:
                valid = False
            types = [str, str, int, float, float, str]
            for index in range(len(types)):
                sub_row = row[index]
                print(sub_row)
                if type(sub_row) != types[index]:
                    valid = False

            if not type(row[3]) == float or not (-90 <= row[3] <= 90):
                valid = False

            if not type(row[4]) == float or not (-180 <= row[4] <= 180):
                valid = False

            if not validate_url(row[5]):
                valid = False

            print(row)
            if not valid:
                data.append(row)
            else:
                to_create.append(row)

        for item in to_create:
            if item[5] is None:
                continue
            CollectibleItem.objects.create(name=item[0],
                                           uid=item[1],
                                           value=item[2],
                                           latitude=item[3],
                                           longitude=item[4],
                                           picture=item[5],
                                           )

        # Return the parsed data as JSON
        return JsonResponse(data, safe=False)
