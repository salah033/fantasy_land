from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .utils import get_response


@login_required
def chatbot (request) : 

    if request.method == 'POST' :
        qst = request.POST.get('message')
        print (qst)
        #data = {"data" : "hello"}
        bot_responce = get_response(qst)
        return JsonResponse({'response': bot_responce})
    return render (request, "chatbot/chat_bot.html")

