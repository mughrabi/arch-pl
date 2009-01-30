$(document).ready(function() {
    // markdown info
    $("#markdown_info").after(
        "<span id=\"markdown_help\"> \
            &bull; <a id=\"markdown_info_more\" href=\"#\">Przykłady użycia</a> \
         </span> \
         <div id=\"markdown_info_text\"> \
                <p><em>emfaza</em> - *emfaza*</p> \
                <p><strong>silna emfaza</strong> - **silna emfaza**</p> \
                <p><code>kod jednolinijkowy</code> - `kod` </p> \
                <p><a href=\"#\">link</a> - [nazwa_linka](adres_linka)</p> \
                <p><em>obrazek</em> - ![nazwa_obrazka](link_obrazka)</p> \
         </div> \
        ");
    $("#markdown_info_text").hide();
    $("#markdown_help").click(function() {
        $("#markdown_info_text").toggle();
        return false;
    });
});
