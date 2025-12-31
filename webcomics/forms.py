from django import forms
from .models import Manga, Comment

class MangaForm(forms.ModelForm):
    class Meta:
        model = Manga
        fields = ['nombre_del_manga', 'descripcion', 'front_page', 'type_of_manga', 'publicado_por', 'talla', 'precio', 'costo']
        widgets = {
            'nombre_del_manga': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del manga'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción...'}),
            'type_of_manga': forms.Select(attrs={'class': 'form-select'}),
            'publicado_por': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autor/Publicado por'}),
            'talla': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: M, 28, XL...'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Añadir un comentario...', 'autocomplete': 'off'}),
        }
