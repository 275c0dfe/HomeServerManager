from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import requests
from . import models

#backend api
backend_url = "http://localhost:5000"
def backend_get(path):
    res = requests.get(backend_url + path)
    if(res.status_code != 200):
        return None
    return res

#Dashboard
def dashboard_page(request):
    if(not request.user.is_authenticated):
        return redirect("dashboard:login")
    return HttpResponse(render(request , "index.html"))

#Shell Page
def shell_page(request):
    if(not request.user.is_authenticated):
        return redirect("dashboard:login")
    return HttpResponse(render(request , "shell.html"))

#Network Page
def network_page(request):
    if(not request.user.is_authenticated):
        return redirect("dashboard:login")
    context = {"port_list":[]}
    res = backend_get("/open_ports")
    if(res.status_code == 200):
        context["port_list"] = res.json()["portList"]
    return HttpResponse(render(request , "network.html" , context=context))

def login_view(request):
    if(request.method != "POST"):
        return HttpResponse(render(request , "login.html"))
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user == None:
        return HttpResponse(render(request , "login.html" , context={"message":"invalid username or password"}))
    login(request , user)
    return redirect("dashboard:index")

def logout_view(request):
    logout(request)
    return redirect("dashboard:login")

#Data Endpoints
def get_cpu_usage(request):
    res = backend_get("/cpu_usage")
    return HttpResponse(res.content , content_type="application/json")

def get_mem_usage(request):
    res = backend_get("/mem_usage")
    return HttpResponse(res.content , content_type="application/json")

def get_docker_ps(request):
    res = backend_get("/docker_ps")
    return HttpResponse(res.content , content_type="application/json")

def execute_shell_command(request):
    if(request.method != "POST"):
        return redirect("dashboard:index")
    command = request.POST["command"]
    res = requests.post(backend_url + "/shell" , {"command":command})
    return HttpResponse(res.content , content_type="application/json")

def get_ssh_info(request):
    res = backend_get("/ssh_info")
    return HttpResponse(res.content)

def get_open_ports(request):
    res = backend_get("/open_ports")
    return HttpResponse(res.content , content_type="application/json")

def get_proc_list(request):
    res = backend_get("/proc_list")
    return HttpResponse(res.content , content_type="application/json")

