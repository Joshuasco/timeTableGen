from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView
from .models import room, lecturer, course, department, faculty, hold_class, carryOver
from json import dumps
import random
from random import seed

#call objects of the model classes
rooms = room.objects.all()
lectrers = lecturer.objects.all()
courses=course.objects.all()
departments =department.objects.all() 
facultys=faculty.objects.all()
classes= hold_class.objects.all()
carryOvers = carryOver.objects.all();
#initialize conflicts_no
conflicts_no = 0

# Create your views here.
def forms(request):
    return render(request, 'time_table.html')
class room(CreateView):
    model = room
    fields="__all__" 
    template_name= "time_table.html"
    def get_success_url(self):
        messages.info(self.request, "room form submitted successfully")
        return reverse_lazy('room')

class lecturer(CreateView):
    model = lecturer
    fields="__all__" 
    template_name= "time_table.html"
    def get_success_url(self):
        print("print somethings for me to see ______________")
        messages.info(self.request, "lecturer form submitted successfully")
        return reverse_lazy('lecturer')

class course(CreateView):
    model = course
    fields="__all__" 
    template_name= "time_table.html"
    courses = course.objects.all()
 
    def get_success_url(self):
        messages.info(self.request, "course form submitted successfully")
        return reverse_lazy('course')

class carryOver(CreateView):
    model = carryOver
    fields="__all__" 
    template_name= "time_table.html"
    courses = carryOver.objects.all()
 
    def get_success_url(self):
        messages.info(self.request, "carry over form submitted successfully")
        return reverse_lazy('carry_over')

# departmental datas
class department(CreateView):
    model = department
    fields="__all__" 
    template_name= "time_table.html"
    
    def get_success_url(self):
        messages.info(self.request, "department form submitted successfully")
        return reverse_lazy('department')

class faculty(CreateView):
    model = faculty
    fields="__all__" 
    template_name= "time_table.html"
    
    def get_success_url(self):
        messages.info(self.request, "falculty form submitted successfully")
        return reverse_lazy('faculty')


# generates data for each class holding
class hold_class(CreateView):
    model = hold_class
    fields="__all__" 
    template_name= "time_table.html"
    clas = hold_class.objects.all()
   
    def get_success_url(self):
        messages.info(self.request, "hold_class form submitted successfully")
        return reverse_lazy('hold_class')

#schedule time table
def time_table_scheduler(request):
    rooms_len = len(rooms)-1
    classes_len= (len(classes)-1)
    newClasses = []
    get_rand_time=[]
    days ={1:"MON", 2:"TUE", 3:"WED", 4:"THUR", 5:"FRI", 6:"SAT"}
    timing = {
        1:"08-09AM",2:"09-10AM",3:"10-11AM",4:"11-12PM",5:"12-01PM",6:"BREAK",7:"02-03PM",\
        8:"03-04PM",9:"04-05PM",10:"05-06PM"
    }
    timing_len = len(timing)
    days_len = len(days)
    

    for i in range(classes_len+1):
        newClasses.append([])
        rand_room=rooms[random.randint(0, rooms_len)]
        rand_day=days[random.randint(1, days_len)]
        #print("course unit = {} ".format(classes[i].course.unit))

        if classes[i].course.unit == 1 :
            rand_time = random.randint(1, timing_len)
            while (timing.get(rand_time) == "BREAK"):
                rand_time = random.randint(1, timing_len)
                #print("2 timing len={}, key= {}, val = {} ".format(timing_len, rand_time, timing.get(rand_time)))
            get_rand_time=timing[rand_time]

        elif classes[i].course.unit == 2 :
            rand_time = random.randint(1, timing_len)
            while ((timing.get(rand_time) == "BREAK") or( (rand_time+1) not in timing)):
                rand_time = random.randint(1, timing_len)
                #print("2 timing len={}, key= {}, val = {} ".format(timing_len, rand_time, timing.get(rand_time)))
            check_val=timing.get(rand_time+1) 
            if  check_val == "BREAK":
                get_rand_time=timing[rand_time]+", "+ timing[rand_time+2]
                get_rand_time=get_rand_time.split(',')
                #print("got time {} = ".format(get_rand_time))
            else:    
                get_rand_time=timing[rand_time]+ ", " +timing[rand_time+1]
                get_rand_time=get_rand_time.split(',')
                #print("got time {} = ".format(get_rand_time))

        elif classes[i].course.unit == 3 :
            rand_time = random.randint(1, timing_len)
            while ((timing.get(rand_time) == "BREAK") or( (rand_time+2) not in timing)):
                rand_time = random.randint(1, timing_len)
                #print("2 timing len={}, key= {}, val = {} ".format(timing_len, rand_time, timing.get(rand_time)))
            check_val=timing.get(rand_time+1)
            check_val1=timing.get(rand_time+2) 
            if  check_val == "BREAK":
                get_rand_time=timing[rand_time]+","+ timing[rand_time+2]+","+timing[rand_time+3]
                get_rand_time = get_rand_time.split(",")
                #print("got time {} = ".format(get_rand_time))
            elif check_val1=="BREAK":
                get_rand_time=timing[rand_time]+ ","+ timing[rand_time+1]+", "+timing[rand_time+3]
                get_rand_time = get_rand_time.split(",")
                #print("got time {} = ".format(get_rand_time))
            else:    
                get_rand_time=timing[rand_time] + ","+timing[rand_time+1]+ ","+timing[rand_time+2]
                get_rand_time = get_rand_time.split(",")
                #print("got time {} = ".format(get_rand_time))

        schedule_class=[rand_day, get_rand_time, classes[i], rand_room]
        newClasses[i].extend(schedule_class)

    #conflict checker
    for i in range(0,len(newClasses)):
        #increase conflicts_no by 1 if capacity conflicts
        if newClasses[i][2].course.student_no > newClasses[i][3].capcity:
            global conflicts_no
            conflicts_no += 1
   
        for j in range(0, len(newClasses)):
            if j>=i:
                #check if same day exits for different class
                if newClasses[i][0] == newClasses[j][0]:
                    #do this for course unit = 1
                    if newClasses[i][2].course.unit == 1:
                        #check if same 'meetingTime and different class object i.e dempartment(using the class id)' of a class exists for another class;
                        if newClasses[i][1] in newClasses[j][1] and newClasses[i][2].course.code[:2] != newClasses[j][2].course.code[:2] :
                            #check if same room or venue
                            if newClasses[i][3] == newClasses[j][3]:
                                #icreament conflicts_no by 1
                                conflicts_no += 1
                            #if same lecturer at same time and different venue, increment conflicts_no by 1
                            if newClasses[i][2].lecturer == newClasses[j][2].lecturer:
                                conflicts_no += 1
                    #check conflict for 2 unit coourses
                    elif  newClasses[i][2].course.unit == 2:
                        #check if same 'meetingTime and different class object i.e dempartment(using the class id)' of a class exists for another class;
                        if (newClasses[i][1][0] in newClasses[j][1] or newClasses[i][1][1] in newClasses[j][1]) and newClasses[i][2].course.code[:2] != newClasses[j][2].course.code[:2] :
                            #check if same room or venue
                            if newClasses[i][3] == newClasses[j][3]:
                                #icreament conflicts_no by 1
                                conflicts_no += 1
                            #if same lecturer at same time and different venue, increment conflicts_no by 1
                            if newClasses[i][2].lecturer == newClasses[j][2].lecturer:
                                conflicts_no += 1
                    #check conflict for 3 unit coourses
                    elif newClasses[i][2].course.unit == 3:
                        #check if same 'meetingTime and different class object i.e dempartment(using the class id)' of a class exists for another class;
                        if (newClasses[i][1][0] in newClasses[j][1] or newClasses[i][1][1] in newClasses[j][1] or newClasses[i][1][2] in newClasses[j][1]) and newClasses[i][2].course.code[:2] != newClasses[j][2].course.code[:2] :
                            #check if same room or venue
                            if newClasses[i][3] == newClasses[j][3]:
                                #icreament conflicts_no by 1
                                conflicts_no += 1
                            #if same lecturer at same time and different venue, increment conflicts_no by 1
                            if newClasses[i][2].lecturer == newClasses[j][2].lecturer:
                                conflicts_no += 1
                    #raise error for courses above 3 unit
                    else:
                        messages.info(request, "can't handle courses above 3 units")
                        print(" can't handle unit above 3 as it is not accepted")
                
# template context datas
    context = {
        'classes':newClasses,
        "days": days,
        "times":timing,
        "rooms": rooms,
        "room_len": len(rooms)+1,
    }
    return context

def generate(request):
    #call time_table_scheduler func
    context=time_table_scheduler(request)
    global conflicts_no
    #initialize count to get number of times time table was reschedule for conflict free
    count=0

    #call time_table_scheduler to reschedule time table  if conflict 
    while conflicts_no != 0 :
        print("--------------------CONFLICT NO = {}".format(conflicts_no))
        conflicts_no = 0
        context= time_table_scheduler(request)
        count += 1
    

    print("generated result at '''' {} '''' ops".format(count))
    print("--------------------CONFLICT NO = {} ----------------------------".format(conflicts_no))

    print(" ---------- Generated timetable datas -----------------")
    print(context)
     
    return render(request, 'gen_table.html', context)

    

    