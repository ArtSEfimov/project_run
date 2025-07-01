from rest_framework.viewsets import ModelViewSet

from ..models import Position
from ..serializers import PositionSerializer


class PositionView(ModelViewSet):
    queryset = Position.objects.select_related("run").all()
    serializer_class = PositionSerializer
