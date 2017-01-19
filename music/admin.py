#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/22/16 2:39 PM
# @Author  : YangGao
# @File    : admin.py

from django.contrib import admin
from .models import Album
from .models import Song

'''for admin page'''
admin.site.register(Album)
admin.site.register(Song)
