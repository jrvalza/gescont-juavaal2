
import json
from django.contrib.auth.models import User

def getUserGroups(user: User):
    """
    Gets a lists with the user groups that the user belongs. The
    user is an object of the
    django.contrib.auth.models.User class
    """
    l = user.groups.values_list('name',flat = True) # QuerySet Object
    return list(l)

def getUserGroups_fromUsername(username):
    """
    Gets a lists with the user groups that the user belongs. The
    username is the username,
    usually an email
    """
    user=User.objects.get(username=username)
    return getUserGroups(user)

def getPostFormData(request):
    l=list(request.POST.values())
    if len(l)==0:
        return json.loads(request.body.decode())
    else:
        return request.POST

"""
def getGetFormData(request):
    l=list(request.GET.values())
    if len(l) ==0:
        return json.loads(request.body.decode())
    else:
        return request.GET

"""