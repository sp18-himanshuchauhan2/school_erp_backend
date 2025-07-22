from rest_framework import serializers
from django.contrib.auth import get_user_model
from classrooms.models import Classroom
from subjects.models import Subject, ClassroomSubject

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# class ClassroomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Classroom
#         fields = '__all__'


# class SubjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subject
#         fields = '__all__'


# class ClassroomSubjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClassroomSubject
#         fields = '__all__'
