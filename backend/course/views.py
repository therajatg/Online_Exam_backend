from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework import status

# Create your views here.

# Add a Course
class AddCourseAPI(APIView):
    """Create a new course"""
    def post(self,request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(
            {
                'message':"Course created successfully",
                'status':status.HTTP_200_OK
                }
        )

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class UpdateCourseAPI(APIView):
    def put(self, request):
        course_name = request.data['course_name']
        course = Course.objects.get(course_name=course_name)
        serializer = CourseUpdateSerializer(course,request.data,many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data
            )

class DeleteCourseAPI(APIView):
    def delete(self, request):
        course_name = request.data['course_name']
        course = Course.objects.get(course_name=course_name)        
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddTestAPI(APIView):
    """Create a new test"""
    def post(self,request):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(
            {
                'message':"Test created successfully",
                'status':status.HTTP_200_OK
                }
        )

    def get(self, request):
        tests = Test.objects.all()
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)

class UpdateTestAPI(APIView):
    def put(self, request, pk):
        test = Test.objects.get(test_id=pk)
        serializer = TestUpdateSerializer(test,request.data,many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data
            )

class DeleteTestAPI(APIView):
    def delete(self, request, pk):
        test = Test.objects.get(test_id=pk)
        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

