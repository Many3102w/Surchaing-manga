from django import forms
from .models import Manga, Comment

class MangaForm(forms.ModelForm):
    class Meta:
        model = Manga
        fields = ['nombre_del_manga', 'descripcion', 'front_page', 'type_of_manga', 'publicado_por']
        widgets = {
            'nombre_del_manga': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'publicado_por': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autor'}),
            'type_of_manga': forms.Select(attrs={'class': 'form-select'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Añadir un comentario...', 'autocomplete': 'off'}),
        }
