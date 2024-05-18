
#Dev imports
import json
from .pycode import connPOO
from .pycode import people
from .pycode import parks
from .pycode import streets
from .pycode.libs import general


#Django imports
from django.views import View
from django.http import JsonResponse
#from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth import logout
#from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
#from django.views.decorators.csrf import csrf_exempt
#from django.utils.decorators import method_decorator


class HelloWord(View):
    def get(self, request):
        return JsonResponse({"ok":True, "message": "Hello world", "data":[] })



class Parks(View):
    #Select by gid
    def get(self, request):
        #conection
        conn=connPOO.Conn()
        b=parks.Parks(conn)

        if request.GET.get('gid'):
            gid = request.GET['gid']
            r=b.select(gid)
        else:
            r=b.select()
        return JsonResponse(r)


class ProtectedParks(LoginRequiredMixin, View):
    #Insert, Update and Delete
    def post(self, request):
        #conection
        conn=connPOO.Conn()
        b=parks.Parks(conn)

        
        #action = request.POST['action']
        d=general.getPostFormData(request)
        action=d['action']
        #Insert
        if action == 'insert':
            #data to insert
            #nombre = request.POST['nombre']
            #descripcion = request.POST['descripcion']
            #geometryWkt = request.POST['geomWkt']
            nombre = d['nombre']
            descripcion = d['descripcion']
            geometryWkt = d['geomWkt']
            
            data = {'nombre':nombre, 'descripcion':descripcion, 'geom':geometryWkt}
        
            r = b.insert(data)
            return JsonResponse(r)

        #Update
        if action == 'update':
            #data to update
            #gid = request.POST['gid']
            #nombre = request.POST['nombre']
            #descripcion = request.POST['descripcion']
            #geometryWkt = request.POST['geomWkt']
            gid = d['gid']
            nombre = d['nombre']
            descripcion = d['descripcion']
            geometryWkt = d['geomWkt']
            data = {'gid':gid, 'nombre':nombre, 'descripcion':descripcion, 'geom':geometryWkt}
        
            r = b.update(data)
            return JsonResponse(r)
        
        #Delete by gid
        if action == 'delete':
            #gid=request.POST['gid']
            gid=d['gid']
            r=b.delete(gid)
            return JsonResponse(r)





class Streets(View):
    
    #Select by gid
    def get(self, request):
        #conection
        conn=connPOO.Conn()
        b=streets.Streets(conn)

        if request.GET.get('gid'):
            gid = request.GET['gid']
            r=b.select(gid)
        else:
            r=b.select()
        return JsonResponse(r)

class ProtectedStreets(LoginRequiredMixin, View):
    #Insert, Update and Delete
    def post(self, request):
        #conection
        conn=connPOO.Conn()
        b=streets.Streets(conn)

        #action = request.POST['action']
        d=general.getPostFormData(request)
        action=d['action']
        
        #Insert
        if action == 'insert':
            #data to insert
            #nombre = request.POST['nombre']
            #tipo = request.POST['tipo']
            #ncarril = request.POST['ncarril']
            #geometryWkt = request.POST['geomWkt']
            nombre = d['nombre']
            tipo = d['tipo']
            ncarril = d['ncarril']
            geometryWkt = d['geomWkt']
            data = {'nombre':nombre, 'tipo':tipo, 'ncarril':ncarril, 'geom':geometryWkt}
        
            r = b.insert(data)
            return JsonResponse(r)

        #Update
        if action == 'update':
            #data to update
            #gid = request.POST['gid']
            #nombre = request.POST['nombre']
            #tipo = request.POST['tipo']
            #ncarril = request.POST['ncarril']
            #geometryWkt = request.POST['geomWkt']
            gid = d['gid']
            nombre = d['nombre']
            tipo = d['tipo']
            ncarril = d['ncarril']
            geometryWkt = d['geomWkt']
            data = {'gid':gid, 'nombre':nombre, 'tipo':tipo, 'ncarril':ncarril, 'geom':geometryWkt}
        
            r = b.update(data)
            return JsonResponse(r)
        
        #Delete by gid
        if action == 'delete':
            #gid=request.POST['gid']
            gid=d['gid']
            r=b.delete(gid)
            return JsonResponse(r)




class People(View):
    
    #Select by dni
    def get(self, request):
        #conection
        conn=connPOO.Conn()
        b=people.People(conn)
        
        if request.GET.get('dni'):
            dni = request.GET['dni']
            r=b.select(dni)
        else:
            r=b.select()
        return JsonResponse(r)
        

class ProtectedPeople(LoginRequiredMixin, View): 
    #Insert, Update and Delete
    def post(self, request):
        #conection
        conn=connPOO.Conn()
        b=people.People(conn)

        #action = request.POST['action']
        d=general.getPostFormData(request)
        action=d['action']
        
        #Insert
        if action == 'insert':
            #data to insert
            """dni = request.POST['dni']
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            profesion = request.POST['profesion']
            ciudad = request.POST['ciudad']
            """
            dni = d['dni']
            nombre = d['nombre']
            apellido = d['apellido']
            profesion = d['profesion']
            ciudad = d['ciudad']
            
            data = {'dni':dni, 'nombre':nombre, 'apellido':apellido, 'profesion':profesion, 'ciudad':ciudad}
        
            r = b.insert(data)
            return JsonResponse(r)

        #Update
        if action == 'update':
            #data to update
            #dni = request.POST['dni']
            #nombre = request.POST['nombre']
            #apellido = request.POST['apellido']
            #profesion = request.POST['profesion']
            #ciudad = request.POST['ciudad']
            dni = d['dni']
            nombre = d['nombre']
            apellido = d['apellido']
            profesion = d['profesion']
            ciudad = d['ciudad']
            data = {'dni':dni, 'nombre':nombre, 'apellido':apellido, 'profesion':profesion, 'ciudad':ciudad}
        
            r = b.update(data)
            return JsonResponse(r)
        
        #Delete by gid
        if action == 'delete':
            #dni=request.POST['dni']
            dni=d['dni']
            r=b.delete(dni)
            return JsonResponse(r)


        



  



