from django.contrib import admin
from .models import Scene, Liker

admin.site.site_header = "Sceneshare Admin"
admin.site.site_title = "Sceneshare Admin"
admin.site.index_title = "Welcome, Admin!"

class LikerInLine(admin.TabularInline):
    model = Liker
    extra = 1

class SceneAdmin(admin.ModelAdmin):
    fieldsets = [('User', {'fields': ['user']}), ('URL', {'fields': ['url']}), ('Text', {'fields': ['text']}), ('Date Information', {
        'fields': ['published'], 'classes': ['collapse']}), ]
    inlines = [LikerInLine]

admin.site.register(Scene, SceneAdmin)
