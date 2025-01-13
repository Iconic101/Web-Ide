from rest_framework import serializers
from .models import *

#
# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = File
#         fields = ['id', 'name', 'content', 'project']

class ProjectSerializer(serializers.ModelSerializer):
    # files = FileSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = "__all__"

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value




