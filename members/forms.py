from django import forms
from .models import ConsultaCrochet, ExperienciaTutorial, Nota, Usuario
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from .models import Comentario

# 🔹 Formulario de registro
class RegistroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'contraseña']
        widgets = {
            'contraseña': forms.PasswordInput(),
        }

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.contraseña = make_password(self.cleaned_data["contraseña"]) 
        if commit:
            usuario.save()
        return usuario

# 🔹 Formulario de login
class LoginForm(forms.Form):
    correo = forms.EmailField(label="Correo")
    contraseña = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")

    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get("correo")
        contraseña = cleaned_data.get("contraseña")

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            raise ValidationError("Usuario no encontrado.")

        if not check_password(contraseña, usuario.contraseña):
            raise ValidationError("Contraseña incorrecta.")

        cleaned_data["usuario"] = usuario
        return cleaned_data

# 🔹 Formulario para solicitar reset de contraseña
class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(label="Correo", max_length=254)

    def get_users(self, email):
        """Busca usuarios en tu modelo Usuario por el campo 'correo'"""
        return Usuario.objects.filter(correo__iexact=email)

# 🔹 Formulario para establecer nueva contraseña
class CustomSetPasswordForm(forms.Form):
    nueva_contraseña = forms.CharField(label="Nueva contraseña", widget=forms.PasswordInput)
    repetir_contraseña = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("nueva_contraseña")
        p2 = cleaned_data.get("confirmar_contraseña")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self):
        if self.usuario:
            self.usuario.contraseña = make_password(self.cleaned_data["nueva_contraseña"])
            self.usuario.save()

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'placeholder': 'Escribe tu comentario...',
                'rows': 4,
                'required': True
            }),
        }

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['titulo', 'contenido']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Escribe el título de tu nota...',
                'required': True
            }),
            'contenido': forms.Textarea(attrs={
                'placeholder': 'Escribe el contenido de tu nota...',
                'rows': 4,
                'required': True
            }),
        }


class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = ExperienciaTutorial
        fields = ['tutorial', 'dificultad', 'tiempo', 'experiencia', 'recomendacion']
        widgets = {
            'tutorial': forms.TextInput(attrs={
                'placeholder': 'Ej: Tulipanes, Girasoles, Llavero de Fresa, etc.',
                'maxlength': '100',
                'required': True
            }),
            'dificultad': forms.Select(attrs={
                'class': 'select-dificultad',
                'required': True
            }),
            'tiempo': forms.TextInput(attrs={
                'placeholder': 'Ej: 2 horas, 30 minutos, etc.',
                'maxlength': '50'
            }),
            'experiencia': forms.Textarea(attrs={
                'placeholder': '¿Cómo te fue con este tutorial? Comparte tu experiencia, tips, dificultades o lo que más te gustó...',
                'rows': 4,
                'required': True
            }),
            'recomendacion': forms.Select(attrs={
                'class': 'select-recomendacion',
                'required': True
            }),
        }
    
    def clean_tutorial(self):
        tutorial = self.cleaned_data.get('tutorial')
        if len(tutorial.strip()) < 3:
            raise forms.ValidationError("El nombre del tutorial debe tener al menos 3 caracteres")
        return tutorial.strip()
    
    def clean_experiencia(self):
        experiencia = self.cleaned_data.get('experiencia')
        if len(experiencia.strip()) < 10:
            raise forms.ValidationError("Por favor comparte una experiencia más detallada (mínimo 10 caracteres)")
        return experiencia.strip()
    

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = ConsultaCrochet
        fields = ['correo', 'tipo_consulta', 'nivel', 'proyecto', 'descripcion', 'urgencia']
        widgets = {
            'correo': forms.EmailInput(attrs={
                'placeholder': 'ejemplo@correo.com',
                'required': True
            }),
            'tipo_consulta': forms.Select(attrs={
                'class': 'select-consulta',
                'required': True
            }),
            'nivel': forms.Select(attrs={
                'class': 'select-nivel',
                'required': True
            }),
            'proyecto': forms.TextInput(attrs={
                'placeholder': 'Ej: Amigurumi de oso, mantel de flores, etc.',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Describe detalladamente tu duda o el problema que estás enfrentando...',
                'rows': 5,
                'required': True
            }),
            'urgencia': forms.Select(attrs={
                'class': 'select-urgencia',
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        # Extraer 'usuario' de kwargs antes de llamar al padre
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        # Si hay un usuario, establecer el correo por defecto
        if usuario:
            self.fields['correo'].initial = usuario.correo