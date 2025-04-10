from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        fields = ['id', 'title', 'description', 'due_date', 'is_completed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
