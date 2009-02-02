$(document).ready(function() {
    var form = $('form.preview');
    var subbutton = form.find(':submit');
    subbutton.before('<input name="preview" type="submit" value="Podgląd" />');
    var preview = subbutton.prev(':submit');
    
    preview.click(function() {
        var t = form.find('textarea').val();
        if ($('#ajax_form_preview').length == 0) {
            form.before('<div id="ajax_form_preview"> </div>');
        }
        $('#ajax_form_preview').html('<img style="margin: 2em;" src="/static/images/ajax-loader.gif" alt="" />');
         $.ajax({
            type: "POST",
            url: "/forum/get_markdown/",
            dataType: "json",
            data: {'text': t, 'xhr': true},
            success: function(data) {
                $('#ajax_form_preview').html(data.markdown);
           }
         });


        return false;
    })
});
