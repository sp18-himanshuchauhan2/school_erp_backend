from django.urls import path
from .views import (
    StudentProfileAPIView,
    ExamTimetableAPIView,
    StudentAttendanceAPIView,
    StudentExamResultsAPIView,
    StudentFeeDetailsAPIView,
    StudentClassroomSubjectsAPIView,
    StudentReportCardAPIView,
)

urlpatterns = [
    path('profile/', StudentProfileAPIView.as_view()),
    path('timetable/exams/', ExamTimetableAPIView.as_view()),
    path('attendance/', StudentAttendanceAPIView.as_view()),
    path('exam-results/', StudentExamResultsAPIView.as_view()),
    path('fees/', StudentFeeDetailsAPIView.as_view()),
    path('classroom-subjects/', StudentClassroomSubjectsAPIView.as_view()),
    path('report-card/', StudentReportCardAPIView.as_view()),
]
