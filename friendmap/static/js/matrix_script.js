$(document).ready(function () {


    var matrix = $("#matrix")
    var matrix_store = new Array();
    for(var i = 0; i < 21; i++){
        var row = $("<div class=\"row\"></div>");
        var row_store = new Array();
        for (var j = 0; j < 3; j++){
            var cell = $("<div id=\"cell-"+i+","+j+"\"class=\"col-xs-1\"></div>").text("cell");
            row_store.push(cell);
            row.append(cell);
        }
        matrix_store.push(row_store);
        matrix.append(row);
    }
    //do without matrix store, use jquery
    refresh_matrix(matrix_store);

});


function refresh_matrix(matrix_store) {
    var type = $('#matrix_type').val();
    get_costs(type, function (data) {
        var data_json = $.parseJSON(data);
        add_to_grid(data_json, matrix_store)
    });
}

function get_costs(type, call_back) {
    $.get(
        "surveys/cost_matrix/"+type,
        {},
        call_back
    );
}

function add_to_grid(matrix, matrix_store){
    for(var i = 0; i < 21; i++){
        for (var j = 0; j < 3; j++){
            var cell = matrix_store[i][j];
            cell.text(matrix[i][j])
        }
    }
}