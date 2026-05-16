from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Category, CustomUser, SubTask, Task


# OopCompanion:suppressRename



class FlexibleDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        if not value:
            return None
        return super().to_representation(value)


class TaskSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(allow_null=True, required=False)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"


class SubTaskCreateSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(allow_null=True, required=False)

    class Meta:
        model = SubTask
        fields = [
            "id",
            "title",
            "description",
            "task",
            "status",
            "deadline",
            "created_at",
            "owner",
        ]
        read_only_fields = ["id", "created_at", "owner"]


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]

    def create(self, validated_data):
        if Category.objects.filter(name=validated_data["name"]).exists():
            raise serializers.ValidationError(
                "Категория с таким названием уже существует"
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if (
                "name" in validated_data
                and Category.objects.filter(name=validated_data["name"])
                .exclude(id=instance.id)
                .exists()
        ):
            raise serializers.ValidationError(
                "Категория с таким названием уже существует"
            )
        return super().update(instance, validated_data)


class SubTaskSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(allow_null=True, required=False)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SubTask
        fields = ["id", "title", "description", "status", "deadline", "created_at", "owner"]


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "deadline",
            "created_at",
            "categories",
            "subtasks",
            "owner",
        ]
        read_only_fields = ["id", "created_at"]


class TaskCreateSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(allow_null=True, required=False)

    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "deadline", "categories", "owner"]
        read_only_fields = ["id", "owner"]
        extra_kwargs = {"categories": {"required": False}}

    def validate_deadline(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Дата дедлайна не может быть в прошлом")
        return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(),
                message="A user with that email already exists."
            )
        ]
    )
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(),
                message="A user with that username already exists."
            )
        ]
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_active:
                msg = 'User account is disabled.'
                raise serializers.ValidationError(msg, code='authorization')

            attrs['user'] = user
            return attrs
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'date_joined', 'is_verified')
        read_only_fields = ('id', 'email', 'date_joined', 'is_verified')
