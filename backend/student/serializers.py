from rest_framework import serializers
from django.contrib.auth.models import User, Group

class UserSerializer(serializers.ModelSerializer):   
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password','is_active']
        # fields = '__all__'

        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password':{'write_only':True,'required': True},
            
        }


class UserUpdateSerializer(serializers.ModelSerializer):   
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','is_active']
        

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance