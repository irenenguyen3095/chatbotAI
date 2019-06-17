from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import dialogflow_v2 as dialogflow
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
        if (username=='irene' and password=='irene'):
            return render(request,'chat.html')
        else:
            return render(request,'login.html')
    else:
        return render(request,'login.html')
    
    


def detect_intent_texts(text):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    project_id= 'sapbot-fef1a'
    session_id='abc'
    language_code='de'
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    #text= 'Hallo'
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

       # print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print(response)
    print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))
    return response.query_result.fulfillment_text
