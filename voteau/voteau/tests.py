import unittest

from django.contrib.auth.models import User
from django.test import TestCase, Client
from voteau.models import *



if __name__ == "main":
    unittest.main()


class ModelTest(TestCase):

    def setUp(self):
        # inzializza il db
        self.client = Client()
        user1 = User(username="admin")
        user1.set_password("admin")
        user1.save()
        user2 = User(username="user",
                     password="user")
        user2.save()
        votazione1 = Votazione(id=1,
                               autore=user1,
                               nome="votazione_test",
                               descrizione="questo è un test",
                               datainizio=date.today().strftime('%Y-%m-%d'),
                               datafine=datetime.today() + timedelta(1),
                               minvotanti=1,
                               maxvotanti=3,
                               n_votanti=1)
        votazione1.save()
        votazione2 = Votazione(id=2,
                               autore=user2,
                               nome="votazione_test2",
                               descrizione="questo è un test2",
                               datainizio=date.today().strftime('%Y-%m-%d'),
                               datafine=datetime.today() + timedelta(1),
                               minvotanti=1,
                               maxvotanti=4,
                               n_votanti=1)
        votazione2.save()
        partecipazione1 = Partecipazioni(id=1,
                                         id_votazione=votazione1,
                                         id_partecipante=user2,
                                         votato=0)
        partecipazione1.save()
        partecipazione2 = Partecipazioni(id=2,
                                         id_votazione=votazione2,
                                         id_partecipante=user1,
                                         votato=0)
        partecipazione2.save()
        quesito1 = Quesito(id=1,
                           votazione=votazione1.id,
                           quesito="questo è un test?",
                           risposta=2,
                           n_fav=0,
                           n_nfav=0,
                           n_ast=0)
        quesito1.save()
        quesito2 = Quesito(id=2,
                           votazione=votazione2.id,
                           quesito="questo è un test2?",
                           risposta=3,
                           n_fav=0,
                           n_nfav=0,
                           n_ast=0)
        quesito2.save()
        quesito3 = Quesito(id=3,
                           votazione=votazione2.id,
                           quesito="questo è un test3?",
                           risposta=3,
                           n_fav=0,
                           n_nfav=0,
                           n_ast=0)
        quesito3.save()

    def testFindModels(self):
        # test sui modelli (Test Integrazione)
        self.assertEqual(len(User.objects.all()), 2)
        self.assertEqual(len(Votazione.objects.all()), 2)
        self.assertEqual(len(Partecipazioni.objects.all()), 2)
        self.assertEqual(len(Quesito.objects.all()), 3)


class ViewsTest(TestCase):

    def setUp(self):
        user1 = User(username="admin")
        user1.set_password("admin")
        user1.save()
        self.client = Client()
        self.client.login(username="admin", password="admin")
        votazione1 = Votazione(id=1,
                               autore=user1,
                               nome="votazione_test",
                               descrizione="questo è un test",
                               datainizio=date.today().strftime('%Y-%m-%d'),
                               datafine=datetime.today() + timedelta(1),
                               minvotanti=1,
                               maxvotanti=3,
                               n_votanti=1)
        votazione1.save()

    def testLoginView(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def testRegisterView(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def testHomeView(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def testAddvotation(self):
        response = self.client.get('/addvotation/')
        self.assertEqual(response.status_code, 200)

    def testRemovevotation(self):
        response = self.client.get('/removevotations/')
        self.assertEqual(response.status_code, 200)

    def testResults(self):
        response = self.client.get('/risultati/')
        self.assertEqual(response.status_code, 200)

    def testVotation(self):
        response = self.client.get(reverse("votations", kwargs={'autoreId':'1', 'votationId':'1'}))
        self.assertEqual(response.status_code, 200)

    def testVote(self):
        response = self.client.get(reverse("vote"), follow=True)
        self.assertEqual(response.status_code, 200)

    def testAddVote(self):
        response = self.client.get(reverse("addvote", kwargs={"id_v": "1"}))
        self.assertEqual(response.status_code, 200)

    def testMakeQuesito(self):
        response = self.client.get(reverse("makequesito", kwargs={'id_v': '1'}))
        self.assertEqual(response.status_code, 200)

    def testRemoveQuesito(self):
        response = self.client.get(reverse("removequesito", kwargs={'id_v': '1'}))
        self.assertEqual(response.status_code, 200)

    def testAddVotante(self):
        response = self.client.get(reverse("removevotante", kwargs={'id_v': '1', "id_p": "1"}))
        self.assertEqual(response.status_code, 200)

    def testRemVotante(self):
        response = self.client.get(reverse("addvotante", kwargs={'id_v': '1', "id_p": "1"}))
        self.assertEqual(response.status_code, 200)

    def testAddPartecipante(self):
        response = self.client.get(reverse("addpart", kwargs={'id_v': '1', "id_p": "1", "id_a": "1"}))
        self.assertEqual(response.status_code, 200)

    def testRemPartecipante(self):
        response = self.client.get(reverse("removepart", kwargs={'id_v': '1', "id_p": "1", "id_a": "1"}))
        self.assertEqual(response.status_code, 200)

    def testEsito(self):
        response = self.client.get(reverse("esito", kwargs={'id_v': '1'}))
        self.assertEqual(response.status_code, 200)

    def testLogOut(self):
        response = self.client.get('/logout/')
        # 302 = redirect. Da logout si reindirizza al Login
        self.assertEqual(response.status_code, 302)


class FunctionalTest(TestCase):

    def setUp(self):
        user1 = User(username="admin")
        user1.set_password("admin")
        user1.save()
        user2 = User(username="partecipante")
        user2.set_password("partecipante")
        user2.save()
        user3 = User(username="partecipante2")
        user3.set_password("partecipante2")
        user3.save()
        votazione1 = Votazione(id=1,
                               autore=user1,
                               nome="votazione_test",
                               descrizione="questo è un test",
                               datainizio=date.today().strftime('%Y-%m-%d'),
                               datafine=datetime.today() + timedelta(1),
                               minvotanti=1,
                               maxvotanti=3,
                               n_votanti=1)
        votazione1.save()
        partecipazione1 = Partecipazioni(id=1,
                                         id_votazione=votazione1,
                                         id_partecipante=user2,
                                         votato=0)
        partecipazione1.save()
        quesito1 = Quesito(id=1,
                           votazione=votazione1.id,
                           quesito="questo è un test?",
                           risposta=2,
                           n_fav=0,
                           n_nfav=0,
                           n_ast=0)
        quesito1.save()
        self.client = Client()
        self.client.login(username="admin", password="admin")

    def testLoginUnitTest(self):
        self.assertTrue(self.client.login(username="admin", password="admin"))

    def testRegisterUnitTest(self):
        utenti = User.objects.all().count()
        response = self.client.post(reverse("register"),
                                    data={"username": "admin1", "password1": "ashfkajhsfkjahksfahk",
                                          "password2": "ashfkajhsfkjahksfahk"},
                                    follow=True)
        self.assertGreater(User.objects.all().count(), utenti)

    def testAddAndRemoveVotationUnitTest(self):
        user = User.objects.get(username="admin")
        response = self.client.post(reverse("addvotation"),
                                    data={"nome": "test",
                                          "descrizione": "test",
                                          "datainizio": date.today().strftime('%Y-%m-%d'),
                                          "datafine": (datetime.today() + timedelta(1)).strftime('%Y-%m-%d'),
                                          "minvotanti": 3,
                                          "maxvotanti": 4,
                                          "autore": user})
        self.assertEqual(Votazione.objects.all().count(), 2)
        response = self.client.post(reverse("delvotation", kwargs={"id_v": "2"}), follow=True)
        self.assertEqual(Votazione.objects.all().count(), 1)

    def testAddAndRemoveQuesitoUnitTest(self):
        votazione = Votazione.objects.get(id="1")
        response = self.client.post(reverse("makequesito", kwargs={"id_v": "1"}),
                                    data={
                                        "votazione": votazione.id,
                                        "quesito": "test",
                                        "risposta": 2
                                    })
        self.assertEqual(Quesito.objects.all().count(), 2)
        response = self.client.post(reverse("removeques", kwargs={"id_q": "1"}), follow=True)
        self.assertEqual(Quesito.objects.all().count(), 1)

    def testAddAndRemovePartecipazioneUnitTest(self):
        votazione = Votazione.objects.get(id="1")
        response = self.client.post(reverse("addpart", kwargs={"id_v": "1", "id_p": "3", "id_a": "1"}),
                                    data={
                                        "votazione": votazione.id,
                                    })
        self.assertEqual(Partecipazioni.objects.all().count(), 2)
        response = self.client.post(reverse("removepart", kwargs={"id_v": "1", "id_p": "3", "id_a": "1"}), follow=True)
        self.assertEqual(Partecipazioni.objects.all().count(), 1)

    def testAddVoteUnitTest(self):
        self.client.logout()
        self.client = Client()
        self.client.login(username="partecipante", password="partecipante")
        votazione = Votazione.objects.get(id="1")
        response = self.client.post(reverse("savevot", kwargs={"risp": "1", "id_v": "1"}))
        partecipazione = Partecipazioni.objects.get(id_votazione="1", id_partecipante="2")
        self.assertEqual(votazione.n_votanti, 1)
        self.assertEqual(partecipazione.votato, 1)