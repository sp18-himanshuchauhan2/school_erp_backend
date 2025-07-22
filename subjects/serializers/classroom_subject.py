from rest_framework import serializers
from ..models import ClassroomSubject

class ClassroomSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomSubject
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        classroom = attrs['classroom']
        subject = attrs['subject']

        if classroom.school != user.school:
            raise serializers.ValidationError("Classroom does not belong to your school.")
        
        if subject.school != user.school:
            raise serializers.ValidationError("Subject does not belong to your school.")
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('school', None)
        return super().create(validated_data)