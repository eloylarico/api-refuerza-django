#Rest
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

#Serialzier
from refuerzamas.clases.api.serializers import GenerosSerializer

#Model
from refuerzamas.clases.models import Genero

class GenerosView(viewsets.ReadOnlyModelViewSet):
	serializer_class = GenerosSerializer
	queryset = Genero.objects.all()
	permission_classes = [AllowAny]