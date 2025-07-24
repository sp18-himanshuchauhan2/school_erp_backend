from rest_framework import serializers
from .models import Student
from users.models import User


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='STUDENT'))

    class Meta:
        model = Student
        fields = ['id', 'user', 'classroom', 'roll_no',
                  'gender', 'dob', 'enrollment_date']
        read_only_fields = ['enrollment_date']

    def validate(self, data):
        request = self.context.get('request')
        user = data.get('user')
        classroom = data.get('classroom')

        if not request:
            return data
        
        if request.user.role == 'SCHOOL_ADMIN':
            if user and user.school != request.user.school:
                raise serializers.ValidationError(
                    "student user must belong to your school.")
            if classroom and classroom.school != request.user.school:
                raise serializers.ValidationError(
                    "Classroom must belong to your school.")
        return data
