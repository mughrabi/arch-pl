/* now that's dirty way of getting slug */
function get_slug() {
    var url = window.location.pathname.split("/")
    if (x[x.length -1] == "") {
        return url[url.length - 2]
    }
    return url[url.length - 1]
}

function toggle_post(post) {
    $(post).find(".post_body").toggle();
    $(post).find(".post_head").toggle();
}

function hide_old_posts() {
    $.ajax({
        type: "POST",
        url: "latest_seen_post/",
        dataType: "json",
        data: { 'xhr': true },
        success: function(data) {
            $('.post:not(:last)').each(function() {
                /* if old, create header, link, hide post body */
                if (data.id == -1 || this.id < data.id) {
                    $(this).find(".post_body").before('<div class="post_head"></div>');
                    $(this).find(".post_head").before(
                        '<div class="js_toggle_post_div" style="font-size: 0.8em; text-align:right; margin: 0.5em 0 -1em 0;">' + 
                        '<a class="js_toggle_post" href="#toggle">pokaż post</a>' +
                        '</div>'
                    );
                    toggle_post(this);
                }
            })
            $(".post").each(function() {
                var post = $(this);
                /* click action - hide header & link */
                $(this).find(".js_toggle_post").click(function() { 
                    toggle_post(post);
                    $(post).find(".js_toggle_post_div").hide();
                });
                /* each post build header */
                var short_text = $(post).find(".post_text").html(
                    ).replace(/\n/g, '').replace(/<blockquote>.*<\/blockquote>/g, '').replace(/<.*?>/g, '').substring(0, 110) + " ..."
                $(post).find(".post_head").html(
                        $(post).find(".post_author").html() + 
                        ' <span style="padding: 0 1em;">&bull;</span> ' +
                        $(post).find(".post_date").html() +
                        ' <span style="padding: 0 1em;">&bull;</span> ' +
                        ' <span style="color: #6F6F6F">' + short_text + '</span>'
                ).toggle();
            })

            $('.post :first').before('<h3 id="js_show_all_posts" style="text-align: right;"><a href="#">Pokaż wszystkie posty</a></h3>');
            $('#js_show_all_posts').click(function() { $('.post').each( function() {
                    $(this).find('.post_head').hide();
                    $(this).find('.post_body').show();
                    $('.post').each(function () { $(this).find('.js_toggle_post_div').hide(); })
                })
                $('#js_show_all_posts').hide();
            })
        } /* sucess */
     });
}

function show_hide_old_posts(){
    $('#forum_path_info').after('<h3 id="js_hide_old_posts" style="text-align: right;"> <a href="#"> Ukryj stare posty </a> </h3>');
    $('#js_hide_old_posts a').click(function () { 
        hide_old_posts(); 
        $('#js_hide_old_posts').hide();
    });
}

$(document).ready(function() {
    show_hide_old_posts();
})
