from rest_framework import generics, permissions, status
from ..models import Subject
from ..serializers.subject import SubjectSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from utils.restful_response import send_response
import openpyxl
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SubjectListCreateView(generics.ListCreateAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subject.objects.filter(school=self.request.user.school)


class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subject.objects.filter(school=self.request.user.school)


class SubjectBulkUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
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
            return send_response(
                message="No file uploaded.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
        except Exception as e:
            return send_response(
                message=f"Invalid Excel file: {str(e)}",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        created = []
        existed = set(name.lower() for name in Subject.objects.filter(
            school=request.user.school).values_list('name', flat=True))

        for row in sheet.iter_rows(min_row=2, values_only=True):
            name = row[0]
            if name and name.lower() not in existed:
                created.append(Subject(name=name.strip(),
                               school=request.user.school))
                existed.add(name.lower())

        if created:
            Subject.objects.bulk_create(created)
            return send_response(
                message=f"{len(created)} subjects uploaded successfully.",
                status_code=status.HTTP_200_OK
            )
        else:
            return send_response(
                message="No new subjects to upload. All are duplicates.",
                status_code=status.HTTP_200_OK
            )
