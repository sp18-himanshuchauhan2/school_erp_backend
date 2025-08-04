from django.forms import ValidationError
from django.shortcuts import render
from .models import FeeCategory, FeeStructure, StudentFee, Payment
from .serializers import FeeCategorySerializer, FeeStructureSerializer, StudentFeeSerializer, PaymentSerializer
from rest_framework.views import APIView
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from rest_framework import permissions, status
from schools.models import School
from classrooms.models import Classroom
from students.models import Student

# Create your views here.


def get_user_school(user):
    if user.is_superuser:
        return None
    return getattr(user, 'school', None)


class FeeCategoryListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        school = get_user_school(request.user)
        qs = FeeCategory.objects.all(
        ) if request.user.is_superuser else FeeCategory.objects.filter(school=school)
        serializer = FeeCategorySerializer(qs, many=True)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    def post(self, request):
        school = get_user_school(request.user)
        data = request.data.copy()

        if not request.user.is_superuser:
            data['school'] = school.id

        serializer = FeeCategorySerializer(data=data)
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


class FeeCategoryRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        school = get_user_school(user)
        try:
            obj = FeeCategory.objects.get(pk=pk)
            if user.is_superuser or obj.school == school:
                return obj
        except FeeCategory.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return send_response(
                message="Not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = FeeCategorySerializer(obj)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS
        )

    def put(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return send_response(
                message="Not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        data = request.data.copy()
        if not request.user.is_superuser:
            data['school'] = request.user.school.id

        serializer = FeeCategorySerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return send_response(
                data=serializer.data,
                message=ResponseMessages.DATA_UPDATE_SUCCESS
            )
        return send_response(
            data=serializer.errors,
            message=ResponseMessages.DATA_UPDATE_FAILED,
            status_code=400
        )

    def delete(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return send_response(
                message="Not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        obj.delete()
        return send_response(
            message=ResponseMessages.RECORD_DELETED
        )


class FeeStructureListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        school = get_user_school(request.user)
        if request.user.is_superuser:
            qs = FeeStructure.objects.all()
        else:
            qs = FeeStructure.objects.filter(classroom__school=school)

        serializer = FeeStructureSerializer(qs, many=True)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    def post(self, request):
        school = get_user_school(request.user)
        data = request.data.copy()

        if not request.user.is_superuser:
            classroom = Classroom.objects.filter(
                school=school, id=data.get('classroom')).first()
            category = FeeCategory.objects.filter(
                school=school, id=data.get('category')).first()

            if not classroom or not category:
                return send_response(
                    message='Invalid classroom or category for your school',
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = FeeStructureSerializer(data=data)
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


class FeeStructureRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        school = get_user_school(user)
        try:
            obj = FeeStructure.objects.get(pk=pk)
            if user.is_superuser or obj.classroom.school == school:
                return obj
        except FeeStructure.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return send_response(
                message="Not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = FeeStructureSerializer(obj)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    def put(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return send_response(
                message="Not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = FeeStructureSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return send_response(
                data=serializer.data,
                message=ResponseMessages.DATA_UPDATE_SUCCESS
            )
        return send_response(
            data=serializer.errors,
            message=ResponseMessages.DATA_UPDATE_FAILED,
            status_code=400
        )

    def delete(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return send_response(
                message="Not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        obj.delete()
        return send_response(
            message=ResponseMessages.RECORD_DELETED
        )


class StudentFeeListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        school = get_user_school(request.user)
        if request.user.is_superuser:
            qs = StudentFee.objects.all()
        else:
            qs = StudentFee.objects.filter(student__classroom__school=school)

        serializer = StudentFeeSerializer(qs, many=True)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    def post(self, request):
        school = get_user_school(request.user)
        data = request.data.copy()

        if not request.user.is_superuser:
            student = Student.objects.filter(
                classroom__school=school, id=data.get('student')).first()
            fee_structure = FeeStructure.objects.filter(
                classroom__school=school, id=data.get('fee_structure')).first()

            if not student or not fee_structure:
                return send_response(
                    message='Invalid student or fee structure for your school',
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        serializer = StudentFeeSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return send_response(
                data=serializer.data,
                message=ResponseMessages.RECORD_CREATED,
                status_code=status.HTTP_201_CREATED
            )
        except Exception:
            return send_response(
                data=serializer.errors,
                message=ResponseMessages.RECORD_CREATE_FAILED,
                status_code=status.HTTP_400_BAD_REQUEST
            )


class StudentFeeRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        school = get_user_school(user)
        try:
            obj = StudentFee.objects.get(pk=pk)
            if user.is_superuser or obj.student.classroom.school == school:
                return obj
        except StudentFee.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return send_response(
                message="Not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = StudentFeeSerializer(obj)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS
        )

    def put(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return send_response(
                message="Not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentFeeSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return send_response(
                data=serializer.data,
                message=ResponseMessages.DATA_UPDATE_SUCCESS
            )
        return send_response(
            data=serializer.errors,
            message=ResponseMessages.DATA_UPDATE_FAILED,
            status_code=400
        )

    def delete(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return send_response(
                message="Not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        obj.delete()
        return send_response(
            message=ResponseMessages.RECORD_DELETED
        )


class PaymentListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        school = get_user_school(request.user)
        if request.user.is_superuser:
            qs = Payment.objects.all()
        else:
            qs = Payment.objects.filter(fee__student__classroom__school=school)

        serializer = PaymentSerializer(qs, many=True)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    def post(self, request):
        school = get_user_school(request.user)
        data = request.data.copy()

        if not request.user.is_superuser:
            fee = StudentFee.objects.filter(
                student__classroom__school=school, id=data.get('fee')).first()
            if not fee:
                return send_response(
                    message='Invalid student fee for your school',
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        serializer = PaymentSerializer(data=data)
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


class PaymentRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        school = get_user_school(user)
        try:
            obj = Payment.objects.get(pk=pk)
            if user.is_superuser or obj.fee.student.classroom.school == school:
                return obj
        except Payment.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return send_response(
                message="Not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = PaymentSerializer(obj)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS
        )

    def put(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return send_response(message="Not found", status_code=status.HTTP_404_NOT_FOUND)

        serializer = PaymentSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return send_response(
                data=serializer.data,
                message=ResponseMessages.DATA_UPDATE_SUCCESS
            )
        return send_response(
            data=serializer.errors,
            message=ResponseMessages.DATA_UPDATE_FAILED,
            status_code=400
        )

    def delete(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return send_response(
                message="Not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        obj.delete()
        return send_response(
            message=ResponseMessages.RECORD_DELETED
        )
