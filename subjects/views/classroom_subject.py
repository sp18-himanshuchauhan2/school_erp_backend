from rest_framework import generics, permissions
from ..models import ClassroomSubject
from ..serializers.classroom_subject import ClassroomSubjectSerializer


class ClassroomSubjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ClassroomSubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ClassroomSubject.objects.filter(classroom__school=self.request.user.school)


class ClasroomSubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassroomSubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ClassroomSubject.objects.filter(classroom__school=self.request.user.school)
