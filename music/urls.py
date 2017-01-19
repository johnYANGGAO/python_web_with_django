#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/22/16 2:58 PM
# @Author  : YangGao
# @File    : urls.py
from django.conf.urls import url
from . import views

'''namespace'''
app_name = 'music'

urlpatterns = [

    url(r'^play_song/$', views.play_song, name='play'),

    url(r'^(?P<album_id>[0-9]+)/cancel_favorite/(?P<song_id>[0-9]+)/$', views.cancel_favorite,
        name='cancel_favorite_song'),

    url(r'^(?P<album_id>[0-9]+)/favorite_song/(?P<song_id>[0-9]+)/$', views.favorite_direct, name='favorite_song'),

    url(r'^search/$', views.display_search_results, name='search'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),
    url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    url(r'^create_album/$', views.create_album, name='create_album'),
    url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    # url(r'album/add/$', views.AlbumCreate.as_view(), name='album_add'),
    # url(r'^[i]$', views.IndexView.as_view(), name='index'),
    url(r'^[i]$', views.index_global, name='index'),
    url(r'^(?P<pk>[0-9]+)/display/$', views.DetailView.as_view(), name='all_songs'),
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^$', views.index, name='index'),
    url(r'^[t]$', views.index_template, name='temp'),
    url(r'^[r]$', views.index_render, name='render'),
    url(r'^(?P<album_id>[0-9]+)/favorite/display/$', views.favorite_display, name='display_favorite'),
    url(r'^(?P<album_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^(?P<album_id>[0-9]+)/display/allById/$', views.all_songs_display_by_album_id, name='display_all_in_album'),
]
