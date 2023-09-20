from rest_framework import serializers
from .models import Attachment, Task, TaskList
from house.models import House


class TaskListSerializer(serializers.ModelSerializer):

    house = serializers.HyperlinkedRelatedField(
        queryset=House.objects.all, many=False, view_name='house-detail')
    created_by = serializers.HyperlinkedRelatedField(
        read_only=True, many=False, view_name='profile-detail')
    tasks = serializers.HyperlinkedRelatedField(
        read_only=True, many=False, view_name='task-detail')

    class Meta:
        model = TaskList
        fields = ['url', 'name', 'description', 'status',
                  'created_on', 'created_by', 'house']
        read_only_field = ['created_on', 'status']


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.HyperlinkedRelatedField(
        read_only=True, many=False, view_name='profile-detail')
    completed_by = serializers.HyperlinkedRelatedField(
        read_only=True, many=False, view_name='profile-detail')

    task_lists = serializers.HyperlinkedRelatedField(
        queryset=TaskList.objects.all(), many=False, view_name='tasklist-detail')

    def validate_task_lists(self, value):
        user_profile = self.context['request'].user.profile
        if value not in user_profile.house.lists.all():
            raise serializers.ValidationError("this does not exist")
        return value

    def create(self, validated_data):
        user_profile = self.context['request'].user.profile
        task = Task.objects.create(**validated_data)
        task.create_by = user_profile
        task.save()

    class Meta:
        model = Task
        fields = ['url', 'id', 'name', 'description', 'status', 'created_on',
                  'completed_on', 'created_by', 'completed_by', 'task_list']
        read_only_fields = ['created_on', 'created_by',
                            'completed_by', 'completed_on', 'status']


class AttachmentSerializer(serializers.ModelSerializer):
    created_on = serializers.HyperlinkedRelatedField(
        queryset=Task.objects.all(), many=False, view_name='task-detail')

    def validate(self, attrs):
        user_profile = self.context['request'].user.profile
        task = attrs['task']
        task_list = TaskList.objects.get(tasks__id__exact=task.id)
        if task_list not in user_profile.house.lists.all():
            raise serializers.ValidationError("does not belong")
        return attrs

    class Meta:
        model = Attachment
        fields = ['url', 'id', 'created_on', 'data', 'task']
        read_only_fields = ['created_on']
