from django.urls import path
from .views import user as user_views
from classrooms import views as classroom_views
from subjects.views import subject as subject_views, classroom_subject as classroom_subject_views
from teachers import views as teacher_views
from .views import CustomTokenObtainPairView, CustomTokenRefreshView
from students.views import StudentListCreateAPIView, StudentRetrieveUpdateDeleteAPIView
from exams.views import (
    ExamListCreateAPIView, ExamSubjectListCreateAPIView,
    ExamResultListCreateAPIView, ExamRetrieveUpdateDeleteAPIView,
    ExamSubjectRetrieveUpdateDeleteAPIView, ExamResultRetrieveUpdateDeleteAPIView
)
from attendances.views import (
    StudentAttendanceListCreateAPIView, TeacherAttendanceListCreateAPIView,
    StudentAttendanceRetrieveUpdateDeleteAPIView,
    TeacherAttendanceRetrieveUpdateDeleteAPIView
)
from fees.views import (
    FeeCategoryListCreateAPIView, FeeStructureListCreateAPIView,
    StudentFeeListCreateAPIView, PaymentListCreateAPIView,
    FeeCategoryRetrieveUpdateDeleteAPIView, FeeStructureRetrieveUpdateDeleteAPIView,
    StudentFeeRetrieveUpdateDeleteAPIView, PaymentRetrieveUpdateDeleteAPIView
)

urlpatterns = [
    # JWT Auth
    path('auth/token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/token/refresh/',
         CustomTokenRefreshView.as_view(), name='token_refresh'),

    # Users
    path('users/', user_views.ListCreateUsersView.as_view(),
         name='list-create-user'),

    # Classrooms
    path('classrooms/', classroom_views.ClassroomListCreateView.as_view(),
         name='classroom-create'),
    path('classrooms/bulk/', classroom_views.ClassroomBulkUploadAPIView.as_view(),
         name='classroom-bulk-upload'),
    path('classrooms/<int:pk>/',
         classroom_views.ClassroomDetailView.as_view(), name='classroom-detail'),

    # Subjects
    path('subjects/', subject_views.SubjectListCreateView.as_view(),
         name='subject-create'),
    path('subjects/bulk/', subject_views.SubjectBulkUploadView.as_view(),
         name='subject-bulk-upload'),
    path('subjects/<int:pk>/', subject_views.SubjectDetailView.as_view(),
         name='subject-detail'),

    # Classroom-Subjects
    path('classroom-subjects/',
         classroom_subject_views.ClassroomSubjectListCreateView.as_view(), name='cs-create'),
    path('classroom-subjects/<int:pk>/',
         classroom_subject_views.ClasroomSubjectDetailView.as_view(), name='cs-detail'),

    # Teachers
    path('teachers/', teacher_views.TeacherListCreateView.as_view(),
         name='teacher-list-create'),
    path('teachers/<int:pk>/',
         teacher_views.TeacherRetrieveUpdateDestroyView.as_view(), name='teacher-detail'),

    # Students
    path('students/', StudentListCreateAPIView.as_view(),
         name='student-list-create'),
    path('students/<int:pk>/',
         StudentRetrieveUpdateDeleteAPIView.as_view(), name='student-detail'),

    # Exams
    path('exams/', ExamListCreateAPIView.as_view(), name='exam-list-create'),
    path('exams/<int:pk>/', ExamRetrieveUpdateDeleteAPIView.as_view(),
         name='exam-detail'),

    path('exam-subjects/', ExamSubjectListCreateAPIView.as_view(),
         name='exam-subject-list-create'),
    path('exam-subjects/<int:pk>/',
         ExamSubjectRetrieveUpdateDeleteAPIView.as_view(), name='exam-subject-detail'),

    path('exam-results/', ExamResultListCreateAPIView.as_view(),
         name='exam-result-list-create'),
    path('exam-results/<int:pk>/',
         ExamResultRetrieveUpdateDeleteAPIView.as_view(), name='exam-result-detail'),

    # fees
    path('fee/category/', FeeCategoryListCreateAPIView.as_view(),
         name='fee-category'),
    path('fee/category/<int:pk>/', FeeCategoryRetrieveUpdateDeleteAPIView.as_view(),
         name='fee-category-update'),

    path('fee/structure/', FeeStructureListCreateAPIView.as_view(),
         name='fee-structure'),
    path('fee/structure/<int:pk>/', FeeStructureRetrieveUpdateDeleteAPIView.as_view(),
         name='fee-structure-update'),

    path('fee/student/', StudentFeeListCreateAPIView.as_view(),
         name='fee-student'),
    path('fee/student/<int:pk>/', StudentFeeRetrieveUpdateDeleteAPIView.as_view(),
         name='fee-student-update'),

    path('fee/payment/', PaymentListCreateAPIView.as_view(),
         name='fee-payment'),
    path('fee/payment/<int:pk>/', PaymentRetrieveUpdateDeleteAPIView.as_view(),
         name='fee-payment-update'),

    # attendance
    path('student-attendance/', StudentAttendanceListCreateAPIView.as_view(),
         name='student-attendance'),
    path('student-attendance/<int:pk>/', StudentAttendanceRetrieveUpdateDeleteAPIView.as_view(),
         name='student-attendance-update'),

    path('teacher-attendance/', TeacherAttendanceListCreateAPIView.as_view(),
         name='teacher-attendance'),
    path('teacher-attendance/<int:pk>/', TeacherAttendanceRetrieveUpdateDeleteAPIView.as_view(),
         name='teacher-attendance-update'),

]
