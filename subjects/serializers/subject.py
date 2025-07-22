from rest_framework import serializers
from ..models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        read_only_fields = ['school']
    
    def validate_name(self, name):
        request = self.context['request']
        school = request.user.school

        if not self.instance:
            if Subject.objects.filter(name__iexact=name, school=school).exists():
                raise serializers.ValidationError(f"Subject '{name}' already exists in this school.")
        else:
            if self.instance.name.lower() != name.lower():
                if Subject.objects.filter(name__iexact=name, school=school).exists():
                    raise serializers.ValidationError(f"Subject '{name}' already exists in this school.")

        return name
    
    def create(self, validated_data):
        validated_data['school'] = self.context['request'].user.school
        return super().create(validated_data)