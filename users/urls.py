from django.urls import path
from .views import user as user_views
from classrooms import views as classroom_views
from subjects.views import subject as subject_views, classroom_subject as classroom_subject_views
from teachers import views as teacher_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # JWT login
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # school-admin views
    # path('users/', views.SchoolAdminUserListView.as_view(), name='school_users'),
    # path('classrooms/', views.SchoolAdminClassroomListView.as_view(), name='school_classrooms'),
    # path('subjects/', views.SchoolAdminSubjectListView.as_view(), name='school_subjects'),
    # path('classroom-subjects/', views.SchoolAdminClassroomSubjectListView.as_view(), name='school_classroom_subjects'),

    # CRUD
    path('users/', user_views.ListCreateUsersView.as_view(),
         name='list-create-user'),

    path('classrooms/', classroom_views.ClassroomListCreateView.as_view(),
         name='classroom-create'),
    path('classrooms/<int:pk>/',
         classroom_views.ClassroomDetailView.as_view(), name='classroom-detail'),

    path('subjects/', subject_views.SubjectListCreateView.as_view(),
         name='subject-create'),
    path('subjects/<int:pk>/', subject_views.SubjectDetailView.as_view(),
         name='subject-detail'),

    path('classroom-subjects/',
         classroom_subject_views.ClassroomSubjectListCreateView.as_view(), name='cs-create'),
    path('classroom-subjects/<int:pk>/',
         classroom_subject_views.ClasroomSubjectDetailView.as_view(), name='cs-detail'),

    path('teacher/', teacher_views.TeacherListCreateView.as_view(),
         name='teacher-list-create'),
    path('teacher/<int:pk>/',
         teacher_views.TeacherRetrieveUpdateDestroyView.as_view(), name='teacher-detail'),
]
