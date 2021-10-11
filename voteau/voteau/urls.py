"""voteau URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from voteau import views

urlpatterns = [
    path('', views.blank),
    path('login/', views.Login, name='login'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.Logout, name='logout'),
    path('addvotation/', views.AddVotation, name="addvotation"),
    path(r'votations/<autoreId>/<votationId>/', views.votations, name="votations"),
    path('removevotations/', views.DelVotation, name="delvotations"),
    path(r'removevotation/<id_v>/', views.DelVote, name="delvotation"),
    path(r'votations/<id_v>/<id_p>/addvotante', views.Votantia, name='addvotante'),
    path(r'votations/<id_v>/<id_p>/removevotante', views.Votantir, name='removevotante'),
    path(r'addpartecipazione/<id_v>/<id_p>/<id_a>', views.AddPartecipazione, name="addpart"),
    path(r'removepartecipazione/<id_v>/<id_p>/<id_a>', views.RemovePartecipazione, name="removepart"),
    path(r'votations/<id_v>/newpoll', views.makeQuesito, name='makequesito'),
    path(r'votations/<id_v>/removequesito', views.removeQuesiti, name='removequesito'),
    path(r'removequesito/<id_q>/', views.removeQuesito, name='removeques'),
    path(r'vote/', views.Voteall, name="vote"),
    path(r'vote/<id_v>/', views.Vote, name="addvote"),
    path(r'saveVotazione/<risp>/<id_v>', views.saveVot, name='savevot'),
    path('risultati/', views.Risultati, name="ris"),
    path(r'votations/<id_v>/esito', views.Esito, name='esito')
]
