from rest_framework import serializers
from .models import *

from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Course
        fields = '__all__'


class CourseUpdateSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Course
        fields = ['course_name','course_description']
        
    def update(self, instance, validated_data):
        instance.course_name = validated_data.get('course_name', instance.course_name)
        instance.course_description = validated_data.get('course_description', instance.course_description)
        instance.save()
        return instance

class TestSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Test
        fields = '__all__'


class TestUpdateSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Test
        fields = ['test_name']
        
    def update(self, instance, validated_data):
        instance.test_name = validated_data.get('test_name', instance.test_name)
        instance.save()
        return instance