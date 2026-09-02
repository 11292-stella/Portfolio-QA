from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit
from .models import ExperienceHighlight, ContactMessage


class ExperienceHighlightForm(forms.ModelForm):
    class Meta:
        model = ExperienceHighlight
        fields = ['azione', 'area', 'tecnologie', 'dettaglio', 'ordine']
        widgets = {
            'dettaglio': forms.Textarea(attrs={'rows': 3}),
            'tecnologie': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # il <form> resta nel template
        self.helper.layout = Layout(
            Row(
                Column('azione', css_class='col-md-6'),
                Column('area', css_class='col-md-6'),
            ),
            Field('tecnologie', wrapper_class='tech-checks mb-3'),
            'dettaglio',
            Column('ordine', css_class='col-md-3'),
        )

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['nome', 'email', 'messaggio']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Come ti chiami?'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'la-tua-email@esempio.com'
            }),
            'messaggio': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4, 'placeholder': 'Raccontami del ruolo o del progetto...'
            }),
        }
        labels = {
            'nome': 'Nome',
            'email': 'Email',
            'messaggio': 'Messaggio',
        }
