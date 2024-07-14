
var last_update = 0; //Idk yet

function UpdateCpu(){
    $.get("/dashboard/endpoint/cpu_usage/" , (data)=>{
        $("#cpuUsage").text(`${data.cpu_usage}`);
    });
}
function UpdateMemory(){
    $.get("/dashboard/endpoint/mem_usage/", (data)=>{
        $("#memoryUsage").text(`${data.memory_usage}`)
    });
}
function UpdateDockerContainers(){
    $.get("/dashboard/endpoint/docker_ps/" , (data)=>{
        var table = $("#dockerContainerTable");
        table.empty();
        for(var i = 0; i<data.containers.length; i++){
            var container = data.containers[i];
            table.append('<tr>' +
            '<td>' + container.ID + '</td>' +
            '<td>' + container.Image + '</td>' +
            '<td>' + container.Command + '</td>' +
            '<td>' + container.CreatedAt + '</td>' +
            '<td>' + container.Status + '</td>' +
            '<td>' + container.Ports + '</td>' +
            '<td>' + container.Names + '</td>' +
            '</tr>');
        }
    });
}
//To Be implemented later
function UpdateSshInfo(){
}
function UpdateProcList(){
    $.get("/dashboard/endpoint/proc_list/" , (data)=>{
        var table = $("#procListTable");
        table.empty();
        for(var i= 0; i<data.process_list; i++){
            var proc = data.process_list[i];
            table.append(`<tr><td>${proc.pid}</td><td>${proc.command}</td></tr>`);
        }
    });
}
function UpdateDashboard(){
    UpdateCpu();
    UpdateMemory();
}