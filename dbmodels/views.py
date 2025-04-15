from django.shortcuts import render
from django.http import HttpResponse

# NOSONAR: Ignora el warning de parámetro innecesario
def home(request):
    return HttpResponse("Bienvenido al sistema LOGIVAG")
