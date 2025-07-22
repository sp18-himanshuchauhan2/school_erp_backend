from rest_framework import serializers
from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

    def create(self, validated_data):
        validated_data['school'] = self.context['request'].user.school
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('school', None)
        return super().update(instance, validated_data)
