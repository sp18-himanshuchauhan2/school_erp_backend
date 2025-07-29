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
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from rest_framework.pagination import PageNumberPagination

# Create your views here.


class StudentListCreateAPIView(APIView):
    def get(self, request):
        school = request.user.school
        students = Student.objects.filter(user__school=school)
        student_users_ids = students.values_list('user_id', flat=True)

        users = User.objects.filter(
            role='STUDENT', school=school
        ).exclude(id__in=student_users_ids)

        # pagination
        student_paginator = PageNumberPagination()
        user_paginator = PageNumberPagination()
        # paginator.page_size = 5

        student_results = student_paginator.paginate_queryset(students, request)
        user_results = user_paginator.paginate_queryset(users, request)

        student_data = StudentSerializer(student_results, many=True).data
        user_data = UserListSerializer(user_results, many=True).data

        data = {
            "enrolled_students": student_data,
            "unenrolled_students": user_data,
            "pagination": {
                "enrolled": {
                    "count": student_paginator.page.paginator.count,
                    "next": student_paginator.get_next_link(),
                    "previous": student_paginator.get_previous_link(),
                },
                "unenrolled": {
                    "count": user_paginator.page.paginator.count,
                    "next": user_paginator.get_next_link(),
                    "previous": user_paginator.get_previous_link(),
                }
            }
        }

        return send_response(
            data=data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(request_body=StudentSerializer, responses={201: StudentSerializer()})
    def post(self, request):
        serializer = StudentSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return send_response(
                data=data,
                status_code=status.HTTP_201_CREATED,
                message=ResponseMessages.RECORD_CREATED
            )

        errors = serializer.errors
        return send_response(
            data=errors,
            message=ResponseMessages.RECORD_CREATE_FAILED,
            status_code=status.HTTP_400_BAD_REQUEST
        )


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
        student = self.get_object(pk, request.user)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
