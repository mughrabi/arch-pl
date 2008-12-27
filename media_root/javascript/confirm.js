$(document).ready(function() {
    $(".confirm").each(function() {
        $(this).click( function() {
            if (confirm("Usunąć?"))
                return true;
            return false;
        });
    });


});
