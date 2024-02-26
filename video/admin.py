from django.contrib import admin

from video.models import Video, Movie, Serie, Episode

class MovieAdmin(admin.ModelAdmin):
    list_display = ['title']

class SeriesAdmin(admin.ModelAdmin):
    list_display = ['title']

class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['title', 'series']

# Register your models here.
admin.site.register(Video)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Serie, SeriesAdmin)
admin.site.register(Episode, EpisodeAdmin)