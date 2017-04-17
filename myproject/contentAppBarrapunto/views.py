from django.shortcuts import render
from django.http import HttpResponse
from contentAppBarrapunto.models import Pages
from django.views.decorators.csrf import csrf_exempt
from updateBarrapunto import update

# Create your views here.

cont_rss = ""
cont_total = ""

def showAll(request):
    lista = Pages.objects.all()
    respuesta = "<h2>BASE DE DATOS</h2>"
    idAux = 1
    #lo imprimimos con forma de lista con <li>
    if len(lista) != 0:
        lista_pags = Pages.objects.all()
        for pag in lista_pags:
            respuesta+="<h4><li>Id: " + str(idAux) + " | " + pag.name + " : " + pag.page + "</li></h4>"
            idAux += 1
    else :
        respuesta = "La base de datos esta vacia."
    return HttpResponse(respuesta)
    
def updateCont(request):
    global cont_rss
    cont_rss = update() #cont_rss = list con todos los links de barrapunto actual
    respuesta = "<html><body><h2>Barrapunto actualizado.</h2><ul>" + showCont() + "</ul></body></html>"
    return HttpResponse(respuesta)

def showCont():
    global cont_total
    cont_total = ""
    for pages in cont_rss:
        cont_total += pages
    return cont_total

@csrf_exempt
def processRequest(request,name):
    global cont_total
    if request.method == "GET":
        try:
            page = Pages.objects.get(name=name)
            respuesta = "Has elegido " + page.name + ". Su pagina es: " + page.page + ". Su id es: " + str(page.id)
            respuesta = "<div><h2>Pagina principal</h2><h3>" + respuesta + "</h3><div>"
            if cont_total == "" :
                respuesta += "Si quieres ver los links de Barrapunto actualiza con /update por favor."
            else:
                respuesta += "<div><h2>Links de Barrapunto:</h2><ul>" + showCont() + "</ul></div>"
        except Pages.DoesNotExist:
            respuesta = "No existe pagina con el nombre " + name + "."
    elif request.method == "PUT":
        try:
            pagina = Pages.objects.get(name=name)
            respuesta = "Ya existe una pagina con ese nombre"
        except Pages.DoesNotExist:
            pagina = request.body
            pagina = Pages(name=name, page=pagina)
            pagina.save()
            respuesta = "Se ha guardado la pagina: " + name \
                        + ". Se ha guardado con identificador " + str(pagina.id)
    else :
        respuesta = "Method not Allowed"

    respuesta = "<html><body>" + respuesta + "</body></html>"
    return HttpResponse(respuesta)
