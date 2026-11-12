
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
        console.log(data);
        for(var i = 0; i<data.containers.length; i++){
            var container = data.containers[i];
            table.append('<tr>' +
            '<td>' + container.ID + '</td>' +
            '<td>' + container.Image + '</td>' +
            '<td>' + container.Status + '</td>' +
            '<td>' + container.Command + '</td>' +
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
        for(var i= 0; i<data.process_list.length; i++){
            var proc = data.process_list[i];
            table.append(`<tr><td>${proc.pid}</td><td class="wrap-text">${proc.command}</td></tr>`);
        }
    });
}
function SetGameServerStatus(message, isError){
    var status = $("#gameServerStatus");
    status.text(message);
    status.toggleClass("text-danger", isError);
    status.toggleClass("text-success", !isError);
}
function GameServerRequest(url, data){
    return $.ajax({
        url: url,
        method: "POST",
        data: $.extend({
            "csrfmiddlewaretoken": $("#gameServerControls input[name=csrfmiddlewaretoken]").val()
        }, data || {})
    });
}
function InitializeGameServerControls(){
    $("#startGameServer").click(function(){
        GameServerRequest("/dashboard/endpoint/game_server/start/")
            .done(function(){ SetGameServerStatus("Game server started.", false); })
            .fail(function(xhr){ SetGameServerStatus("Unable to start game server: " + xhr.responseText, true); });
    });
    $("#stopGameServer").click(function(){
        GameServerRequest("/dashboard/endpoint/game_server/stop/")
            .done(function(){ SetGameServerStatus("Game server stopped.", false); })
            .fail(function(xhr){ SetGameServerStatus("Unable to stop game server: " + xhr.responseText, true); });
    });
    $("#readGameServerOutput").click(function(){
        GameServerRequest("/dashboard/endpoint/game_server/output/")
            .done(function(data){
                $("#gameServerOutput").text(data.cmd_result || "");
                $("#gameServerOutput").scrollTop($("#gameServerOutput")[0].scrollHeight);
                SetGameServerStatus("Game server output updated.", false);
            })
            .fail(function(xhr){
                SetGameServerStatus("Unable to read game server output: " + xhr.responseText, true);
            });
    });
    $("#sendGameServerCommand").click(function(){
        var command = $("#gameServerCommand").val().trim();
        if(!command){
            SetGameServerStatus("Enter a command first.", true);
            return;
        }
        GameServerRequest("/dashboard/endpoint/game_server/command/", {"command": command})
            .done(function(){
                SetGameServerStatus("Command sent.", false);
                $("#gameServerCommand").val("");
            })
            .fail(function(xhr){ SetGameServerStatus("Unable to send command: " + xhr.responseText, true); });
    });
    $("#gameServerCommand").keypress(function(event){
        if(event.which === 13){
            event.preventDefault();
            $("#sendGameServerCommand").click();
        }
    });
}
function UpdateDashboard(){
    UpdateCpu();
    UpdateMemory();
}