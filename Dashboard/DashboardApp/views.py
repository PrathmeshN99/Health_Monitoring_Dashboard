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


def home(request):  

    request.session['username'] = request.user.username
    channel_id = str(1771248)

    api_key = str("2WZQATARKYJ5L58N")

    number_of_results = str(1)

    base_urls = "https://api.thingspeak.com/channels/" + channel_id + "/feeds.json?api_key=" + api_key + "&results=" + number_of_results

    data = requests.get(base_urls).json()

            
    data_req = data['feeds'] 
    for i in range(len(data_req)):
        Time_stamp = data_req[i]["created_at"]
        User = request.session['username']
        if (data_req[i]['field1']) is None: 
            Humidity = Record.objects.filter(Humidity__isnull = False).values('Humidity')[0]['Humidity']
            # Humidity = Record.objects.filter(Humidity__isnull = False)
        else: Humidity = data_req[i]['field1']

        if (data_req[i]['field2']) is None: 
            Temperature = Record.objects.filter(Temperature__isnull = False).values('Temperature')[0]['Temperature']
            # Humidity = Record.objects.filter(Humidity__isnull = False)
        else: Temperature = data_req[i]['field2']

        if (data_req[i]['field3']) is None: 
            aqi = Record.objects.filter(AQI__isnull = False).values('AQI')[0]['AQI']
            # Humidity = Record.objects.filter(Humidity__isnull = False)
        else: aqi = data_req[i]['field3']

        if (data_req[i]['field4']) is None: 
            Body_Temperature = Record.objects.filter(Body_Temperature__isnull = False).values('Body_Temperature')[0]['Body_Temperature']
            # Humidity = Record.objects.filter(Humidity__isnull = False)
        else: Body_Temperature = data_req[i]['field4']
        
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
        aqi_list = list(Record.objects.filter(User=request.session['username']).values_list('AQI',flat=True))
        datetime_queryset = pd.Series(Record.objects.filter(User=request.session['username']).values_list('Time_stamp',flat=True))
        datetime_queryset.apply(func)
        Temperature = decimal(data_req[0]['field2'])
        Humidity = decimal(data_req[0]['field1'])
        aqi = decimal(data_req[0]['field3'])
        Body_Temperature = decimal(data_req[0]['field4'])
        
        if(Profile.objects.filter(username=request.session['username']).exists()):
            profile_pic_name = Profile.objects.filter(username=request.session['username']).values('profile_pic')[0]['profile_pic']
            age = Profile.objects.filter(username=request.session['username']).values('age')[0]['age']
            height = Profile.objects.filter(username=request.session['username']).values('height')[0]['height']
            sex = Profile.objects.filter(username=request.session['username']).values('sex')[0]['sex'][0]
            weight = Profile.objects.filter(username=request.session['username']).values('weight')[0]['weight']
            blood_group = Profile.objects.filter(username=request.session['username']).values('blood_group')[0]['blood_group']
            bmi = (round(weight/(height*height*0.01*0.01),2))

        else: 
            profile_pic_name = 'Not provided' 
            age = 0
            height = 0
            sex = 'Not provided'
            weight = 0
            blood_group = 'Not provided'
            bmi = 0

        print(time_list)
        print(body_temp_list)
        print(profile_pic_name)
    else:
        print("User with username does not exists")
    context = { "time_list": time_list[1:], "body_temp_list" : body_temp_list,"aqi_list":aqi_list,"user":request.session['username'], "Temperature":Temperature, "Humidity":Humidity, "aqi":aqi,"Body_Temperature":Body_Temperature,"profile_pic_name":"AB.jpg","height":height,"weight":weight,"sex":sex,"blood_group":blood_group,"bmi":bmi,"age":age}

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
        return render(request,'register.html')
 
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
        return render(request,'login2.html')

@login_required
def editProfile(request):
    print(request.session['username'])
    if request.method == 'POST':
        first_name = request.POST['first_name']   
        last_name = request.POST['last_name']
        user_name = request.session['username']
        email = request.POST['email']
        password = request.POST['password']
        age = request.POST['age']
        weight = request.POST['weight']
        height = request.POST['height']

        if User.objects.all().filter(username=user_name).exists():
            user = User.objects.get(username=user_name)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.password = password 
            user.save()
            if Profile.objects.all().filter(username=user_name).exists():
                profile = Profile.objects.get(username=user_name)
                profile.first_name = first_name
                profile.last_name = last_name
                profile.email = email
                profile.password = password 
                profile.weight = weight
                profile.height = height
                profile.age = age
                profile.save()
            return redirect('home')       
    else:
        return render(request,'editProfile2.html')

def logout_view(request):
    logout(request)
    messages.success(request,'Logged out')
    return redirect('/')

def about(request):
    return render(request,'about.html')

        