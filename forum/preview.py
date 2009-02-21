# -*- coding: utf-8 -*-

class FormPreview(object):
    def __init__(self, form, POST):
        self.form = form
        self.POST = POST

    def is_preview(self):
        return "preview" in self.POST

    def as_table(self):
        if self.is_preview():
            return "<h1>Działa!</h1>" + self.form.as_table()
        return self.form.as_table()

    def as_ul(self):
        if self.is_preview():
            return "<h1>Działa!</h1>" + self.form.as_ul()
        return self.form.as_ul()

    def as_p(self):
        if self.is_preview():
            return "<h1>Działa!</h1>" + self.form.as_p()
        return self.form.as_ul()
