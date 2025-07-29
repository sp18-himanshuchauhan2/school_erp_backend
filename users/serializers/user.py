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

    def validate(self, data):
        request = self.context['request']
        curr_user = request.user

        if curr_user.role == 'SCHOOL_ADMIN':
            if data.get('role') == "MAIN_ADMIN":
                raise serializers.ValidationError("You are not allowed to create a Main Admin user.")
        return data

    def create(self, validated_data):
        request = self.context['request']
        school = request.user.school
        password = validated_data.pop('password')
        role = validated_data.get('role')

        user = User(**validated_data)
        user.school = school
        user.set_password(password)

        if role == 'SCHOOL_ADMIN':
            user.is_staff = True
        user.save()

        if role:
            try:
                group = Group.objects.get(name=role.lower())
                user.groups.add(group)
                print(f"User added to group: {group.name}")
            except Group.DoesNotExist:
                print(f"Group '{role}' does not exist — cannot assign group.")
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role']
