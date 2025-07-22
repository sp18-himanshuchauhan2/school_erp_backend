from rest_framework import serializers
from .models import Classroom
from teachers.models import Teacher

class ClassroomSerializer(serializers.ModelSerializer):
    class_teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    class Meta:
        model = Classroom
        fields = '__all__'

    def validate_class_teacher(self, value):
        user_school = self.context['request'].user.school
        if value.user.school != user_school:
            raise serializers.ValidationError("No Teacher found.")
        return value

    def create(self, validated_data):
        validated_data['school'] = self.context['request'].user.school
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data.pop('school', None)
        return super().update(instance, validated_data)