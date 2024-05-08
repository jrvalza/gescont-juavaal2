
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import logout

from .pycode import users

def notLoggedIn(request):
    return JsonResponse({"ok": False,
                        "message": "You are not logged in",
                        "data": []
                        })


class AppLogin(View):
    def post(self, request):
        r=users.appLogin(request)
        return JsonResponse(r)


class AppLogout(View):
    def get(self, request):
        if request.user.is_authenticated:
            username=request.user.username
            logout(request) #removes from the header of the request the user data, stored in a cookie
            return JsonResponse({"ok":True,
                                "message": "The user {0} is now logged out".format(username),
                                "data":[]
                                })
        
        else:
            return JsonResponse({"ok":False,
                                "message": "You where  not logged in",
                                "data":[]
                                })

