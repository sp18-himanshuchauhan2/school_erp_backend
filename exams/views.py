from django.forms import ValidationError
from django.shortcuts import render
from rest_framework.views import APIView
from utils.restful_response import send_response
from rest_framework import status
from .models import Exam, ExamResult, ExamSubject
from .serializers import ExamSerializer, ExamSubjectSerializer, ExamResultSerializer
from drf_yasg.utils import swagger_auto_schema
from utils.data_constants import ResponseMessages
from rest_framework.exceptions import NotFound
from classrooms.models import Classroom
from rest_framework.permissions import IsAuthenticated
from school_erp_backend.permissions import IsSchoolAdmin
# Create your views here.


class ExamListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get(self, request):
        school = request.user.school
        title = request.query_params.get('title')

        exams = Exam.objects.filter(classrooms__school=school).distinct()
        if title:
            exams = exams.filter(title__icontains=title).distinct()

        serializer = ExamSerializer(exams, many=True)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(request_body=ExamSerializer, responses={201: ExamSerializer()})
    def post(self, request):
        school = request.user.school
        classroom_ids = request.data.get("classrooms", [])

        if not Classroom.objects.filter(id__in=classroom_ids, school=school).count() == len(classroom_ids):
            return send_response(
                error_code="Invalid classrooms for your school.",
                message=ResponseMessages.RECORD_CREATE_FAILED,
                status_code=status.HTTP_403_FORBIDDEN
            )

        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
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


class ExamRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get_object(self, pk, school):
        try:
            return Exam.objects.filter(pk=pk, classrooms__school=school).distinct().get()
        except Exam.DoesNotExist:
            raise NotFound("Exam not found.")
        except Exam.MultipleObjectsReturned:
            raise ValidationError(
                "Multiple exam entries found. Data integrity issue.")

    def get(self, request, pk):
        school = request.user.school
        exam = self.get_object(pk, school)
        serializer = ExamSerializer(exam)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    def put(self, request, pk):
        exam = self.get_object(pk, request.user.school)
        classroom_ids = request.data.get("classrooms", [])

        if classroom_ids:
            valid_classrooms = Classroom.objects.filter(
                id__in=classroom_ids, school=request.user.school)
            if valid_classrooms.count() != len(classroom_ids):
                return send_response(
                    error_code="Invalid classrooms for your school.",
                    message=ResponseMessages.DATA_UPDATE_FAILED,
                    status_code=status.HTTP_403_FORBIDDEN
                )

        serializer = ExamSerializer(exam, data=request.data)
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

    def delete(self, request, pk):
        exam = self.get_object(pk, request.user.school)
        exam.delete()
        return send_response(
            message=ResponseMessages.DATA_DELETED_SUCCESS,
            status_code=status.HTTP_204_NO_CONTENT
        )


class ExamSubjectListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get(self, request):
        school = request.user.school
        exam_id = request.query_params.get('exam_id')
        classroom_id = request.query_params.get('classroom_id')

        filters = {
            'exam__classrooms__school': school,
        }

        if exam_id:
            filters['exam_id'] = exam_id

        if classroom_id:
            filters['classroom_id'] = classroom_id
            filters['exam__classrooms__id'] = classroom_id

        exam_subjects = ExamSubject.objects.filter(**filters).distinct()

        serializer = ExamSubjectSerializer(exam_subjects, many=True)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=ExamSubjectSerializer,
        responses={201: ExamSubjectSerializer()}
    )
    def post(self, request):
        exam_id = request.data.get("exam")
        classroom_id = request.data.get("classroom")

        try:
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            return send_response(
                error_code="Invalid exam ID.",
                message=ResponseMessages.RECORD_CREATE_FAILED,
                status_code=status.HTTP_404_NOT_FOUND
            )

        try:
            classroom = Classroom.objects.get(id=classroom_id)
        except Classroom.DoesNotExist:
            return send_response(
                error_code="Invalid classroom ID.",
                message=ResponseMessages.RECORD_CREATE_FAILED,
                status_code=status.HTTP_404_NOT_FOUND
            )

        if classroom not in exam.classrooms.all():
            return send_response(
                error_code="Classroom not associated with the exam.",
                message=ResponseMessages.RECORD_CREATE_FAILED,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer = ExamSubjectSerializer(data=request.data)
        if serializer.is_valid():
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


class ExamSubjectRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get_object(self, pk, school):
        try:
            exam_subject = ExamSubject.objects.get(pk=pk)
            if not exam_subject.exam.classrooms.filter(school=school).exists():
                raise ValidationError(
                    "You do not have permission to access this exam subject.")
            return exam_subject
        except ExamSubject.DoesNotExist:
            raise NotFound("Exam Subject not found.")

    def get(self, request, pk):
        exam_subject = self.get_object(pk, request.user.school)
        serializer = ExamSubjectSerializer(exam_subject)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    def put(self, request, pk):
        exam_subject = self.get_object(pk, request.user.school)
        exam_id = request.data.get("exam")

        if exam_id:
            try:
                exam = Exam.objects.get(id=exam_id)
                if not exam.classrooms.filter(school=request.user.school).exists():
                    return send_response(
                        error_code="Invalid exam for your school.",
                        message=ResponseMessages.RECORD_CREATE_FAILED,
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Exam.DoesNotExist:
                return send_response(
                    error_code="Exam not found.",
                    message=ResponseMessages.RECORD_CREATE_FAILED,
                    status_code=status.HTTP_404_NOT_FOUND
                )

        serializer = ExamSubjectSerializer(exam_subject, data=request.data)
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

    def delete(self, request, pk):
        exam_subject = self.get_object(pk, request.user.school)
        exam_subject.delete()
        return send_response(
            message=ResponseMessages.DATA_DELETED_SUCCESS,
            status_code=status.HTTP_204_NO_CONTENT
        )


class ExamResultListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get(self, request):
        school = request.user.school
        exam_results = ExamResult.objects.filter(
            exam_subject__exam__classrooms__school=school).distinct()
        serializer = ExamResultSerializer(exam_results, many=True)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=ExamResultSerializer,
        responses={201: ExamResultSerializer()}
    )
    def post(self, request):
        school = request.user.school
        exam_subject_id = request.data.get("exam_subject")

        try:
            exam_subject = ExamSubject.objects.get(id=exam_subject_id)
            if exam_subject.classroom.school != school:
                return send_response(
                    error_code="You cannot add results for another school's exam subject.",
                    message=ResponseMessages.RECORD_CREATE_FAILED,
                    status_code=status.HTTP_403_FORBIDDEN
                )
        except ExamSubject.DoesNotExist:
            return send_response(
                error_code="Exam subject not found.",
                message=ResponseMessages.RECORD_CREATE_FAILED,
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = ExamResultSerializer(data=request.data)
        if serializer.is_valid():
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


class ExamResultRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get_object(self, pk, school):
        result = ExamResult.objects.filter(
            id=pk,
            exam_subject__exam__classrooms__school=school
        ).first()

        if not result:
            raise NotFound(detail="Exam Result not found.")

        return result

    def get(self, request, pk):
        school = request.user.school
        result = self.get_object(pk, school)
        if not result:
            raise NotFound("Exam Result not found.")
        serializer = ExamResultSerializer(result)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    def put(self, request, pk):
        result = self.get_object(pk, request.user.school)
        exam_subject_id = request.data.get("exam_subject")
        student_id = request.data.get("student")

        if exam_subject_id:
            try:
                exam_subject = ExamSubject.objects.get(id=exam_subject_id)
                if not exam_subject.exam.classrooms.filter(school=request.user.school).exists():
                    return send_response(
                        error_code="Invalid exam subject for your school.",
                        message=ResponseMessages.RECORD_CREATE_FAILED,
                        status_code=status.HTTP_403_FORBIDDEN
                    )
            except ExamSubject.DoesNotExist:
                return send_response(
                    error_code="Exam subject not found.",
                    message=ResponseMessages.RECORD_CREATE_FAILED,
                    status_code=status.HTTP_404_NOT_FOUND
                )

        if student_id and exam_subject_id:
            exists = ExamResult.objects.filter(
                student_id=student_id,
                exam_subject_id=exam_subject_id
            ).exclude(id=result.id).exists()
            if exists:
                return send_response(
                    error_code="Result for this student and exam subject already exists.",
                    message=ResponseMessages.RECORD_CREATE_FAILED,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        if not result:
            raise NotFound("Exam Result not found.")

        serializer = ExamResultSerializer(result, data=request.data)
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

    def delete(self, request, pk):
        result = self.get_object(pk, request.user.school)
        result.delete()
        return send_response(
            message=ResponseMessages.DATA_DELETED_SUCCESS,
            status_code=status.HTTP_204_NO_CONTENT
        )
