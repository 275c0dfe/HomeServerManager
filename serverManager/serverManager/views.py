from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


def index(request):
    return redirect("dashboard:index")