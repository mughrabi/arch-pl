$(document).ready(function() {
    var tr_odd_selected_background = "#E9FFB8";
    var tr_even_selected_background = "#E4FFA8";

    $("tbody tr:odd").css("background", "#F5F8EF");

    $("tbody tr:odd").mouseover(function() {
        // bad global variable
        _tr_odd_background = $(this).css("background");
        $(this).css("background", tr_odd_selected_background);
    }).mouseout(function() {
        $(this).css("background", _tr_odd_background);
    });
    $("tbody tr:even").mouseover(function() {
        // bad global variable
        _tr_even_background = $(this).css("background");
        $(this).css("background", tr_even_selected_background);
    }).mouseout(function() {
        $(this).css("background", _tr_even_background);
    });
})
