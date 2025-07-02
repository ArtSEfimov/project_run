from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser

from ..models import CollectibleItem
from ..serializers import CollectibleItemSerializer


class CollectibleItemView(ListAPIView):
    queryset = CollectibleItem
    serializer_class = CollectibleItemSerializer


class UploadFileView(GenericAPIView):
    serializer_class = ""
    parser_classes = (MultiPartParser, FormParser)

    def post(self):
        pass
