from django.shortcuts import render
from django.http import HttpResponse
from .models import Pages
from sqlite3 import OperationalError
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.contrib.auth.views import logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

# Create your views here.
formulario = """
        <form action="" method="POST">
          <h3>PAGE:</h3>
          <input type="text" name="PAGE" value="http://"><br>
          <input type="submit" value="Enviar">
        </form>
        """

def mylogout(request):
    logout(request)
    return redirect(barra)

def namePage(page):
    if page.startswith('http://') or page.startswith('https://'):
        return page
    else:
        return('http://' + page)


def numberOption(request, recurso):
    if request.method == 'GET':
        try:
            objeto = Pages.objects.get(id = int(recurso))
            return HttpResponseRedirect(objeto.name)
        except Pages.DoesNotExist:
            return HttpResponse("No encontrado", status=404)
        

@csrf_exempt
def barra(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            sesion = '<li><a href="/logout">Logout</a>'
        else:
            sesion = '<li><a href="/login">Login</a>'
        list = Pages.objects.all()
        resp = "<h3>LISTA DE PÁGINAS INCLUIDAS: </h3><ul>"
        try:
            for objeto in list:
                resp += '<li><a href="/' + str(objeto.id) + '">' + objeto.name + '</a>'
            resp += "</ul>"
        except OperationalError:
            resp = "No hay nada en la lista."

        return HttpResponse(sesion + formulario + resp)
    
    elif request.method == 'POST':
        if request.user.is_authenticated():
            page = Pages(name=namePage(request.POST['PAGE']))
            try:
                page.save()
                return HttpResponseRedirect(page.name)
            except IntegrityError:
                return HttpResponse("Página ya añadida en la lista anteriormente.")
        else:
            resp = '<li><a href="/login">Login</a>'
            return HttpResponse("No ha iniciado sesión." + resp)

def notOption(request, recurso):
    return HttpResponse("No contemplada esta opción.")
