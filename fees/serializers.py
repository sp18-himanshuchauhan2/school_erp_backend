from rest_framework import serializers
from .models import FeeCategory, FeeStructure, StudentFee, Payment


class FeeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeCategory
        fields = '__all__'


class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = '__all__'


class StudentFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFee
        fields = '__all__'

    def validate(self, data):
        fee_structure = data.get('fee_structure')
        student = data.get('student')
        month = data.get('month')

        if fee_structure and student:
            if fee_structure.fee_type == 'monthly' and not month:
                raise serializers.ValidationError(
                    "Month is required for monthly fees.")
            if fee_structure.fee_type != 'monthly' and month:
                raise serializers.ValidationError(
                    "Month should be empty for non-monthly fees.")
            if student.classroom != fee_structure.classroom:
                raise serializers.ValidationError(
                    f"Selected student is not associated with the classroom '{fee_structure.classroom}'"
                )

        return data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
