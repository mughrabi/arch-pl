$(document).ready(function() {
    // wait function
    $.fn.wait = function(time, type) {
        time = time || 1000;
        type = type || "fx";
        return this.queue(type, function() {
            var self = this;
            setTimeout(function() {
                $(self).dequeue();
            }, time);
        });
    };

    // do the stuff
    $("#popupinfo").wait(4000).fadeOut("slow");
})
