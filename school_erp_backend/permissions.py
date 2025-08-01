from rest_framework.permissions import BasePermission


class IsSchoolAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'SCHOOL_ADMIN'


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'TEACHER'

