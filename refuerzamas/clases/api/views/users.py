#Rest
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

#Serialzier
from refuerzamas.clases.serializers import UserModelSerializer

#Model
from refuerzamas.clases.models import User

class UserView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    lookup_field = "username"
    def get_queryset(self):
        queryset = User.objects.all()
        return queryset