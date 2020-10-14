#Rest
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

#Serialzier
from refuerzamas.clases.api.serializers import InstitucionModelSerializer

#Model
from refuerzamas.clases.models import Institucion


class InstitucionViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = InstitucionModelSerializer
	queryset = Institucion.objects.all()
	permission_classes = [AllowAny]
