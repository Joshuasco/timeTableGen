from django.urls import path, include
from  .views import room, lecturer, course, carryOver, department, faculty, hold_class, generate
from . import views

urlpatterns = [
path('', views.forms, name="forms"),
path('room/', room.as_view(), name="room"),
path('lecturer/', lecturer.as_view(), name="lecturer"),
path('course/', course.as_view(), name="course"),
path('carry_over/', carryOver.as_view(), name="carry_over"),
path('department/', department.as_view(), name="department"),
path('faculty/', faculty.as_view(), name="faculty"),
path('hold_class/', hold_class.as_view(), name="hold_class"),
path('generate/', views.generate, name="generate"),
]