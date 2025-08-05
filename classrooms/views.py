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
from school_erp_backend.permissions import IsSchoolAdmin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages


class ClassroomListCreateView(generics.ListCreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated, IsSchoolAdmin]

    def get_queryset(self):
        return Classroom.objects.filter(school=self.request.user.school)

    def perform_create(self, serializer):
        serializer.save(school=self.request.user.school)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except Exception:
            return send_response(
                message="Classroom with the same name and section already exists in your school.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        headers = self.get_success_headers(serializer.data)
        return send_response(
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
            headers=headers
        )


class ClassroomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated, IsSchoolAdmin]

    def get_queryset(self):
        return Classroom.objects.filter(school=self.request.user.school)

    def perform_update(self, serializer):
        serializer.save(school=self.request.user.school)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_update(serializer)
        except Exception:
            return send_response(
                message="Class teacher already assigned for another class.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        return send_response(
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )


class ClassroomBulkUploadAPIView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated, IsSchoolAdmin]

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

        df = df.dropna(subset=['class_name', 'section'])
        df["class_name"] = df["class_name"].astype(str).str.strip().str.lower()
        df["section"] = df["section"].astype(str).str.strip().str.capitalize()

        df.drop_duplicates(subset=["class_name", "section"], inplace=True)

        class_names = df["class_name"].unique()
        sections = df["section"].unique()

        existing = Classroom.objects.filter(
            school=school,
            class_name__in=class_names,
            section__in=sections,
        ).values_list("class_name", "section")

        existing_set = set((class_name.lower(), section.capitalize())
                           for class_name, section in existing)

        df["exists"] = df.apply(
            lambda row: (row["class_name"], row["section"]) in existing_set,
            axis=1
        )
        df_new = df[~df["exists"]]

        classroom_objects = [
            Classroom(
                school=school,
                class_name=row["class_name"],
                section=row["section"],
            )
            for _, row in df_new.iterrows()
        ]
        if classroom_objects:
            Classroom.objects.bulk_create(classroom_objects)

        return send_response(
            data={
                "created": df_new[["class_name", "section"]].values.tolist(),
                "skipped": df[df["exists"]][["class_name", "section"]].values.tolist(),
            },
            message=ResponseMessages.DATA_FETCH_SUCCESS,
        )
