#Rest
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404

#Serialzier
from refuerzamas.clases.serializers import NivelesModelSerializer, GradoModelSerializer

#Model
from refuerzamas.clases.models import Nivel, Grado

class NivelesView(viewsets.ReadOnlyModelViewSet):
	serializer_class = NivelesModelSerializer
	queryset = Nivel.objects.all()
	permission_classes = [AllowAny]


class NivelesGradoView(viewsets.ReadOnlyModelViewSet):

	serializer_class = GradoModelSerializer
	queryset = Grado.objects.all()
	permission_classes = [AllowAny]

	def dispatch(self, request, *args, **kwargs):
		id = kwargs['id']
		self.nivel = get_object_or_404(Nivel, id = id)
		return super(NivelesGradoView, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		return self.queryset.filter(nivel=self.nivel)