from school.models import Teacher, User, Subject, Exam, Student, Parent, Marks, Attendance
from .serializers import UserSerializer, \
    CreateUserSerializer, LoginUserSerializer, \
    TeacherSerializer, ExamSerializer, ExamCreateSerializer, \
    TeacherCreateSerializer, SubjectSerializer, \
    StudentSerializer, ParentSerializer, ParentCreateSerializer, \
    StudentCreateSerializer, MarksCreateSerializer, MarksSerializer, \
    AttendanceSerializer

from rest_framework import generics
from rest_framework.views import APIView
from .permission import UserPermission
from rest_framework.response import Response
from knox.models import AuthToken


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)
        })


class CurrentUserAPI(generics.RetrieveAPIView):
    permission_classes = [UserPermission, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UsersAPI(generics.ListAPIView):
    permission_classes = [UserPermission, ]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class TeacherSubjectsAPI(generics.ListAPIView):
    permission_classes = [UserPermission, ]
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ExamCreateAPI(generics.ListCreateAPIView):
    permission_classes = [UserPermission, ]
    queryset = Exam.objects.all()
    serializer_class = ExamCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExamSerializer
        else:
            return ExamCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "exam": serializer.data,
            "response": True
        })


class StudentAPI(generics.ListCreateAPIView):
    permission_classes = [UserPermission, ]
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StudentSerializer
        else:
            return StudentCreateSerializer


class CurrentStudentAPI(generics.RetrieveAPIView):
    permission_classes = [UserPermission, ]

    def get(self, request, *args, **kwargs):
        return Response(StudentCreateSerializer(Student.objects.get(user=self.request.user)).data)


class SubjectAPI(APIView):
    permission_classes = [UserPermission, ]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        return Response({
            "subject": self.serializer_class(student, context=self.serializer_class).data,
            "response": True
        })

    def get(self, request, format=None):
        serializer = self.serializer_class(Subject.objects.all(), many=True, context=request)
        return Response(serializer.data)


class ParentAPI(generics.ListCreateAPIView):
    permission_classes = [UserPermission, ]
    queryset = Parent.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ParentSerializer
        else:
            return ParentCreateSerializer


class ParentDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [UserPermission, ]
    queryset = Parent.objects.all()

    def get(self, request, *args, **kwargs):
        print(kwargs)
        if kwargs.get('pk'):
            serializer = self.get_serializer(Parent.objects.get(parent=kwargs.get('pk')),context=request)
        else:
            serializer = self.get_serializer(Parent.objects.all(), context=request)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ParentSerializer
        else:
            return ParentCreateSerializer


class MarksCreateAPI(generics.ListCreateAPIView):
    permission_classes = [UserPermission, ]
    queryset = Marks.objects.all()

    def post(self, request, *args, **kwargs):
        print(self.get_serializer_class())
        serializer = MarksCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exam = serializer.save()
        exam.save()
        return Response({
            "exam": MarksCreateSerializer(exam, context=self.get_serializer_class()).data,
            "response": True
        })

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MarksSerializer
        else:
            return MarksCreateSerializer


class TeacherSubjectAdd(generics.ListCreateAPIView):
    permission_classes = [UserPermission, ]
    queryset = Teacher.objects.all()
    serializer_class = TeacherCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        ts = serializer.save()
        ts.save()
        return Response({
            "record": self.serializer_class(ts, context=self.serializer_class).data,
            "response": True
        })


class AttendanceAPI(generics.ListAPIView):
    permission_classes = [UserPermission, ]
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        print("hola")
        print(self.kwargs)
        if self.kwargs.get('student'):
            return Attendance.objects.filter(student=self.kwargs.get('student'))
        else:
            return Attendance.objects.all()
