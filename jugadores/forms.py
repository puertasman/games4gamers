from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Jugadores

User = get_user_model()

class formulario_registro_usuarios(forms.ModelForm):
    username = forms.CharField(label='Nombre de usuario', max_length=100,
                               widget=forms.TextInput(attrs={'id': 'id_username',
                                                             'placeholder': 'Introduce tu nombre de usuario'}))
    password1 = forms.CharField(label='Contraseña', max_length=100,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Introduce tu contraseña'}))
    password2 = forms.CharField(label='Confirmar contraseña', max_length=100,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirma tu contraseña'}))
    fecha_nacimiento = forms.DateField(label='Fecha de nacimiento',
                                       required=True, widget=forms.DateInput(attrs={'type': 'date',
                                'placeholder': 'YYY-MM-DD',
                                'class': 'datepicker'}))
    email = forms.EmailField(label='Correo electrónico',
                             required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'Introduce tu correo electrónico'}))
    nivel = forms.ChoiceField(label='Nivel', choices=Jugadores.NIVEL_OPCIONES,
                              widget=forms.Select(attrs={'placeholder': 'Selecciona tu nivel'}))

    # añadido para que no se pueda registrar dos usuarios con el mismo nombre
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario ya existe. Por favor, elige otro.")
        return username
    # añadido para que no se pueda registrar dos usuarios con el mismo mail
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe una cuenta con este correo electrónico. Por favor, utiliza otro.")
        return email
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'nivel', 'fecha_nacimiento']
        # con esto se controla el orden de aparición de los campos en el formulario

    def save(self, commit=True):
        user = super(formulario_registro_usuarios, self).save(commit=False)
        password = self.cleaned_data.get('password1')
        # establecemos la contraseña
        user.set_password(password)
        user.email = self.cleaned_data['email']
        # de momento activo pero lo cambiaré para que tenga que activar por email.
        # user.is_active = False  # hasta que no conteste al mail de activación estará inactivo
        if commit:
            user.save()
        return user
