from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import Token
from .serializers import UserSerializer, UserUpdateSerializer
from django.http import Http404

# from .models import Student
import jwt, datetime
from rest_framework import status
from django.contrib.auth.models import User, Group

# Create your views here.

# Register a student
class RegisterAPI(APIView):
    """Create a new student"""
    def post(self,request):
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        username = request.data["username"]
        email = request.data["email"]
        password = request.data["password"]
        request_group_name = request.data["group"]
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            )
        # user.save(commit=False)
        user.set_password(password)
        user.save()
        group_name = Group.objects.get(name=request_group_name)
        user.groups.add(group_name)
    
        return Response(
            {
                'message':"Student created successfully",
                'status':status.HTTP_200_OK
                }
        )


    def get(self, request):
        users = User.objects.filter(groups__name='student').values()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# # Logging in a student by authenticating jwt token
class LoginAPI(APIView):

    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")

        payload = {
            "id":user.id,
            "exp":datetime.datetime.utcnow() + datetime.timedelta(seconds=40),
            "iat":datetime.datetime.utcnow()
        }

        token = jwt.encode(payload,'secret',algorithm="HS256")

        response = Response()

        response.set_cookie(key="jwt",value=token,httponly=True)

        response.data= {
            'jwt':token
        }
        return response

        # return Response({
        #     'jwt':token
        # })

        # return Response(serializer.data)

class StudentUpdateAPI(APIView):
    def put(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(token,'secret',algorithms=["HS256"])
        
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")
        
        user = User.objects.get(id=payload['id'])
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


class StudentViewAPI(APIView):
    """Retrieve, update or delete a student instance."""
    # View a single student using token
    def get(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(token,'secret',algorithms=["HS256"])
        
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutAPI(APIView):
# Logout a single student using token
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'User logged out successfully'
        }

        return response


# class StudentList(APIView):
    """
    List all students, create, or update (using JWT token) a new student.
    """
    def get(self, request):
        users = User.objects.filter(groups__name='student').values()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        username = request.data["username"]
        email = request.data["email"]
        password = request.data["password"]
        request_group_name = request.data["group"]
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            )
        # user.save(commit=False)
        user.set_password(password)
        try:
            user.save()
            group_name = Group.objects.get(name=request_group_name)
            user.groups.add(group_name)
            return Response(
                {
                    'message':"Student created successfully",
                    'status':status.HTTP_200_OK
                }
            )
        except:
            return Response(
                {
                    'message':"Some error occurred",
                    'status':status.HTTP_400_BAD_REQUEST
                })


    def put(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(token,'secret',algorithms=["HS256"])
        
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")
        
        user = User.objects.get(id=payload['id'])
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class StudentDetail(APIView):
    """
    Retrieve, delete a student instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        student = self.get_object(pk)
        serializer = UserSerializer(student)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)