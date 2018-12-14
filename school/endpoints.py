from django.conf.urls import url
from django.urls import path
from .api import RegistrationAPI, LoginAPI, CurrentUserAPI, UsersAPI, \
    TeacherSubjectsAPI, ExamCreateAPI, TeacherSubjectAdd, SubjectAPI, \
    StudentAPI, ParentAPI, ParentDetailAPI, MarksCreateAPI, AttendanceAPI, CurrentStudentAPI

urlpatterns = [
    url("^auth/register/$", RegistrationAPI.as_view()),
    url("^auth/login/$", LoginAPI.as_view()),
    url("^current_user/$", CurrentUserAPI.as_view()),
    path('users/', UsersAPI.as_view()),
    path('exam/', ExamCreateAPI.as_view()),
    path('subjects/', SubjectAPI.as_view()),
    path('student/', StudentAPI.as_view()),
    path('parent/', ParentAPI.as_view()),
    path('current_student/', CurrentStudentAPI.as_view()),
    path('parent/<int:pk>/', ParentDetailAPI.as_view()),
    path('teacher_subjects/', TeacherSubjectsAPI.as_view()),
    path('add_subject_for_teacher/', TeacherSubjectAdd.as_view()),
    path('exam_marks/', MarksCreateAPI.as_view()),
    path('exam_marks/<int:student>/', MarksCreateAPI.as_view()),
    path('attendance/<int:student>/', AttendanceAPI.as_view())
]
