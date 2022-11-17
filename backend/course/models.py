from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100,unique=True,null=True,blank=False)
    course_description = models.CharField(max_length=500,null=True,blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,to_field='username',null=False,blank=False)

    def __str__(self) -> str:
        return f"{self.author.first_name}:{self.course_name}"

class Test(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=100,null=True,blank=False,unique=True)
    related_course_name = models.OneToOneField(Course,on_delete=models.CASCADE,to_field='course_name',null=False,blank=False)

    def __str__(self) -> str:
        return self.test_name
    
class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_name = models.TextField(max_length=255,null=False,blank=False)
    option_a = models.CharField(max_length=100,null=False,blank=False)
    option_b = models.CharField(max_length=100,null=False,blank=False)
    option_c = models.CharField(max_length=100,null=False,blank=False)
    option_d = models.CharField(max_length=100,null=False,blank=False)
    correct_ans = models.CharField(max_length=100,null=False,blank=False)
    related_test = models.ForeignKey(Test,on_delete=models.CASCADE,to_field='test_name',null=False,blank=False)

    def __str__(self) -> str:
        return f"{self.related_test.test_name}:{self.question_name}"


