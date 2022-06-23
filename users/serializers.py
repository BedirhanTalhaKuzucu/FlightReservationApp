from asyncore import write
from wsgiref.validate import validator
from pkg_resources import require
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password=serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type":"password"}
    )

    password2=serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type":"password"}
    )

    class Meta:
        model=User
        fields=(
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",

        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password2")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user