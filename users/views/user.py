from rest_framework import generics, permissions
from users.models import User
from ..serializers.user import UserCreateSerializer, UserListSerializer
from school_erp_backend.permissions import IsSchoolAdmin


class ListCreateUsersView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSchoolAdmin]

    def get_queryset(self):
        return User.objects.filter(school=self.request.user.school)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserListSerializer
