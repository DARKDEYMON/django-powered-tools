from django import forms

__all__ = ['SearchForm']

class SearchForm(forms.Form):
	search = forms.CharField(required=False, label="", help_text="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Buscar...','autocomplete':'off'}))
