from django.shortcuts import render
from django.http import HttpResponse

def home():
    return HttpResponse("Bienvenido al sistema LOGIVAG")
