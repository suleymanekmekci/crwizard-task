from django.shortcuts import render
from asgiref.sync import sync_to_async
from .tasks import xml_function
import time
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url="/accounts/google/login")
def addXml(request):
    

    if request.GET.get("xmlurl") and request.GET.get("oldword") and request.GET.get("newword"):

        xmlurl = request.GET.get("xmlurl")

        oldword = request.GET.get("oldword")
        newword = request.GET.get("newword")

        # delay makes function async
        items = xml_function.delay(xmlurl,oldword,newword,request.user.email)

        if not items:
            messages.info(request,"Error occured!")
        else:
            messages.success(request, "Successfully downloaded")


    

    return render(request, "addxml.html")
