$(document).ready(function() {
    var show_message = 'Pokaż zagnieżdzony cytat';
    var hide_message = 'Schowaj zagnieżdzony cytat';

    $('blockquote blockquote').each(function() {
        var quote = $(this);

        quote.before('<strong style="margin-left: 2em;"> &times; \
                <a class="show_blockquotes" href="#js_show_quotes"> \
                  ' + show_message + ' \
                </a> \
            </strong>');
        quote.hide();
        quote.prev('strong a .show_blockquotes').click(function() {
            $(this).find('.show_blockquotes').toggle(
                function() {
                    $(this).text(show_message);
                    quote.toggle('slow')},
                function() {
                    $(this).text(hide_message);
                    quote.toggle('slow');
                });
            // WTF!?
            $(this).find('.show_blockquotes').text(hide_message);
            quote.toggle('slow');
        });
    });
});
