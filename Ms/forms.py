from django import forms

class MsForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea(attrs = {"class": "formulario",

				"placeholder": "Escribe tu mensaje"

			}))