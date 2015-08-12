function retrieve_data() {
    var username = $('#username').val();
    if (username != '') {
        get_users(username, function (data) {
            results.users = $.parseJSON(data).filter(function(user){
                return user !== my_username && node_ids.indexOf(user) < 0;
            });
        });
    }
    else {
        results.users = [];
    }
}

function retrieve_friends(){
    get_friends(function(data){
        friend_data.usernames = $.parseJSON(data);
        update_graph();
    });
}

function add_friend(name) {
    var index = results.users.indexOf(name);
    results.users.splice(index, 1);
    var data = {
        username: name
    };
    $.ajax({
        type: "POST",
        url: "/friend/",
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (response) {
            retrieve_friends();
        }
    });
}

function get_users(username, call_back) {
    $.get(
        "user",
        {username: username},
        call_back);
}

function get_my_username(call_back){
    $.get(
        "whoami",
        {},
        call_back);
}

function get_friends(call_back) {
    $.get(
        "friend",
        {},
        call_back).fail(function(){
            window.location.replace("/login_form");
        });
}

function add_friend_click(el){
    add_friend(el.innerText);
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
    for(var i = 0; i < friend_data.usernames.length; i++){
        var friend = friend_data.usernames[i];
        if(node_ids.indexOf(friend) < 0) {
            nodes.add({
                id: friend,
                label: friend
            });
            edges.add({
                from: 'me',
                to: friend
            });
            node_ids.push(friend);
        }

    }
}

var nodes = new vis.DataSet([{
        id: 'me',
        label: 'me'
    }]);
var edges = new vis.DataSet();
var node_ids = [];
var results = {};
var friend_data = {};
var my_username = '';

$(document).ready(function () {

    get_my_username(function(data){
        my_username = $.parseJSON(data);
        $('#my_username')[0].innerText += " "+my_username;
    });


    rivets.configure({
        adapter: {
            observe: function (obj, keypath, callback) {
                watch(obj, keypath, callback)
            },
            unobserve: function (obj, keypath, callback) {
                unwatch(obj, keypath, callback)
            },
            get: function (obj, keypath) {
                return obj[keypath]
            },
            set: function (obj, keypath, value) {
                obj[keypath] = value
            }
        }
    });


    rivets.bind(
        $('#results'),
        {
            results: results
        }
    );


    watch(results, 'names', function () {});
    watch(friend_data, 'username', function () {});

    $('#username').on('input', retrieve_data);


    retrieve_friends();
    make_graph()

});


