from django.urls import path
from .views import user as user_views
from classrooms import views as classroom_views
from subjects.views import subject as subject_views, classroom_subject as classroom_subject_views
from teachers import views as teacher_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from students.views import StudentListCreateAPIView, StudentRetrieveUpdateDeleteAPIView

urlpatterns = [
    # JWT Auth
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

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

]
