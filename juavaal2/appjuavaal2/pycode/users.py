
import json
import random, time
from django.contrib.auth.models import User
from .libs import general
from django.contrib.auth import authenticate, login



def appLogin(request):
    #django puts im every request the object ’user’,
    #which is of the class from django.contrib.auth.models.User
    #this object is used to get the user data
    #Las cookies en DJango duran un mes por defecto, pero se pueden configurar a un determinado tiempo o accion
    if request.user.is_authenticated: #aqui saca la cookie del navegador para identificar si esta autenticado
        groups = general.getUserGroups(request.user)
        return {"ok":True,"message": "You where already authenticated", "data":[{"username": request.user.username, 'groups': groups}]}
    
    #to make thinks difficult to hackers, you make a random delay,
    #between 0 and 1 second
    seconds=random.uniform(0, 1)
    time.sleep(seconds)

    #get the form data
    #username=request.POST["username"]
    #password=request.POST["password"]
    
    d = general.getPostFormData(request)
    username=d["username"]
    password=d["password"]

    #If user is not None, the credentials where correct
    user = authenticate(username=username, password=password)

    if user:
        login(request,user)#introduce into the request the user data
        #in order, in the the followoing requests, know the user 
        #is authenticated
        return {"ok":"true","message": "User {0} logged in".format(username), 
                "data":[{"userame": username, 
                         "userGroups":general.getUserGroups(user=request.user)}]}
    else:
        return {"ok":False,"message": "Wrong user or password", "data":[]}


