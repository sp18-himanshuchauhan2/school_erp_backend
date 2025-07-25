from rest_framework import generics, permissions
from .models import Classroom
from .serializers import ClassroomSerializer
from rest_framework.views import APIView
import pandas as pd
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from schools.models import School
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ClassroomListCreateView(generics.ListCreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Classroom.objects.filter(school=self.request.user.school)


class ClassroomDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Classroom.objects.filter(school=self.request.user.school)


class ClassroomBulkUploadAPIView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            operation_description="Upload Excel file to bulk create classrooms.",
            manual_parameters=[
                openapi.Parameter(
                    name='file',
                    in_=openapi.IN_FORM,
                    type=openapi.TYPE_FILE,
                    required=True,
                    description="Excel file (.xlsx) with class_name, section, class_teacher",
                )
            ],
            responses={201: "Successfully created classrooms", 400: "Bad Request"},
    )
    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('file')

        if not excel_file:
            return Response(
                {'error': 'No file uploaded.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return Response(
                {'error': 'Invalid Excel format.', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        required_cols = ['class_name', 'section']
        for col in required_cols:
            if col not in df.columns:
                return Response(
                    {'error': f"Missing required column: {col}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        school = getattr(request.user, 'school', None)
        if not school:
            return Response(
                {'error': 'Associated school not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        created = []
        errors = []

        for index, row in df.iterrows():
            class_name = str(row.get('class_name')).strip().lower()
            section = str(row.get('section')).strip().capitalize()

            if Classroom.objects.filter(school=school, class_name=class_name, section=section).exists():
                errors.append(
                    f"Row {index+2}: Classroom {class_name}-{section} already exists.")
                continue

            Classroom.objects.create(
                school=school,
                class_name=class_name,
                section=section,
                class_teacher=None
            )
            created.append(f"{class_name}-{section}")

        return Response({
            'message': 'Upload processed.',
            'created': created,
            'errors': errors,
        }, status=status.HTTP_201_CREATED if created else status.HTTP_400_BAD_REQUEST)
