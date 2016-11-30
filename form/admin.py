from django.contrib import admin
from models import Form,Key,KeyContent
# Register your models here.
class FormAdmin(admin.ModelAdmin):
    list_display = ('title','author','password','create_time')

class KeyAdmin(admin.ModelAdmin):
    list_display = ('form','keyLabel','keyType')

class KeyContentAdmin(admin.ModelAdmin):
    list_display = ('key','content','create_time')

admin.site.register(Form,FormAdmin)
admin.site.register(Key,KeyAdmin)
admin.site.register(KeyContent,KeyContentAdmin)