import datetime
from datetime import *
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


def getTomorrow():
    return datetime.today() + timedelta(1)


class Votazione(models.Model):
    id = models.AutoField(primary_key=True)
    autore = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=0)
    nome = models.CharField(max_length=30)
    descrizione = models.CharField(max_length=500)
    datainizio = models.DateField(default=datetime.today().strftime('%Y-%m-%d'))
    datafine = models.DateField(default=getTomorrow().strftime('%Y-%m-%d'))
    minvotanti = models.PositiveSmallIntegerField(validators=[MinValueValidator(3, "Almeno 3 votanti!")])
    maxvotanti = models.PositiveSmallIntegerField()
    n_votanti = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nome}"

    def get_absolute_url(self):
        return reverse('votations', args=[str(self.autore_id), str(self.id)])

    def deleteVotazione(self):
        return reverse('delvotation', args=[str(self.id)])


class Partecipazioni(models.Model):
    id = models.AutoField(primary_key=True)
    id_votazione = models.ForeignKey(Votazione, on_delete=models.CASCADE)
    id_partecipante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    votato = models.IntegerField(default=0)

    class Meta:
        unique_together = (("id_votazione", "id_partecipante"))

    def __str__(self):
        return f"tabella: {self.id_votazione}, partecipante: {self.id_partecipante}, votato={self.votato}"


class Quesito(models.Model):
    id = models.AutoField(primary_key=True)
    votazione = models.IntegerField(default=0)
    quesito = models.CharField(max_length=300)
    risposta = models.PositiveSmallIntegerField(default=2, validators=[MinValueValidator(2, "Almeno 2 risposte necessarie"),MaxValueValidator(3, "Massimo 3 risposte")])
    n_fav = models.IntegerField(default=0)
    n_nfav = models.IntegerField(default=0)
    n_ast = models.IntegerField(default=0)


