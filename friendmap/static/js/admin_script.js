function retrieve_friends(){
    get_friends(function(data){
        friend_data.users = $.parseJSON(data);
        console.log(friend_data.users);
        update_graph();
    });
}

function get_friends(call_back) {
    $.get(
        "all_connections",
        {},
        call_back).fail(function(){
        });
}

function make_graph(){
    var container = document.getElementById('graph');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {};
    var network = new vis.Network(container, data, options);
}

function update_graph(){
    var new_nodes = [];
    var new_edges = [];
    for(var i = 0; i < friend_data.users.length; i++){
        var friend_obj = friend_data.users[i];
        var username = friend_obj.username;
        new_nodes.push({
            id: username,
            label: username
        });
        node_ids.push(username);
        for (var x = 0; x < friend_obj.friends.length; x++){
            var friend = friend_obj.friends[x];
            if(node_ids.indexOf(friend) < 0) {
                new_edges.push({
                    from: username,
                    to: friend
                });
            }
        }
    }
    nodes.add(new_nodes);
    edges.add(new_edges);
}

var nodes = new vis.DataSet();
var edges = new vis.DataSet();
var node_ids = [];
var friend_data = {};

$(document).ready(function () {

    retrieve_friends();
    make_graph()

});


