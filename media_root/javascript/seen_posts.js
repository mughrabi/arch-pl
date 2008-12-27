function hide_post(post) 
{
    post.find(".js_show_hide").text("pokaż treść");
    __post_min_height = post.css("min-height");
    post.css("min-height", "2em"); 
    post.find(".post_body").hide();
}

function show_post(post)
{
    post.find(".js_show_hide").text("ukryj treść");
    post.css("min-height", __post_min_height); 
    post.find(".post_body").show();
}

function hide_old_posts()
{
    /* AJAX old post hiding.. */
    $.getJSON("latest_seen/",function(data){
        $(".post").each(function() {
            if $(this).
        })
    });
}


$(document).ready(function() {
    $(".thread_prop").append('&bull; <a id="hide_old_posts" href="#">Ukryj stare posty</a>');
    $("#hide_old_posts").click(hide_old_posts);

    $(".post").each(function () {
        var post = $(this);
        post.find(".panel-right").append('&bull; <a class="js_show_hide" href="#">ukryj treść</a>');
        $(this).find(".js_show_hide").toggle(
            function () { hide_post(post); },
            function () { show_post(post); }
        );
    });
})
