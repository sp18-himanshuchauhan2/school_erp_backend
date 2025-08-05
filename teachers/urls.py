from django.urls import path
from .views import (
    TeacherProfileAPIView,
    TeacherClassroomSubjectAPIView,
    StudentInClassSubjectAPIView,
    MarkAttendanceAPIView,
    TeacherClassResultSummaryAPIView,
    TeacherUpdateMarksAPIView
)


urlpatterns = [
    path('profile/', TeacherProfileAPIView.as_view(),
         name='teacher-profile'),
    path('classrooms-subjects/', TeacherClassroomSubjectAPIView.as_view(),
         name='teacher-classrooms-subjects'),
    path('students/', StudentInClassSubjectAPIView.as_view(),
         name='teacher-students'),
    path('attendance/<int:classroom_id>/', MarkAttendanceAPIView.as_view(),
         name='mark-attendance'),
    path('exam-subjects/<int:exam_subject_id>/marks/', TeacherUpdateMarksAPIView.as_view(),
         name='update-marks'),
    path('classrooms/<int:classroom_id>/results/', TeacherClassResultSummaryAPIView.as_view(),
         name='class-result-summary'),
]
