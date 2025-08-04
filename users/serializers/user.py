import uuid
from rest_framework import serializers
from ..models import User
from django.contrib.auth.models import Group


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists.")
        return value

    def validate(self, data):
        request = self.context['request']
        curr_user = request.user

        if curr_user.role == 'SCHOOL_ADMIN':
            if data.get('role') == "MAIN_ADMIN":
                raise serializers.ValidationError(
                    "You are not allowed to create a Main Admin user."
                )
        return data

    def create(self, validated_data):
        request = self.context['request']
        school = request.user.school
        password = validated_data.pop('password')
        role = validated_data.get('role')

        username = f"user_{uuid.uuid4().hex[:8]}"
        while User.objects.filter(username=username).exists():
            username = f"user_{uuid.uuid4().hex[:8]}"

        user = User(**validated_data)
        user.username = username
        user.school = school
        user.set_password(password)

        if role == 'SCHOOL_ADMIN':
            user.is_staff = True
        user.save()

        if role:
            try:
                group = Group.objects.get(name=role.lower())
                user.groups.add(group)
            except Group.DoesNotExist:
                pass

        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role']
