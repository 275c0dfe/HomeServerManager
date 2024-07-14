import flask
import psutil
import subprocess
import socket
import time
import json


app = flask.Flask(__name__)

@app.route("/" , methods=["GET"])
def index():
    return "<html><body>Home Server Manager Version 0.0.1</body></html"

@app.route("/cpu_usage" , methods=["GET"])
def get_cpu_usage():
    usage = psutil.cpu_percent()
    if(usage == 0.0):
        time.sleep(0.1)
        usage = psutil.cpu_percent()
    return flask.jsonify({"cpu_usage":usage , "cpu_speed":psutil.cpu_freq() , "cpu_times":psutil.cpu_times()}) 

@app.route("/mem_usage" , methods=["GET"])
def get_memory_usage():
    mem_usage = psutil.virtual_memory().percent
    return flask.jsonify({"memory_usage":mem_usage})

@app.route("/docker_ps" , methods=["GET"])
def get_docker_ps():
    result = subprocess.run(["sudo" , "docker" , "ps" , "--format", "json"] , stdout=subprocess.PIPE)
    loaded_containers = []
    if(result.stdout != None):
        containers = result.stdout.decode().split("\n")
        for container_json in containers:
            if container_json != "":
                loaded_containers.append(json.loads(container_json))
        return flask.jsonify({"containers":loaded_containers})
    return flask.jsonify({"error":"command error"})

@app.route("/shell" , methods=["POST"])
def post_shell_command():
    cmd = flask.request.form["command"]
    result = subprocess.run(cmd.split(" ") , stdout=subprocess.PIPE)
    stdout = ""
    if(result.stdout):
        stdout += result.stdout.decode()
    
    if(result.stderr):
        stdout += result.stderr.decode()
    
    return flask.jsonify({"cmd_result":stdout})

@app.route("/ssh_info" , methods=["GET"])
def get_ssh_info():
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    return flask.jsonify({"local_ip":host_ip})

@app.route("/open_ports" , methods=["GET"])
def get_open_ports():
    result = subprocess.run(["sudo" , "ss" , "-tnl"] , stdout=subprocess.PIPE)
    parts = result.stdout.decode().split("\n")
    port_list = []
    for part in parts:
        np = []
        pparts = part.split(" ")
        for pp in pparts:
            if(pp != ""):
                np.append(pp)
        port_list.append(np)
    
    json_port_list = []
    for entry in port_list[1:]:
        if(len(entry) > 4):
            state = entry[0]
            recv = entry[1]
            send = entry[2]
            laddr_port = entry[3]
            raddr_port = entry[4]
            json_port_list.append({"State":state , "recv_q":recv,  "send_q":send , "Laddr_port":laddr_port, "Raddr_port":raddr_port})
    
    return flask.jsonify({"portList":json_port_list})

@app.route("/proc_list" , methods=["GET"])
def get_process_list():
    result = subprocess.run(["ps" , "-eo" , "pid,args"] , stdout=subprocess.PIPE)
    res_text = result.stdout.decode()
    process_list = []
    for line in res_text.split("\n")[1:]:
        if(line != ""):
            proc = line.split(" ")
            pproc = []
            for pp in proc:
                if(pp != ""):
                    pproc.append(pp)
            process_list.append(pproc)
    
    json_proc_list = []
    for proc in process_list:
        pid = int(proc[0])
        command = " ".join(proc[1:])
        json_proc_list.append({"pid":pid, "command":command})
    return flask.jsonify({"process_list":json_proc_list})


if __name__ == "__main__":
    app.run()