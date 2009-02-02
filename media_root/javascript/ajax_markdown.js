$(document).ready(function() {
    var form = $('form.preview');
    var subbutton = form.find(':submit');
    subbutton.before('<span id="ajax_preview_image"></span><input id="ajax_preview_button" name="preview" type="submit" value="Podgląd" />');
    var preview = subbutton.prev(':submit');
    
    preview.click(function() {
        var t = form.find('textarea').val();
        if ($('#ajax_form_preview').length == 0) {
            form.before('<div id="ajax_form_preview"> </div>');
        }
        $('#ajax_preview_image').html('<img style="margin: 0 2em;" src="/static/images/ajax-loader.gif" alt="" />');
        $.ajax({
            type: "POST",
            url: "/forum/get_markdown/",
            dataType: "json",
            data: {'text': t, 'xhr': true},
            success: function(data) {
                $('#ajax_form_preview').html(data.markdown);
                $('#ajax_preview_image').html('');
           }
         });


        return false;
    })
});
