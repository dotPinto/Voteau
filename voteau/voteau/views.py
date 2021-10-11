from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from voteau.models import Votazione, Partecipazioni, Quesito
from django.contrib.auth import get_user_model
from django.contrib import messages
from voteau.forms import *
from django.db.models import Q
from datetime import date
from functools import reduce
import operator
import ast


def blank(request):
    return redirect('home')


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
           messages.info(request, "Password o username non corretti")
    return render(request, "login.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def home(request):
    return render(request, "home.html", {"votations": (Votazione.objects.all())})


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, "register.html", {'form': form})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def Logout(request):
    logout(request)
    return redirect('login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def AddVotation(request):
    form = AddVotazioneForm()
    if request.method == "POST":
        form = AddVotazioneForm(request.POST)
        instance = form.instance
        if form.is_valid() or instance.autore_id == 0:
            instance = form.instance
            instance.autore_id = request.user.id
            instance.save()
            messages.success(request, f"Votazione {instance.nome} creata!")
    return render(request, "addvotation.html", {'form': form})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def votations(request,  autoreId, votationId):
    autoreid = int(autoreId)
    autore = User.objects.get(pk=autoreid)
    try:
        votation = Votazione.objects.get(pk=votationId)
    except Votazione.DoesNotExist:
        votation = None

    qs = Partecipazioni.objects.all().filter(id_votazione=votation)
    utenti = qs.only('id_partecipante_id')
    if utenti.exists():
        utenti_n = User.objects.exclude(reduce(operator.or_, (Q(id__contains=x) for x in utenti.values_list('id_partecipante', flat=True))))
        return render(request, "votation.html", {'votation': votation, "autore": autore, "utenti": utenti_n, "partecipazioni": Partecipazioni.objects.all()})
    else:
        return render(request, "votation.html", {'votation': votation, "autore": autore, "utenti": User.objects.all(), "partecipazioni": Partecipazioni.objects.all()})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def DelVote(request, id_v):
    idvv = int(id_v)
    if idvv != 0 and idvv is not None:
        try:
            Votazione.objects.all().filter(id=idvv).delete()
            if Quesito.objects.all().filter(votazione=id_v):
                Quesito.objects.all().filter(votazione=id_v).delete()
        except Votazione.DoesNotExist:
            messages.info(request, "Votazione non cancellata")
    return render(request, "removevotations.html", {"votations": Votazione.objects.all()})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def DelVotation(request):
    return render(request, "removevotations.html", {"votations": (Votazione.objects.all())})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def Votantia(request, id_v, id_p):
    autoreid = int(id_p)
    user = get_user_model()
    autore = User.objects.get(pk=autoreid)
    try:
        votation = Votazione.objects.get(pk=id_v)
    except Votazione.DoesNotExist:
        votation = None

    qs = Partecipazioni.objects.all().filter(id_votazione=votation)
    utenti = qs.only('id_partecipante_id')
    if utenti.exists():
        utenti_n = User.objects.exclude(
            reduce(operator.or_, (Q(id__contains=x) for x in utenti.values_list('id_partecipante', flat=True))))
        return render(request, "addpartecipante.html", {"utenti": utenti_n, "votation": votation})
    else:
        return render(request, "addpartecipante.html", {"utenti": User.objects.all(), "votation": votation})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def Votantir(request, id_v, id_p):
    autoreid = int(id_p)
    user = get_user_model()
    autore = User.objects.get(pk=autoreid)
    try:
        votation = Votazione.objects.get(pk=id_v)
    except Votazione.DoesNotExist:
        votation = None

    qs = Partecipazioni.objects.all().filter(id_votazione=votation)
    utenti = qs.only('id_partecipante_id')
    if utenti.exists():
        utenti_n = User.objects.filter(id__in=utenti.values_list('id_partecipante', flat=True))
        return render(request, "RemovePartecipante.html", {"utenti": utenti_n, "votation": votation})
    else:
        return render(request, "RemovePartecipante.html", {"utenti": [], "votation": votation})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def AddPartecipazione(request, id_v, id_p, id_a):
    votazione = Votazione.objects.get(pk=id_v)
    partecipante = User.objects.get(pk=id_p)
    autore = User.objects.get(pk=id_a)
    partecipazione = Partecipazioni(id_votazione=votazione, id_partecipante=partecipante)
    if Partecipazioni.objects.all().filter(id_votazione=votazione).count() < votazione.maxvotanti:
        try:
            partecipazione.save()
            messages.info(request, f"Partecipante {partecipazione.id_partecipante} aggiunto!")
        except Exception as e:
            messages.error(request, "Abbiamo riscontrato un errore salvando la partecipazione")
        qs = Partecipazioni.objects.all().filter(id_votazione=votazione)
        utenti = qs.only('id_partecipante_id')


        if utenti.exists():
            utenti_n = User.objects.exclude(reduce(operator.or_, (Q(id__contains=x) for x in utenti.values_list('id_partecipante', flat=True))))
            return render(request, "AddPartecipante.html", {'votation': votazione, "autore": autore.id, "utenti": utenti_n, "partecipazioni": Partecipazioni.objects.all()})
        else:
            return render(request, "AddPartecipante.html", {'votation': votazione, "autore": autore.id, "utenti": User.objects.all(), "partecipazioni": Partecipazioni.objects.all()})
    else:
        messages.error(request, "Numero massimo di votanti è stato raggiunto, impossibile aggiungerne altri!")
        return render(request, "AddPartecipante.html",
                      {'votation': votazione, "autore": autore.id, "utenti": [],
                       "partecipazioni": Partecipazioni.objects.all()})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def makeQuesito(request, id_v):
    form = AddQuesitoForm()
    votation = None
    if request.method == 'POST':
        try:
            votation = Votazione.objects.get(pk=id_v)
        except Votazione.DoesNotExist:
            votation = None
        form = AddQuesitoForm(request.POST)
        if form.is_valid():
            instance = form.instance
            instance.votazione = id_v
            instance.save()
            messages.success(request, "Quesito creato correttamente!")
    return render(request, "makequesito.html", {'votation': votation, 'form': form})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def removeQuesiti(request, id_v):
    if (id_v != 0 and id_v is not None):
        idvv = int(id_v)
        try:
            quesiti = Quesito.objects.all().filter(votazione=idvv)
        except Votazione.DoesNotExist:
            messages.info(request, "Votazione non cancellata")

    return render(request, "removequesito.html", {"quesiti": quesiti})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def removeQuesito(request, id_q):
    idq = int(id_q)
    try:
        Quesito.objects.get(pk=idq).delete()
        messages.info(request, "Quesito cancellato")
    except Votazione.DoesNotExist:
        messages.info(request, "Quesito non cancellato")

    return render(request, "removequesito.html", {"quesiti": Quesito.objects.all()})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def Voteall(request):
    partecipazioni_sue = Partecipazioni.objects.all().filter(id_partecipante=request.user.id).filter(votato=0)
    partecipazioni_dis = partecipazioni_sue.only('id_votazione_id')
    votation_vote = Votazione.objects.all().filter(id__in=partecipazioni_dis.values_list('id_votazione', flat=True))
    votazionf = []
    for votazione in votation_vote:
        if votazione.datafine > date.today():
            votazionf.append(votazione)
    return render(request, "voteall.html", {"votations": votazionf})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def Vote(request, id_v):
    quesiti = Quesito.objects.all().filter(votazione=id_v)
    return render(request, "vote.html", {"quesiti": quesiti})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def saveVot(request, risp, id_v):
    i = 0
    risps = ast.literal_eval(risp)
    if isinstance(risps, int):
        quesiti = Quesito.objects.get(votazione=id_v)
    else:
        quesiti = Quesito.objects.all().filter(votazione=id_v)
        risps = [n for n in risps]

    p = Partecipazioni.objects.get(id_partecipante_id=request.user.id, id_votazione=int(id_v))
    p.votato = 1
    p.save()
    v = Votazione.objects.get(pk=int(id_v))
    v.n_votanti = v.n_votanti+1
    v.save()
    if isinstance(risps, int):
        if risps == 1: quesiti.n_fav += 1
        if risps == 2: quesiti.n_ast += 1
        if risps == 3: quesiti.n_nfav += 1
        quesiti.save()
    else:
        for q in quesiti:
            if risps[i] == 1: q.n_fav += 1
            if risps[i] == 2: q.n_ast += 1
            if risps[i] == 3: q.n_nfav += 1
            i += 1
            q.save()

    messages.success(request, "Votazione salvata!")
    return render(request, "home.html", {"votations": (Votazione.objects.all())})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def RemovePartecipazione(request, id_v, id_p, id_a):
    votazione = Votazione.objects.get(pk=id_v)
    partecipante = User.objects.get(pk=id_p)
    partecipazione = Partecipazioni(id_votazione=votazione, id_partecipante=partecipante)
    autore = User.objects.get(pk=id_a)
    nome = partecipazione.id_partecipante
    ha_votato_query = Partecipazioni.objects.all().filter(id_partecipante_id=id_p).filter(id_votazione_id=id_v)
    if ha_votato_query.filter(votato=0):
        Partecipazioni.objects.all().filter(id_partecipante_id=id_p).filter(id_votazione_id=id_v).delete()
        messages.info(request, f"Partecipante {nome} rimosso!")
        qs = Partecipazioni.objects.all().filter(id_votazione=votazione)
        utenti = qs.only('id_partecipante_id')
        utenti_n = User.objects.all().filter(id__in=utenti.values_list('id_partecipante', flat=True))
        return render(request, "removepartecipante.html", {'votation': votazione, "autore": autore.id,
                                                           "utenti": utenti_n,
                                                           "partecipazioni": Partecipazioni.objects.all()})
    else:
        qs = Partecipazioni.objects.all().filter(id_votazione=votazione)
        utenti = qs.only('id_partecipante_id')
        utenti_n = User.objects.all().filter(id__in=utenti.values_list('id_partecipante', flat=True))
        messages.error(request, f"Partecipante {nome} non può essere rimosso perchè ha già votato!")
        return render(request, "removepartecipante.html", {'votation': votazione,
                                                           "autore": autore.id, "utenti": utenti_n,
                                                           "partecipazioni": Partecipazioni.objects.all()})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def Risultati(request):
    partecipazioni_sue = Partecipazioni.objects.all().filter(id_partecipante=request.user.id)
    partecipazioni_dis = partecipazioni_sue.only('id_votazione_id')
    votazioniv = Votazione.objects.all().filter(id__in=partecipazioni_dis.values_list('id_votazione', flat=True))
    votazionic = Votazione.objects.all().filter(autore_id=request.user.id)
    votazioni = votazionic.union(votazioniv)
    votazionf = []
    for votazione in votazioni:
        if votazione.datafine < date.today():
            votazionf.append(votazione)
    return render(request, "Risultati.html", {"votations": votazionf})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def Esito(request, id_v):
    user = get_user_model()
    votazione = Votazione.objects.get(pk=int(id_v))
    autore = User.objects.get(pk=votazione.autore.id)
    quesiti = Quesito.objects.all().filter(votazione=int(id_v))
    valida = votazione.n_votanti >= votazione.minvotanti
    perc_fav=[]
    perc_ast=[]
    perc_nfav=[]
    n_partecipanti= Partecipazioni.objects.filter(id_votazione=id_v).count()

    if n_partecipanti != 0:
        perc_votato = ((votazione.n_votanti/n_partecipanti)*100)
    else:
        perc_votato = 0

    for quesito in quesiti:
        if votazione.n_votanti != 0:
            perc_fav.append((quesito.n_fav / (quesito.n_nfav + quesito.n_fav + quesito.n_ast))*100)
            perc_ast.append((quesito.n_ast / (quesito.n_nfav + quesito.n_fav + quesito.n_ast))*100)
            perc_nfav.append((quesito.n_nfav / (quesito.n_nfav + quesito.n_fav + quesito.n_ast))*100)
        else:
            perc_fav.append(0)
            perc_ast.append(0)
            perc_nfav.append(0)
    perc_list= zip(perc_fav ,perc_ast ,perc_nfav, quesiti)
    return render(request, "Esito.html", {"votation": votazione, "autore": autore, "valida": valida, "listperc": perc_list , "percvotato": perc_votato})


