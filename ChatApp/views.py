from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import os
import pandas as pd
from django import template
from django.views.decorators.csrf import csrf_exempt
from ChatApp.train_model import predict



#import json
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/saturn/Downloads/SAPbot-d3843c6f611b.json"


#
@csrf_exempt
def chat(request):
    if request.is_ajax():
        print("ajax")
    if request.method== 'POST':
        text= request.POST.get('msgbox')
        print(text)
        AutoMessage= predict(text)
        if isinstance(AutoMessage,str):
            message= AutoMessage
            print(message)
            return JsonResponse({'msg': text,'rep':message})
        else:
            message1= AutoMessage[0]
            message2= AutoMessage[1]
            #message.append(auto for auto in AutoMessage)
            return JsonResponse({'msg': text,'rep':message1,'rep2':message2})
    else:
        print("is GET")
   # if request.method == 'POST':
        return render(request, 'chat.html', {'response': 'text'})
   


@csrf_exempt  
def login(request):
    if request.method=='POST':
        username= request.POST['username']
        password= request.POST['password']
        if (username=='chatbotAI' and password=='chatbotAI'):
            return render(request,'chat.html')
        else:
            return render(request,'login.html')
    else:
        return render(request,'login.html')
    
    

