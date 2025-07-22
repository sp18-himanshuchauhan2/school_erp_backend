from rest_framework import generics, permissions
from users.models import User
from ..serializers.user import UserCreateSerializer, UserListSerializer

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class ListUsersView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(school=self.request.user.school)