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
                if (this.id < data.id) {
                    toggle_post(this);
                }
            })
        }
     });
}

$(document).ready(function() {
    $(".post_body").before('<div class="post_head"></div>');
    $(".post").find(".post_head").before(
        '<div style="font-size: 0.8em; text-align:right; margin: 0.5em 0 -1em 0;">' + 
        '[ <a class="js_toggle_post" href="#toggle">pokaż/schowaj post</a> ]' +
        '</div>'
    );
    $(".post").each(function() {
        var post = $(this);
        $(this).find(".js_toggle_post").click(function() { 
            toggle_post(post);
        });
        $(post).find(".post_head").html(
                $(post).find(".post_author").html() + 
                " &bull; " +
                $(post).find(".post_date").html()
        ).toggle();
    })
    $('.post :first').before('<h3 id="js_show_all_posts" style="text-align: right;"><a href="#">Pokaż wszystkie posty</a></h3>');
    $('#js_show_all_posts').click(function() { $('.post').each( function() {
            $(this).find('.post_head').hide();
            $(this).find('.post_body').show();
        })
    })

    hide_old_posts();
})
