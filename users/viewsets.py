from django.contrib.auth.models import User
from .models import Profile

from rest_framework import viewsets, mixins

from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsUserOwnerOrGetPostOnly, IsProfileOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserOwnerOrGetPostOnly,]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    permission_classes = [IsProfileOwnerOrReadOnly,]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
