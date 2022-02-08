from django.contrib import admin
from  .models import  room, course, lecturer, department, faculty, hold_class,carryOver
# Register your models here.
admin.site.register(room)
admin.site.register(course)
admin.site.register(lecturer)
admin.site.register(department)
admin.site.register(faculty)
admin.site.register(hold_class)
admin.site.register(carryOver)
