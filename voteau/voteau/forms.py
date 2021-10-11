from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, NumberInput, DateInput
from voteau.models import Votazione, Quesito


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class AddVotazioneForm(ModelForm):
    class Meta:
        model = Votazione
        fields = ["nome", "descrizione", "datainizio", "datafine", "minvotanti", "maxvotanti", "autore"]
        widgets = {
            'nome': Textarea(attrs={
                'class': 'Inputtext',
                'placeholder': 'Inserisci un nome per la votazione...',
                'id': 'nomeinput',

            }),

            'descrizione': Textarea(attrs={
                'class': "desc_vot",
                'placeholder': 'Inserisci una descrizione...',
                'id': 'textarea',
            }),

            'datainizio': DateInput(attrs={
                'class': "Inputtext",
                'placeholder': 'Inserisci una data di inizio...',
                'id': 'datainizioinput',
            }),

            'datafine': DateInput(attrs={
                'class': "Inputtext",
                'placeholder': 'Inserisci una data di fine...',
                'id': 'datafineinput',
            }),

            'minvotanti': NumberInput(attrs={
                'class': "Inputtext",
                'placeholder': 'Inserisci un minimo di votanti... [MIN: 3]',
                'id': 'minvotantiinput',
            }),

            'maxvotanti': NumberInput(attrs={
                'class': "Inputtext",
                'placeholder': 'Inserisci un massimo di votanti...',
                'id': 'maxvotantiinput',
            }),

        }

    def clean(self):
        cleaned_data = super(AddVotazioneForm, self).clean()
        if len(cleaned_data.get('descrizione')) > 500:
            self.add_error('descrizione', 'Descrizione troppo lunga')
        if len(cleaned_data.get('nome')) > 50:
            self.add_error('nome', 'Nome troppo lungo')
        #Inserito un validatore per minvotanti dentro il modello Votazione (è in inglese)
        if (cleaned_data.get('maxvotanti')) < (cleaned_data.get('minvotanti')):
            self.add_error('maxvotanti', 'Il massimo di votanti non può essere minore del Minimo Votanti')


class AddQuesitoForm(ModelForm):
    class Meta:
        model = Quesito
        fields = ['id', 'votazione', 'quesito', 'risposta']
        widgets = {
            'id': NumberInput(attrs={
                'class': 'HiddenText',
                'id': 'id',

            }),
            'votazione': Textarea(attrs={
                'class': 'HiddenText',
                'id': 'id',
                'default': '0'

            }),
            'quesito': Textarea(attrs={
                'class': 'Inputtext',
                'style': 'resize: none',
                'placeholder': 'Inserisci un quesito...',
                'id': 'nomequesito',

            }),
            'risposta': NumberInput(attrs={
                'class': 'Inputtext',
                'default': '2',
                'id': 'risposta',
            }),
        }

    def clean(self):
        cleaned_data = super(AddQuesitoForm, self).clean()
        if len(cleaned_data.get('quesito')) < 1:
            self.add_error('quesito', 'Inserisci qualcosa nel campo')
    # Inputtext ha già un controllo per la lunghezza, non ti fa eccedere oltre i 300 caratteri
