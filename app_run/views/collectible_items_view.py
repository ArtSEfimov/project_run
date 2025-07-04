import openpyxl
from rest_framework import status
from rest_framework.response import Response

from .validate_url import validate_url
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from ..models import CollectibleItem
from ..serializers import CollectibleItemSerializer, FileUploadSerializer


class CollectibleItemView(ListAPIView):
    queryset = CollectibleItem.objects.all()
    serializer_class = CollectibleItemSerializer


# class UploadFileView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#
#     def post(self, request, *args, **kwargs):
#         # input_serializer = FileUploadSerializer(data=request.data)
#         # input_serializer.is_valid(raise_exception=True)
#         # file_object = input_serializer.validated_data["file"]
#
#         file_object = request.FILES.get("file")
#
#         # workbook = load_workbook(file_object)
#         # worksheet = workbook.active
#         #
#         # header_row = next(worksheet.iter_rows(min_row=1, max_row=1, values_only=True))
#         # headers = list(h.lower() for h in header_row)
#         #
#         # wrong_rows = list()
#         #
#         # for row in worksheet.iter_rows(min_row=2, values_only=True):
#         #     row_serializer = CollectibleItemSerializer(data=dict(zip(headers, row)))
#         #     if row_serializer.is_valid(raise_exception=False):
#         #         row_serializer.save()
#         #     else:
#         #         print(row_serializer.errors)
#         #         wrong_rows.append(list(row))
#         #
#         # return Response(wrong_rows, status=status.HTTP_200_OK)
#
#         # TRY IT
#
#         # Open the workbook
#         workbook = openpyxl.load_workbook(file_object)
#
#         # Select the active worksheet
#         worksheet = workbook.active
#
#         # Read the contents
#         data = []
#         to_create = []
#         for i, row in enumerate(worksheet.iter_rows(values_only=True)):
#             if i == 0:
#                 continue
#             valid = True
#             types = [str, str, int, float, float, str]
#             for index, sub_row in enumerate(row):
#                 if type(sub_row) != types[index]:
#                     valid = False
#
#             if not type(row[3]) == float or not (-90 <= row[3] <= 90):
#                 valid = False
#
#             if not type(row[4]) == float or not (-180 <= row[4] <= 180):
#                 valid = False
#
#             if not validate_url(row[5]):
#                 valid = False
#
#             if not valid:
#                 data.append(row)
#             else:
#                 to_create.append(row)
#
#         for item in to_create:
#             CollectibleItem.objects.create(name=item[0],
#                                            uid=item[1],
#                                            value=item[2],
#                                            latitude=item[3],
#                                            longitude=item[4],
#                                            picture=item[5],
#                                            )
#
#         return JsonResponse(data, safe=False)
class UploadFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # Open the workbook
        workbook = openpyxl.load_workbook(file_obj)

        # Select the active worksheet
        worksheet = workbook.active

        # Read the contents
        data = []
        to_create = []
        for i, row in enumerate(worksheet.iter_rows(values_only=True)):
            if i == 0:
                continue
            valid = True
            types = [str, str, int, float, float, str]
            for index, sub_row in enumerate(row):
                if type(sub_row) != types[index]:
                    valid = False

            if not type(row[3]) == float or not (-90 <= row[3] <= 90):
                valid = False

            if not type(row[4]) == float or not (-180 <= row[4] <= 180):
                valid = False

            if not validate_url(row[5]):
                valid = False

            if not valid:
                data.append(row)
            else:
                to_create.append(row)

        for item in to_create:
            CollectibleItem.objects.create(name=item[0],
                                           uid=item[1],
                                           value=item[2],
                                           latitude=item[3],
                                           longitude=item[4],
                                           picture=item[5],
                                           )

        # Return the parsed data as JSON
        return JsonResponse(data, safe=False)
