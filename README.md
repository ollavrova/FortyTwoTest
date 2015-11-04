42-test project
===========================

A Django 1.6+ project



### Description
* apps in apps/ folder
* per-app templates folders
* per-app static folders
* used migrations
* use settings.local for different environments
* common templates live in templates/
* common static lives in assets/
* management commands proxied to single word make commands, e.g make test

Requirements packages:
Django==1.6.7
42cc-pystyle
south
easy_thumbnails
selenium