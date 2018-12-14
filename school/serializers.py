from .models import User, Teacher, Subject, \
    Course, Department, Exam, Student, Parent, \
    Marks, Attendance
from rest_framework import serializers
from django.core.serializers import serialize as django_serialize
from django.contrib.auth import authenticate


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'user_type', 'name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        user_type=validated_data['user_type'],
                                        name=validated_data['name'],
                                        password=validated_data['password'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'user_type')


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Unable to log in with provided credentials')


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('id', 'name')


class CourseSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'department')


class SubjectSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True, many=True)

    class Meta:
        model = Subject
        fields = ('id', 'name', 'course')


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    subject = SubjectSerializer(read_only=True, many=False)

    class Meta:
        model = Teacher
        fields = ('id', 'user', 'subject')


class StudentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    department = DepartmentSerializer()
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ("id", "user", "course", "department", "year_of_study")


class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("id", "user", "course", "department", "year_of_study")

    def _user(self):
        request = getattr(self.context, 'request', None)
        if request:
            return request.user

    def create(self, validated_data):
        student = Student(user=validated_data['user'],
                          course=validated_data['course'],
                          department=validated_data['department'],
                          year_of_study=validated_data['year_of_study'])
        student.save()
        return student
    

class ExamSerializer(serializers.ModelSerializer):

    subject = SubjectSerializer()
    course = CourseSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = Exam
        fields = ('id', 'subject', 'course', 'department', 'total_marks', 'year_of_study', 'creation_date')


class ExamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ('id', 'subject', 'course', 'department', 'total_marks', 'year_of_study', 'creation_date')

    def _user(self):
        request = getattr(self.context, 'request', None)
        print(self.context)
        if request:
            return request.user

    def create(self, validated_data):
        print(self.context['request'])
        print("wow")
        exam = Exam(created_by=self.context['request'].user,
                    subject=validated_data['subject'],
                    course=validated_data['course'],
                    total_marks=validated_data['total_marks'],
                    department=validated_data['department'],
                    year_of_study=validated_data['year_of_study'])
        exam.save()
        return exam


class ParentSerializer(serializers.ModelSerializer):
    child = StudentSerializer(many=True)

    class Meta:
        model = Parent
        fields = ("child", "parent")


class ParentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parent
        fields = ("parent", "child")


class MarksCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marks
        fields = ("student", "exam", "marks_scored")

    def create(self, validated_data):
        exam = Marks(exam=validated_data['exam'],
                    marks_scored=validated_data['marks_scored'],
                    student=validated_data['student'])
        return exam


class MarksSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    exam = ExamSerializer()

    class Meta:
        model = Marks
        fields = ("student", "exam", "marks_scored")


class TeacherCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('subject', 'user')

    def create(self, validated_data):
        teacher = Teacher(user=validated_data['user'],
                          subject=validated_data['subject'])
        return teacher


def attendanceSerializer(data):
    return django_serialize('json', list(data))


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('student', 'date', 'status')
