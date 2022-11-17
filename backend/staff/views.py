from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, UserUpdateSerializer
# from .models import Staff
import jwt, datetime
from rest_framework import status
from django.contrib.auth.models import User, Group

# Create your views here.

# Register a Staff
class RegisterAPI(APIView):
    """Create a new Staff"""
    def post(self,request):
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        username = request.data["username"]
        email = request.data["email"]
        password = request.data["password"]
        req_group_name = request.data["group"]
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            is_staff = True
            )
        # user.save(commit=False)
        user.set_password(password)
        user.save()
        group_name = Group.objects.get(name=req_group_name)
        user.groups.add(group_name)
    
        return Response(
            {
                'message':"Staff created successfully",
                'status':status.HTTP_200_OK
                }
        )
        # serializer = UserSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()        
        # return Response(serializer.data)

    def get(self, request):
        users = User.objects.filter(groups__name='staff').values()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# # Logging in a staff by authenticating jwt token
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

class StaffUpdateAPI(APIView):
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

        # user = User.objects.get(id=payload['id'])
        # user = User.objects
        # serializer = UserSerializer(user,data=request.data)

        # user_id = User.objects.get(id=payload['id'])

        # # Update method, 
        # user = User(id=user_id,
        # first_name = request.data["first_name"],
        # last_name = request.data["last_name"],
        # username = request.data["username"],
        # email = request.data["email"],
        #     )

        # user.set_password(request.data['new_password'])
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message':"Staff updated successfully",
                    'status':status.HTTP_200_OK
                    }
            )

        # except:
        #     return Response(
        #         {
        #             'message':"Some error occured",
        #             'status':status.HTTP_400_BAD_REQUEST
        #             }
        #     )

class StaffViewAPI(APIView):
    """Retrieve, update or delete a staff instance."""
    # View a single staff using token
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

# Logout a single staff using token
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'User logged out successfully'
        }

        return response