from models import UserProfile
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
#from django.utils.translation import ugettext_lazy as _




class UserInline(admin.StackedInline):
    model = UserProfile
    #extra = 1
    max_num = 1

class UserProfileAdmin(UserAdmin):
    inlines = [UserInline, ]

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
