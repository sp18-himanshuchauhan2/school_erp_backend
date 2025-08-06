from rest_framework import generics, permissions
from users.models import User
from ..serializers.user import UserCreateSerializer, UserListSerializer
from school_erp_backend.permissions import IsSchoolAdmin
from users.tasks import send_welcome_email_task


class ListCreateUsersView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSchoolAdmin]

    def get_queryset(self):
        return User.objects.filter(school=self.request.user.school)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserListSerializer

    def perform_create(self, serializer):
        user = serializer.save(school=self.request.user.school)
        raw_password = serializer.validated_data.get('password')
        role = serializer.validated_data.get('role')

        send_welcome_email_task.delay(
            email=user.email,
            name=user.name,
            password=raw_password,
            role=role,
            school_name = self.request.user.school.name
        )
