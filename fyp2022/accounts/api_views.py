from rest_framework import viewsets
from django.contrib.auth.models import User
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated, BasePermission

class IsSuperAdminOrNotAnUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or (not request.user.is_authenticated and
            request.method == 'POST'):
            return True
        return False

class CustomersCanView(BasePermission):
    def has_permission(self, request, view):
        if (request.method == "GET" and request.user.profile.type == 'customer') or \
            request.user.is_superuser:
            return True
        return False

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated, CustomersCanView]

    def get_queryset(self):
        if self.request.user.profile.type == 'customer':
            return self.queryset.filter(user=self.request.user)
        return self.queryset

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsSuperAdminOrNotAnUser]


