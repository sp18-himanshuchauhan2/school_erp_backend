from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, permissions
from .models import StudentAttendance, TeacherAttendance
from .serializers import StudentAttendanceSerializer, TeacherAttendanceSerializer
from students.models import Student
from teachers.models import Teacher
from classrooms.models import Classroom
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from school_erp_backend.permissions import IsSchoolAdmin

# Create your views here.


class StudentAttendanceListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSchoolAdmin]

    def get(self, request):
        user = request.user
        if user.is_superuser:
            attendance = StudentAttendance.objects.all()
        else:
            attendance = StudentAttendance.objects.filter(
                student__user__school=user.school)

        serializer = StudentAttendanceSerializer(attendance, many=True)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = StudentAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.validated_data['student']
            classroom = serializer.validated_data['classroom']

            if not request.user.is_superuser and (
                student.user.school != request.user.school or
                classroom.school != request.user.school
            ):
                return send_response(
                    message='You are not authorized to add attendance for this student/classroom.',
                    status_code=status.HTTP_403_FORBIDDEN
                )

            serializer.save()
            return send_response(
                data=serializer.data,
                message=ResponseMessages.RECORD_CREATED,
                status_code=status.HTTP_201_CREATED
            )

        return send_response(
            data=serializer.errors,
            message=ResponseMessages.RECORD_CREATE_FAILED,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class StudentAttendanceRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSchoolAdmin]

    def get_object(self, pk, user):
        try:
            attendance = StudentAttendance.objects.get(pk=pk)
            if user.is_superuser or attendance.student.user.school == user.school:
                return attendance
            return None
        except StudentAttendance.DoesNotExist:
            return None

    def get(self, request, pk):
        attendance = self.get_object(pk, request.user)
        if attendance is None:
            return send_response(
                message="Attendance not found or unauthorized.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentAttendanceSerializer(attendance)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    def put(self, request, pk):
        attendance = self.get_object(pk, request.user)
        if attendance is None:
            return send_response(
                message="Attendance not found or unauthorized.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentAttendanceSerializer(attendance, data=request.data)
        if serializer.is_valid():
            student = serializer.validated_data['student']
            classroom = serializer.validated_data['classroom']

            if not request.user.is_superuser and (
                student.user.school != request.user.school or classroom.school != request.user.school
            ):
                return send_response(
                    message="Unauthorized update.",
                    status_code=status.HTTP_403_FORBIDDEN
                )

            serializer.save()
            return send_response(
                data=serializer.data,
                message=ResponseMessages.DATA_UPDATE_SUCCESS,
                status_code=status.HTTP_200_OK
            )

        return send_response(
            data=serializer.errors,
            message=ResponseMessages.DATA_UPDATE_FAILED,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        attendance = self.get_object(pk, request.user)
        if attendance is None:
            return send_response(
                message="Attendance not found or unauthorized.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        attendance.delete()
        return send_response(
            message=ResponseMessages.RECORD_DELETED,
            status_code=status.HTTP_204_NO_CONTENT
        )


class TeacherAttendanceListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSchoolAdmin]

    def get(self, request):
        user = request.user
        if user.is_superuser:
            attendance = TeacherAttendance.objects.all()
        else:
            attendance = TeacherAttendance.objects.filter(
                teacher__user__school=user.school)

        serializer = TeacherAttendanceSerializer(attendance, many=True)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = TeacherAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            teacher = serializer.validated_data['teacher']

            if not request.user.is_superuser and teacher.user.school != request.user.school:
                return send_response(
                    message='You are not authorized to add attendance for this teacher.',
                    status_code=status.HTTP_403_FORBIDDEN
                )

            serializer.save()
            return send_response(
                data=serializer.data,
                message=ResponseMessages.RECORD_CREATED,
                status_code=status.HTTP_201_CREATED
            )

        return send_response(
            data=serializer.errors,
            message=ResponseMessages.RECORD_CREATE_FAILED,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class TeacherAttendanceRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSchoolAdmin]

    def get_object(self, pk, user):
        try:
            attendance = TeacherAttendance.objects.get(pk=pk)
            if user.is_superuser or attendance.teacher.user.school == user.school:
                return attendance
            return None
        except TeacherAttendance.DoesNotExist:
            return None

    def get(self, request, pk):
        attendance = self.get_object(pk, request.user)
        if attendance is None:
            return send_response(
                message="Attendance not found or unauthorized.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = TeacherAttendanceSerializer(attendance)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    def put(self, request, pk):
        attendance = self.get_object(pk, request.user)
        if attendance is None:
            return send_response(
                message="Attendance not found or unauthorized.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = TeacherAttendanceSerializer(attendance, data=request.data)
        if serializer.is_valid():
            teacher = serializer.validated_data['teacher']

            if not request.user.is_superuser and teacher.user.school != request.user.school:
                return send_response(
                    message="Unauthorized update.",
                    status_code=status.HTTP_403_FORBIDDEN
                )

            serializer.save()
            return send_response(
                data=serializer.data,
                message=ResponseMessages.DATA_UPDATE_SUCCESS,
                status_code=status.HTTP_200_OK
            )

        return send_response(
            data=serializer.errors,
            message=ResponseMessages.DATA_UPDATE_FAILED,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        attendance = self.get_object(pk, request.user)
        if attendance is None:
            return send_response(
                message="Attendance not found or unauthorized.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        attendance.delete()
        return send_response(
            message=ResponseMessages.RECORD_DELETED,
            status_code=status.HTTP_204_NO_CONTENT
        )
