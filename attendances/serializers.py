from rest_framework import serializers
from .models import StudentAttendance, TeacherAttendance
from students.models import Student
from classrooms.models import Classroom
from teachers.models import Teacher


class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = '__all__'

    def validate(self, data):
        student = data['student']
        classroom = data['classroom']

        if student.classroom != classroom:
            raise serializers.ValidationError(
                "Selected student is not part of the selected classroom."
            )
        return data
    

class TeacherAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAttendance
        fields = '__all__'