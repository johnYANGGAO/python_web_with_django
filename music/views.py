#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/22/16 2:40 PM
# @Author  : YangGao
# @File    : views.py
# from django.http import Http404
from django.http import HttpResponse
from .models import Album, Song
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from .forms import AlbumForm, UserForm, SongForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.db.models import Q

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def index_render(request):
    all_albums = Album.objects.all()
    context = {
        'all_albums': all_albums
    }

    return render(request, 'music/index.html', context)


def index_template(request):
    all_albums = Album.objects.all()
    template = loader.get_template('music/index.html')
    context = {
        'all_albums': all_albums,
    }
    return HttpResponse(template.render(context, request))


# def index(request):
#     all_albums = Album.objects.all()
#     html = ''
#
#     for album in all_albums:
#         url = '/music/' + str(album.id) + '/'
#         html += '<a href="' + url + '">' + album.album_title + '</a><span>' + \
#                 '<a href="' + album.album_logo + '"> 专辑logo</a></span><br>'
#
#     return HttpResponse(html)


def detail(request, album_id):
    # try:
    #     album = Album.objects.get(pk=album_id)
    # except Album.DoesNotExist:
    #     raise Http404('Album does not exist')
    # '''No Album matches the given query.'''
    album = get_object_or_404(Album, pk=album_id)

    return render(request, 'music/detail.html', {
        'album': album})


def favorite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        selected_song = album.song_set.get(pk=request.POST['song'])
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/a.html', {
            'album': album, 'error_message': 'no song be selected '})
    else:
        selected_song.is_favorite = True
        selected_song.save()
        return render(request, 'music/b.html', {'album': album})


def favorite_direct(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    selected_song = Song.objects.get(pk=song_id)
    selected_song.is_favorite = True
    selected_song.save()
    return render(request, 'music/all_songs_by_albumID.html', {'album': album})


def cancel_favorite(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    selected_song = Song.objects.get(pk=song_id)
    selected_song.is_favorite = False
    selected_song.save()
    return render(request, 'music/all_songs_by_albumID.html', {'album': album})


''' check all of favorite songs alone  by album_id in browser'''


def favorite_display(request, album_id):
    album = get_object_or_404(Album, pk=album_id)

    return render(request, 'music/b.html', {'album': album})


def all_songs_display_by_album_id(request, album_id):
    album = get_object_or_404(Album, pk=album_id)

    return render(request, 'music/all_songs_by_albumID.html', {'album': album})


# class IndexView(generic.ListView):
#     template_name = 'music/index.html'
#     context_object_name = 'object_list'
#
#     def get_queryset(self):
#         return Album.objects.all()


def index_global(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        return render(request, 'music/index.html', {'object_list': albums})


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/all_songs_by_albumID.html'


# class AlbumCreate(CreateView):
#     # the name of html file must be album_form , then does work
#     model = Album
#     fields = ['artist', 'album_title', 'genre', 'album_logo']


def create_album(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        '''TODO how to hide the attr like is_local_file in form'''
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.is_local_file = True
            album.album_logo = request.FILES['album_logo']
            logo_type = album.album_logo.url.split('.')[-1]
            logo_type = logo_type.lower()
            if logo_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/album_form.html', context)
            album.save()
            return render(request, 'music/all_songs_by_albumID.html', {'album': album})

        context = {
            "form": form,
        }
        return render(request, 'music/album_form.html', context)


def delete_album(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        album = Album.objects.get(pk=album_id)
        album.delete()
        albums = Album.objects.filter(user=request.user)
        return render(request, 'music/index.html', {'object_list': albums})


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'object_list': albums})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            print('user is active', user.is_active)
            if user.is_active:
                login(request, user)
                print('user name is ', user.username)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'object_list': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def display_search_results(request):
    song_results = Song.objects.all()
    query = request.GET.get("search")
    if query:
        song_results = song_results.filter(
            Q(song_title__icontains=query)
        ).distinct()
        if song_results:
            return render(request, 'music/search_results.html', {
                'songs': song_results,
            })
        else:
            return render(request, 'music/no_answer_page.html')


def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/add_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'music/add_song.html', context)
        song.file_type = file_type
        song.save()
        return render(request, 'music/all_songs_by_albumID.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/add_song.html', context)


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/all_songs_by_albumID.html', {'album': album})


def play_song(request):
    return render(request, 'music/player.html')
