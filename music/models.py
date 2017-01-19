#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/22/16 2:40 PM
# @Author  : YangGao
# @File    : models.py
from django.db import models
from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse

'''

(py_ve) johnsdeMacBook-Pro:python_web_with_django johnsmac$ python manage.py makemigrations music
Migrations for 'music':
  music/migrations/0001_initial.py:
    - Create model Album
    - Create model Son
(py_ve) johnsdeMacBook-Pro:python_web_with_django johnsmac$ python manage.py sqlmigrate music 0001
BEGIN;
--
-- Create model Album
--
CREATE TABLE "music_album" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
"artist" varchar(250) NOT NULL, "album_title" varchar(500) NOT NULL,
"genre" varchar(100) NOT NULL, "album_logo" varchar(1000) NOT NULL);
--
-- Create model Son
--
CREATE TABLE "music_son" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
"file_type" varchar(10) NOT NULL, "song_title" varchar(250) NOT NULL,
 "album_id" integer NOT NULL REFERENCES "music_album" ("id"));

CREATE INDEX "music_son_95c3b9df" ON "music_son" ("album_id");

COMMIT;

(py_ve) johnsdeMacBook-Pro:python_web_with_django johnsmac$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, music, sessions
Running migrations:
  Applying music.0001_initial... OK
(py_ve) johnsdeMacBook-Pro:python_web_with_django johnsmac$


'''


class Album(models.Model):

    user = models.ForeignKey(User, default=1)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)
    is_local_file = models.BooleanField(default=False)
    # '''当点击添加 新专辑 按钮时 会走这方法,暂时 有URL错误 '''
    #
    # def get_absolute_url(self):
    #     reverse('music:all_songs', kwargs={'pk': self.pk})

    def __str__(self):
        return self.album_title + '_' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)
    audio_file = models.FileField(default='')

    def __str__(self):
        return self.song_title
