from django.contrib import admin
from django.urls import path , include
from . import views


app_name = "dashboard"

urlpatterns = [
    #Pages
    path("" , views.dashboard_page , name="index"),
    path("shell/" , views.shell_page , name="shell"),
    path("network/" , views.network_page, name="network"),
    
    #Auth
    path("login/" , views.login_view , name="login"),
    path("logout/" , views.logout_view , name="logout"),

    #Api
    path("endpoint/cpu_usage/" , views.get_cpu_usage),
    path("endpoint/mem_usage/" , views.get_mem_usage),
    path("endpoint/docker_ps/" , views.get_docker_ps),
    path("shell/exec/" , views.execute_shell_command),
    path("endpoint/game_server/start/" , views.start_hl_server),
    path("endpoint/game_server/stop/" , views.stop_hl_server),
    path("endpoint/game_server/command/" , views.exec_hl_server),
    path("endpoint/game_server/output/", views.get_hl_server_output),
    path("endpoint/ssh_info/" , views.get_ssh_info),
    path("endpoint/open_ports/" , views.get_open_ports),
    path("endpoint/proc_list/" , views.get_proc_list),
]