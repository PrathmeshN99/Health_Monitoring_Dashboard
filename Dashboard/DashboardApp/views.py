import profile
from django.shortcuts import render,redirect
import pandas as pd
from django.contrib.auth.models import User, auth
import requests
from DashboardApp.models import Record,Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.contrib.auth import logout
from django.contrib import messages

# Create your views here.
def home(request):
    print(request.session['username'])

    channel_id = str(1726803)

    api_key = str("PGETFAXFNAYC4HR8")

    number_of_results = str(2)

    base_urls = "https://api.thingspeak.com/channels/" + channel_id + "/feeds.json?api_key=" + api_key + "&results=" + number_of_results

    data = requests.get(base_urls).json()

    data_req = data['feeds'] 
    for i in range(len(data_req)):
        Time_stamp = data_req[i]["created_at"]
        User = request.session['username']
        Temperature = data_req[i]['field1']
        Humidity = data_req[i]['field2']
        aqi = data_req[i]['field3']
        Body_Temperature = data_req[i]['field4']
        
        newRecord = Record.objects.create(User=User,Time_stamp=Time_stamp,Temperature=Temperature,Humidity=Humidity,AQI=aqi,Body_Temperature=Body_Temperature)
        newRecord.save()

    time_list = []
    def decimal(x):
        if (type(x)==type("l")): return(float("{0:.2f}".format(float(x))))
        else: return 0
    def func(x):
        obj = str(x.hour) + ":" + str(x.minute) + ":" + str(x.second)
        time_list.append(obj)
    if Record.objects.filter(User=request.session['username']).exists():
        body_temp_list = list(Record.objects.filter(User=request.session['username']).values_list('Body_Temperature',flat=True))
        datetime_queryset = pd.Series(Record.objects.filter(User=request.session['username']).values_list('Time_stamp',flat=True))
        datetime_queryset.apply(func)
        Temperature = decimal(data_req[0]['field1'])
        Humidity = decimal(data_req[0]['field2'])
        aqi = decimal(data_req[0]['field3'])
        Body_Temperature = decimal(data_req[0]['field4'])

        profile_pic_name = Profile.objects.filter(username=request.session['username']).values('profile_pic')[0]['profile_pic']
        age = Profile.objects.filter(username=request.session['username']).values('age')[0]['age']
        height = Profile.objects.filter(username=request.session['username']).values('height')[0]['height']
        sex = Profile.objects.filter(username=request.session['username']).values('sex')[0]['sex'][0]
        weight = Profile.objects.filter(username=request.session['username']).values('weight')[0]['weight']
        blood_group = Profile.objects.filter(username=request.session['username']).values('blood_group')[0]['blood_group']
        bmi = round(weight/(height*height),2)    

        print(time_list)
        print(body_temp_list)
        print(profile_pic_name)
    else:
        print("User with username does not exists")
    context = { "time_list": time_list[1:], "body_temp_list" : body_temp_list,"user":request.session['username'], "Temperature":Temperature, "Humidity":Humidity, "aqi":aqi,"Body_Temperature":Body_Temperature,"profile_pic_name":profile_pic_name,"height":height,"weight":weight,"sex":sex,"blood_group":blood_group,"bmi":bmi,"age":age}

    return render(request,'base2.html',context)

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']   
        last_name = request.POST['last_name']
        user_name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        sex = request.POST['sex']
        age = request.POST['age']
        profile_pic = request.POST['profile_pic']
        weight = request.POST['weight']
        height = request.POST['height']
        blood_group = request.POST['blood_group']
        if User.objects.all().filter(username=user_name).exists():
            print("Username already exists")
            return redirect('/register')

        else:    
            user = User.objects.create_user(username=user_name,first_name=first_name,last_name=last_name,email=email,password=password)
            user.save()
            user = User.objects.get(username=user_name)
            profile = Profile(user=user,profile_pic=profile_pic,sex=sex,age=age,height=height,weight=weight,blood_group=blood_group,username=user_name)

            profile.save()
            print("Created user " + user_name)
            return redirect('/')
    else:
        return render(request,'register2.html')
 
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        print("user : ")
        print(user)
        
        if user is not None:
            auth.login(request,user)
            print("logged in")
            # return render(request,'home.html')
            request.session['username']=username
            return redirect('/home')
        else:

            print("Please enter correct credentials")
            return redirect('/')
    else:
        return render(request,'login.html')

@login_required
def editProfile(request):
    print(request.session['username'])
    if request.method == 'POST':
        first_name = request.POST['first_name']   
        last_name = request.POST['last_name']
        user_name = request.session['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.all().filter(username=user_name).exists():
            user = User.objects.get(username=user_name)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.password = password 
            user.save()
            return redirect('home')       
    else:
        return render(request,'editProfile.html')

def logout_view(request):
    logout(request)
    messages.success(request,'Logged out')
    return redirect('/')

def about(request):
    return render(request,'about.html')

        