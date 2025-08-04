from rest_framework import serializers
from .models import Exam, ExamResult, ExamSubject
from classrooms.models import Classroom


class ExamSerializer(serializers.ModelSerializer):
    classrooms = serializers.PrimaryKeyRelatedField(
        queryset=Classroom.objects.all(),
        many=True
    )

    class Meta:
        model = Exam
        fields = "__all__"


class ExamSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSubject
        fields = "__all__"
        extra_kwargs = {
            'classroom': {'required': True}
        }


class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = "__all__"

    def validate(self, data):
        data = super().validate(data)
        
        student = data.get('student')
        exam_subject = data.get('exam_subject')

        student_classroom = student.classroom
        exam_classrooms = exam_subject.exam.classrooms.all()

        if student_classroom not in exam_classrooms:
            raise serializers.ValidationError(
                "This student does not belong to the classrooms assigned for this exam."
            )
        
        if exam_subject.classroom != student_classroom:
            raise serializers.ValidationError(
                f"This subject is not assigned to the student's classroom."
            )

        return data
