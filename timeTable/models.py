from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator  


# Create your models here.

class room(models.Model):
    name= models.CharField(max_length= 50)
    capcity = models.PositiveIntegerField()
    def __str__(self):
        return (self.name + ", "+ str(self.capcity))

class faculty(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class department(models.Model):
    name =models.CharField(max_length= 50)
    faculty= models.ForeignKey(faculty, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class lecturer(models.Model):
    name = models.CharField(max_length=50)
    id_num = models.CharField(max_length=10)
    department= models.ForeignKey(department, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class course(models.Model):
    name= models.CharField(max_length= 50)
    code = models.CharField(max_length=50)
    unit = models.PositiveIntegerField( validators=[MinValueValidator(1), MaxValueValidator(3)])
    student_no = models.IntegerField()
    department= models.ForeignKey(department, on_delete=models.CASCADE)
    def __str__(self):
        return (self.code + "(" +str(self.unit)+ "), " +str(self.student_no))

class carryOver(models.Model):
    department= models.ForeignKey(department, on_delete=models.CASCADE)
    course = models.ForeignKey(course, on_delete= models.CASCADE)
    student_no =models.PositiveIntegerField( validators=[MinValueValidator(1), MaxValueValidator(50)]) 
    carryOver_level = models.PositiveIntegerField( validators=[MinValueValidator(100), MaxValueValidator(500)])
    current_level =models.PositiveIntegerField( validators=[MinValueValidator(100), MaxValueValidator(500)])
    def __str__(self):
        return str(self.course) 


class hold_class(models.Model):
    course = models.ForeignKey(course, on_delete=models.CASCADE) #fetches courses and their lecturers from department
    lecturer = models.ForeignKey(lecturer, on_delete=models.CASCADE)
    # time = models.TimeField(blank=True, null=True) #assign to schedule randomly
    # room = models.ForeignKey(room, on_delete=models.CASCADE, blank=True, null=True ) #assign to schedule randomly
    def __str__(self):
        return (str(self.course) + ", "+  str(self.lecturer))

    