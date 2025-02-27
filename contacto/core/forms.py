import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from user.models import User
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError


# Validador para RUT
def validate_rut(rut):
    """
    Valida un RUT chileno.
    """
    rut = rut.upper().replace(".", "").replace("-", "")
    match = re.match(r"^(\d{1,8})([0-9K])$", rut)
    if not match:
        raise ValidationError("El RUT ingresado no es válido.")

    number, verifier = match.groups()
    reverse_digits = map(int, reversed(number))
    factors = [2, 3, 4, 5, 6, 7]
    s = sum(d * f for d, f in zip(reverse_digits, factors * 2))
    mod = (-s) % 11
    expected_verifier = "K" if mod == 10 else str(mod)
    if verifier != expected_verifier:
        raise ValidationError("El RUT ingresado no es válido.")

# Formulario para registro de usuarios
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from user.models import User, regiones_comunas


class CustomUserCreationForm(UserCreationForm):
    rut = forms.CharField(
        max_length=12,
        required=True,
        label="RUT",
        validators=[validate_rut],
        help_text="Ingrese un RUT válido, incluyendo dígito verificador.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUT'}),
        error_messages={
            'required': 'El RUT es obligatorio.',
            'invalid': 'El RUT ingresado no es válido.',
        }
    )

    region = forms.ChoiceField(
        choices=[(region, region) for region in regiones_comunas.keys()],
        required=True,
        label="Región",
        help_text="Seleccione la región correspondiente.",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    comuna = forms.ChoiceField(
        choices=[],
        required=True,
        label="Comuna",
        help_text="Seleccione la comuna correspondiente.",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Tipo de usuario",
        help_text="Seleccione si el usuario es cliente o profesional.",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        help_text="La contraseña debe tener al menos 8 caracteres y no puede ser muy común.",
    )

    password2 = forms.CharField(
        label="Confirme su contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme su contraseña'}),
        help_text="Ingrese la misma contraseña nuevamente para verificar.",
    )

    class Meta:
        model = User
        fields = ['username', 'group', 'first_name', 'last_name', 'rut', 'email', 'telefono', 'location', 'region', 'comuna', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUT'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
        }
        error_messages = {
            'username': {
                'required': 'El nombre de usuario es obligatorio.',
                'unique': 'Este nombre de usuario ya está en uso.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Verificar si hay datos enviados para preseleccionar las comunas
        region_selected = self.data.get('region') or self.initial.get('region')
        if region_selected:
            self.fields['comuna'].choices = [(comuna, comuna) for comuna in regiones_comunas.get(region_selected, [])]
        else:
            self.fields['comuna'].choices = [('', 'Seleccione una comuna')]



# ACTUALIZACIÓN DATOS DE USER
from django import forms
from user.models import User
from user.models import regiones_comunas  # Asegúrate de importar `regiones_comunas`

class UserUpdateForm(forms.ModelForm):
    region = forms.ChoiceField(
        choices=[(region, region) for region in regiones_comunas.keys()],
        required=True,
        label="Región",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    comuna = forms.ChoiceField(
        required=True,
        label="Comuna",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def __init__(self, *args, **kwargs):
        # Sobreescribir para manejar comunas dinámicas
        region_selected = kwargs.pop('region_selected', None)
        super().__init__(*args, **kwargs)

        if region_selected:
            # Cargar comunas según la región seleccionada
            comunas = regiones_comunas.get(region_selected, [])
            self.fields['comuna'].choices = [(comuna, comuna) for comuna in comunas]
        else:
            self.fields['comuna'].choices = [('', 'Seleccione una región primero')]

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'location', 'telefono', 'region', 'comuna']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }




#ACTUALIZACIÓN DATOS DE MODELO PERFIL
from django import forms
from user.models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'specialties',
            'profile_picture',
            'linkedin',
            'instagram',
            'facebook',
            'twitter',
            'website'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'specialties': forms.CheckboxSelectMultiple(),  # Usar checkboxes
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enlace a LinkedIn'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enlace a Instagram'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enlace a Facebook'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enlace a Twitter'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enlace a tu Página Web'}),
        }



#Subir credenciales
from django import forms
from user.models import Credential

class CredentialForm(forms.ModelForm):
    class Meta:
        model = Credential
        fields = ['title', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }



    


#Filtros especialidad, region y comuna
from django import forms
from user.models import Speciality, regiones_comunas


class SpecialtyFilterForm(forms.Form):
    specialty = forms.ModelChoiceField(
        queryset=Speciality.objects.all(),
        required=False,
        label="Especialidad",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Todas las especialidades"
    )
    region = forms.ChoiceField(
        choices=[("", "Todas las regiones")] + [(region, region) for region in regiones_comunas.keys()],
        required=False,
        label="Región",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    comuna = forms.ChoiceField(
        choices=[("", "Todas las comunas")],
        required=False,
        label="Comuna",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        region_selected = self.data.get('region') or self.initial.get('region')
        if region_selected:
            comunas = regiones_comunas.get(region_selected, [])
            self.fields['comuna'].choices = [("", "Todas las comunas")] + [(comuna, comuna) for comuna in comunas]

    

## FORMULARIO RESEÑAS
from django import forms
from user.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Escribe tu comentario aquí...'}),
        }
        labels = {
            'rating': 'Calificación (1 a 5)',
            'comment': 'Comentario',
        }



#Filtros por comuna y región
class ProfessionalFilterForm(forms.Form):
    specialty = forms.ModelChoiceField(
        queryset=Speciality.objects.all(),
        required=False,
        label="Especialidad"
    )
    region = forms.ChoiceField(
        choices=[("", "Todas las regiones")] + [(region, region) for region in regiones_comunas.keys()],
        required=False,
        label="Región"
    )
    comuna = forms.ChoiceField(
        choices=[("", "Todas las comunas")],
        required=False,
        label="Comuna"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si una región está seleccionada, actualiza las comunas dinámicamente
        region_selected = self.data.get("region") or self.initial.get("region")
        if region_selected:
            comunas = regiones_comunas.get(region_selected, [])
            self.fields["comuna"].choices = [("", "Todas las comunas")] + [(comuna, comuna) for comuna in comunas]
