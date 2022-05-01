from turtle import shape
from django.shortcuts import render,redirect
import pandas as pd
from django.contrib.auth.models import User, auth
import requests
from DashboardApp.models import Record
# Create your views here.
def home(request):
    
    channel_id = str(1705656)

    api_key = str("78LTB5JLV25P3OW9")

    number_of_results = str(10)

    base_urls = "https://api.thingspeak.com/channels/" + channel_id + "/feeds.json?api_key=" + api_key + "&results=" + number_of_results

    data = requests.get(base_urls).json()

    data_req = data['feeds']
    for i in range(len(data_req)):
        Time_stamp = data_req[i]["created_at"]
        User = request.session['username']
        Temp = data_req[i]['field1']
        newRecord = Record.objects.create(User=User,Time_stamp=Time_stamp,Temp=Temp)
        newRecord.save()
    # df = pd.DataFrame(data_req)

    # df.tail()

    # df['temperature'] = df['field1']

    # df.drop(['field1'],axis=1)

    # def getTime(x):
    #     return x[11:19]

    # time = df['time']=df['created_at'].apply(getTime).to_list()

    # temp = df['temperature'].to_list()

    # df.to_csv('Data/data.csv',index=False)

    time_list = []

    def func(x):
        obj = str(x.hour) + ":" + str(x.minute) + ":" + str(x.second)
        time_list.append(obj)
    if Record.objects.filter(User=request.session['username']).exists():
        temp_list = list(Record.objects.filter(User=request.session['username']).values_list('Temp',flat=True))
        datetime_queryset = pd.Series(Record.objects.filter(User=request.session['username']).values_list('Time_stamp',flat=True))
        datetime_queryset.apply(func)
        print(time_list)
        print(temp_list)
    else:
        print("User with username does not exists")
    context = { "time": time_list[1:], "temp" : temp_list}

    return render(request,'base.html',context)

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']   
        last_name = request.POST['last_name']
        user_name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.all().filter(username=user_name).exists():
            print("Username already exists")
            return redirect('/register')

        else:    
            user = User.objects.create_user(username=user_name,first_name=first_name,last_name=last_name,email=email,password=password)
            user.save()
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
        return render(request,'login.html')