from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from users.models import User
from users.serializers import UserListSerializer
from .serializers import StudentSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class StudentListCreateAPIView(APIView):
    def get(self, request):
        school = request.user.school
        students = Student.objects.filter(user__school=school)
        student_users_ids = students.values_list('user_id', flat=True)

        users = User.objects.filter(
            role='STUDENT', school=school
        ).exclude(id__in=student_users_ids)

        student_data = StudentSerializer(students, many=True).data
        user_data = UserListSerializer(users, many=True).data

        return Response({
            "enrolled_students": student_data,
            "unenrolled_students": user_data
        })

    @swagger_auto_schema(request_body=StudentSerializer, responses={201: StudentSerializer()})
    def post(self, request):
        serializer = StudentSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentRetrieveUpdateDeleteAPIView(APIView):
    def get_object(self, pk, user):
        if user.role == 'SCHOOL_ADMIN':
            return get_object_or_404(Student, pk=pk, user__school=user.school)
        return get_object_or_404(Student, pk=pk)

    def get(self, request, pk):
        student = self.get_object(pk, request.user)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=StudentSerializer, responses={200: StudentSerializer()})
    def put(self, request, pk):
        student = self.get_object(pk, request.user)
        serializer = StudentSerializer(
            student, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=StudentSerializer, responses={200: StudentSerializer()})
    def patch(self, request, pk):
        student = self.get_object(pk, request.user)
        serializer = StudentSerializer(
            student, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = self.get_obj(pk, request.user)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
