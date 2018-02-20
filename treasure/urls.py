"""treasure URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
import players.views as views
from treasure.views import homepage, crossdomain, extension

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', homepage, name='home'),
    path(r'crossdomain.xml', crossdomain, name='crossdomain'),
    path(r'extension.js', extension, name='extension'),
    path(r'players/new/<str:player>', views.create_player, name="new_player"),
    path(r'players/<int:player>', views.PlayerView.as_view(), name="show_player"),
    path(r'players/<int:player>/games/new', views.NewGameView.as_view(), name="new_game"),
    path(r'players/<int:player>/games/join', views.JoinAnyGameView.as_view(), name="join_any_game"),
    path(r'players/<int:player>/games/resume', views.ResumeGameView.as_view(), name="resume_game"),
    path(r'players/<int:player>/games/<int:game>/join', views.JoinGameView.as_view(), name="join_game"),
    path(r'players/<int:player>/games/<int:game>', views.GameView.as_view(), name="show_game"),
    path(r'players/<int:player>/games/<int:game>/autoplay', views.SetAutoPlayView.as_view(), name="autoplay"),
    path(r'players/<int:player>/games/<int:game>/play/<int:play>', views.PlayMoveView.as_view(), name="play_move")
]
