from datetime import date
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Teacher
from users.models import User
from .serializers import TeacherSerializer, TeacherProfileSerializer
from users.serializers import UserListSerializer
from rest_framework.views import APIView
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from django.shortcuts import get_object_or_404
from subjects.models import ClassroomSubject
from subjects.serializers import ClassroomSubjectSerializer
from students.models import Student
from students.serializers import StudentSerializer
from school_erp_backend.permissions import IsSchoolAdmin, IsTeacher
from classrooms.models import Classroom
from attendances.models import StudentAttendance
from attendances.serializers import StudentAttendanceSerializer
from exams.serializers import ExamSerializer
from exams.models import Exam, ExamSubject, ExamResult
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TeacherListCreateView(generics.ListCreateAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated, IsSchoolAdmin]

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
    permission_classes = [permissions.IsAuthenticated, IsSchoolAdmin]

    def get_queryset(self):
        return Teacher.objects.filter(user__school=self.request.user.school)

    def get_serializer_context(self):
        return {'request': self.request}


class TeacherProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get(self, request):
        teacher = get_object_or_404(Teacher, user=request.user)
        serializer = TeacherProfileSerializer(teacher)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=TeacherProfileSerializer,
        responses={200: TeacherProfileSerializer}
    )
    def patch(self, request):
        teacher = get_object_or_404(Teacher, user=request.user)
        serializer = TeacherProfileSerializer(
            teacher, data=request.data, partial=True)
        if serializer.is_valid():
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


class TeacherClassroomSubjectAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get(self, request):
        teacher = get_object_or_404(Teacher, user=request.user)
        assignments = ClassroomSubject.objects.filter(
            teacher=teacher).select_related('classroom', 'subject')
        serializer = ClassroomSubjectSerializer(assignments, many=True)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )


class StudentInClassSubjectAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get(self, request):
        teacher = get_object_or_404(Teacher, user=request.user)
        classroom_ids = ClassroomSubject.objects.filter(
            teacher=teacher).values_list('classroom_id', flat=True).distinct()
        students = Student.objects.filter(
            classroom_id__in=classroom_ids).select_related('classroom')
        serializer = StudentSerializer(students, many=True)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )


class MarkAttendanceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get(self, request, classroom_id):
        classroom = get_object_or_404(Classroom, id=classroom_id)
        teacher = get_object_or_404(Teacher, user=request.user)

        if classroom.class_teacher != teacher:
            return Response({'error': 'You are not the class teacher of this classroom.'}, status=status.HTTP_403_FORBIDDEN)

        records = StudentAttendance.objects.filter(
            classroom=classroom).select_related('student')
        serializer = StudentAttendanceSerializer(records, many=True)
        return send_response(
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    attendance_schema = openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(
            type=openapi.TYPE_OBJECT,
            properties={
                'student_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['P', 'A']),
            },
            required=['student_id', 'status']
        )
    )

    @swagger_auto_schema(
        request_body=attendance_schema,
        responses={200: 'Attendance marked successfully.'}
    )
    def post(self, request, classroom_id):
        teacher = get_object_or_404(Teacher, user=request.user)

        try:
            classroom = Classroom.objects.get(
                id=classroom_id, class_teacher=teacher)
        except Classroom.DoesNotExist:
            return send_response(
                message="Not your assigned classroom.",
                status_code=status.HTTP_403_FORBIDDEN
            )

        for entry in request.data:
            student_id = entry.get('student_id')
            status_val = entry.get('status')
            try:
                student = Student.objects.get(
                    id=student_id, classroom=classroom)
            except Student.DoesNotExist:
                continue

            StudentAttendance.objects.update_or_create(
                student=student,
                date=date.today(),
                defaults={"status": status_val, "classroom": classroom}
            )

        return send_response(
            message="Attendance marked successfully.",
            status_code=status.HTTP_202_ACCEPTED
        )


class TeacherUpdateMarksAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    marks_schema = openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(
            type=openapi.TYPE_OBJECT,
            properties={
                'student_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'marks_obtained': openapi.Schema(type=openapi.TYPE_NUMBER),
            },
            required=['student_id', 'marks_obtained']
        )
    )

    @swagger_auto_schema(
        request_body=marks_schema,
        responses={200: 'Marks updated successfully.'}
    )
    def post(self, request, exam_subject_id):
        teacher = get_object_or_404(Teacher, user=request.user)

        try:
            exam_subject = get_object_or_404(
                ExamSubject.objects.select_related('classroom__class_teacher'),
                id=exam_subject_id,
                classroom__class_teacher=teacher
            )
        except ExamSubject.DoesNotExist:
            return send_response(
                message="You are not assigned to this subject.",
                status_code=status.HTTP_403_FORBIDDEN
            )

        for record in request.data:
            student_id = record.get("student_id")
            marks = record.get("marks_obtained")

            ExamResult.objects.update_or_create(
                exam_subject=exam_subject,
                student_id=student_id,
                defaults={"marks_obtained": marks}
            )

        return send_response(
            message="Marks updated successfully.",
            status_code=status.HTTP_201_CREATED
        )


class TeacherClassResultSummaryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get(self, request, classroom_id):
        teacher = get_object_or_404(Teacher, user=request.user)

        if not Classroom.objects.filter(id=classroom_id, class_teacher=teacher).exists():
            return send_response(
                message="You are not the class teacher.", 
                status_code=status.HTTP_403_FORBIDDEN
            )

        students = Student.objects.filter(classroom_id=classroom_id)
        data = []

        for student in students:
            results = ExamResult.objects.filter(
                student=student).select_related('exam_subject__subject')
            total_marks = sum(r.marks_obtained for r in results)

            student_data = {
                "student_id": student.id,
                "student_name": student.user.name,
                "total_marks": total_marks,
                "subjects": [
                    {
                        "subject": r.exam_subject.subject.name,
                        "marks": r.marks_obtained
                    }
                    for r in results
                ]
            }
            data.append(student_data)

        return send_response(
            data=data,
            status_code=status.HTTP_200_OK
        )
