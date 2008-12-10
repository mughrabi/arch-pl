$(document).ready(function() {
    // markdown info
    $("#markdown_info").append(
        "<div style=\"text-align: right; margin: 1em;\"> \
            <p><em>(<a id=\"markdown_info_more\" href=\"#\">Przykłady użycia</a>.)</em></p> \
            <div class=\"info\"> \
                <p><em>emfaza</em> - *emfaza*</p> \
                <p><strong>silna emfaza</strong> - **silna emfaza**</p> \
                <p><code>kod jednolinijkowy</code> - `kod` </p> \
                <p><a href=\"#\">link</a> - [nazwa_linka](adres_linka)</p> \
                <p><em>obrazek</em> - ![nazwa_obrazka](link_obrazka)</p> \
            </div> \
        </div> \
        ");
    $("#markdown_info").find(".info").hide();
    $("#markdown_info").click(function() {
        $(this).find(".info").toggle();
        return false;
    });
});
