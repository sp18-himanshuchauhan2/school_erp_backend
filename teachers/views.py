from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Teacher
from users.models import User
from .serializers import TeacherSerializer
from users.serializers import UserListSerializer


class TeacherListCreateView(generics.ListCreateAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Teacher.objects.filter(user__school=self.request.user.school)

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        school = request.user.school
        teachers = self.get_queryset()
        teachers_data = TeacherSerializer(
            teachers, 
            many=True, 
            context={'request': request}
        ).data

        teachers_users_id = teachers.values_list('user_id', flat=True)
        user_without_profile = User.objects.filter(
            role='TEACHER', 
            school=school
        ).exclude(id__in=teachers_users_id)

        user_data = UserListSerializer(
            user_without_profile, 
            many=True, 
            context={'request': request}
        ).data
        return Response(
            {
                "teachers": teachers_data,
                "users_with_teacher_role": user_data
            }, 
            status=status.HTTP_200_OK
        )


class TeacherRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Teacher.objects.filter(user__school=self.request.user.school)

    def get_serializer_context(self):
        return {'request': self.request}
