from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.utils.crypto import salted_hmac
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib import messages

from .forms import RegistroForm, LoginForm, CustomPasswordResetForm, CustomSetPasswordForm, NotaForm, ComentarioForm, ExperienciaForm, ConsultaForm
from .models import Usuario, Comentario, Nota, ExperienciaTutorial, ConsultaCrochet

def index(request):
    return render(request, 'Index.html')

def sobre_nosotros(request):
    return render(request, 'SobreNosotros.html')

def nuestro_trabajo(request):
    return render(request, 'NuestroTrabajo.html')

def precios(request):
    return render(request, 'Precios.html')

def contacto(request):
    usuario = None
    usuario_id = request.session.get('usuario_id')
    
    if usuario_id:
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            pass
    
    # Inicializar el formulario con el correo del usuario si está logueado
    initial_data = {}
    if usuario:
        initial_data['correo'] = usuario.correo
    
    form = ConsultaForm(initial=initial_data)
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            if usuario:
                consulta.usuario = usuario
            consulta.save()
            messages.success(request, '¡Tu consulta ha sido enviada! Te responderemos pronto.')
            return redirect('contacto')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    
    return render(request, 'Contacto.html', {
        'usuario': usuario,
        'form': form
    })

def cuidados(request):
    return render(request, 'Cuidados.html')

def tutoriales(request):
    # Obtener todas las experiencias para mostrar (más recientes primero)
    experiencias = ExperienciaTutorial.objects.all().order_by('-fecha_creacion')
    
    # Obtener usuario de la sesión si está logueado
    usuario = None
    form = ExperienciaForm()
    
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            pass
    
    # Manejar el envío del formulario de experiencia
    if request.method == 'POST':
        if usuario_id:
            form = ExperienciaForm(request.POST)
            if form.is_valid():
                experiencia = form.save(commit=False)
                experiencia.usuario = usuario
                experiencia.save()
                messages.success(request, '¡Gracias por compartir tu experiencia!')
                return redirect('tutoriales')
            else:
                messages.error(request, 'Por favor corrige los errores en el formulario')
        else:
            messages.error(request, 'Debes iniciar sesión para compartir tu experiencia')
    
    return render(request, 'Tutoriales.html', {
        'usuario': usuario,
        'form': form,
        'experiencias': experiencias
    })

def guardar_experiencia(request):
    """Vista separada para guardar experiencias"""
    if not request.session.get('usuario_id'):
        messages.error(request, 'Debes iniciar sesión para compartir tu experiencia')
        return redirect('tutoriales')
    
    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(id=usuario_id)
    
    if request.method == 'POST':
        form = ExperienciaForm(request.POST)
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.usuario = usuario
            experiencia.save()
            messages.success(request, '¡Gracias por compartir tu experiencia!')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    
    return redirect('tutoriales')

def enviar_consulta(request):
    """Vista para enviar consultas desde el formulario de contacto"""
    if not request.session.get('usuario_id'):
        messages.error(request, 'Debes iniciar sesión para enviar consultas')
        return redirect('contacto')
    
    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(id=usuario_id)
    
    if request.method == 'POST':
        # Inicializar el formulario con el correo del usuario
        initial_data = {'correo': usuario.correo}
        form = ConsultaForm(request.POST, initial=initial_data)
        
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.usuario = usuario
            consulta.save()
            messages.success(request, '¡Tu consulta ha sido enviada! Te responderemos pronto.')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    
    return redirect('contacto')

def comentarios(request):
    if not request.session.get('usuario_id'):
        return redirect('registro')
    
    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(id=usuario_id)
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = usuario
            comentario.save()
            return redirect('comentarios')
    else:
        form = ComentarioForm()
    
    comentarios_lista = Comentario.objects.all().order_by('-fecha_creacion')
    
    return render(request, 'Comentarios.html', {
        'form': form,
        'comentarios': comentarios_lista,
        'usuario_actual': usuario
    })

def equipo(request):
    return render(request, 'Equipo.html')

def nueva(request):
    return render(request, 'Nueva.html')

# 🔹 Registro - CORREGIDO
def registro(request):
    mensaje = ""
    if request.method == 'POST':
        try:
            form = RegistroForm(request.POST)
            
            print("=== DEBUG REGISTRO ===")
            print(f"Form válido: {form.is_valid()}")
            print(f"Datos recibidos: {request.POST}")
            
            if form.is_valid():
                print("✅ Formulario VÁLIDO - Guardando usuario...")
                usuario = form.save()
                # ✅ CORREGIDO: usa 'nombre' en lugar de 'username'
                print(f"✅ Usuario guardado: {usuario.nombre} - ID: {usuario.id}")
                
                request.session['usuario_id'] = usuario.id
                print("✅ Session establecida - Redirigiendo a bienvenida")
                return redirect('bienvenida')
            else:
                print("❌ Formulario INVÁLIDO")
                print(f"Errores: {form.errors}")
                mensaje = "Por favor corrige los errores en el formulario."
                
        except Exception as e:
            print("❌❌❌ ERROR 500 EN REGISTRO ❌❌❌")
            print(f"Tipo de error: {type(e).__name__}")
            print(f"Mensaje: {str(e)}")
            import traceback
            traceback.print_exc()
            mensaje = "Error interno del servidor. Por favor intenta nuevamente."
            
    else:
        form = RegistroForm()
    
    return render(request, 'registro.html', {'form': form, 'mensaje': mensaje})

# 🔹 Login - VERSIÓN CORREGIDA CON DEBUG
def login_view(request):
    mensaje = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        # ✅ AGREGA DEBUG TAMBIÉN AQUÍ
        print("=== DEBUG LOGIN ===")
        print(f"Form válido: {form.is_valid()}")
        print(f"Datos login: {request.POST}")
        
        if form.is_valid():
            print("✅ Login exitoso")
            usuario = form.cleaned_data["usuario"]
            request.session['usuario_id'] = usuario.id
            return redirect('bienvenida')
        else:
            print("❌ Login fallido")
            print(f"Errores login: {form.errors}")
            mensaje = "Correo o contraseña incorrectos."
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'mensaje': mensaje})

def bienvenida(request):
    print("=== INICIANDO BIENVENIDA ===")
    usuario_id = request.session.get('usuario_id')
    print(f"Usuario ID desde session: {usuario_id}")
    
    if not usuario_id:
        print("❌ No hay usuario_id - redirigiendo a login")
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        # ✅ CORREGIDO: usa 'nombre' en lugar de 'username'
        print(f"✅ Usuario encontrado: {usuario.nombre}")
    except Usuario.DoesNotExist as e:
        print(f"❌ Usuario no existe en BD: {e}")
        return redirect('login')
    except Exception as e:
        print(f"❌ Error al obtener usuario: {e}")
        return redirect('login')
    
    notas = Nota.objects.filter(usuario=usuario).order_by('-fecha_creacion')
    print(f"✅ Notas encontradas: {notas.count()}")
    
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.usuario = usuario
            nota.save()
            messages.success(request, 'Nota guardada correctamente')
            return redirect('bienvenida')
    else:
        form = NotaForm()
    
    print("✅ Renderizando bienvenida.html")
    return render(request, 'bienvenida.html', {
        'usuario': usuario,
        'form': form,
        'notas': notas
    })

# 🔹 Eliminar nota
def eliminar_nota(request, nota_id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    
    nota = get_object_or_404(Nota, id=nota_id, usuario_id=usuario_id)
    
    if request.method == 'POST':
        nota.delete()
        messages.success(request, 'Nota eliminada correctamente')
    
    return redirect('bienvenida')

# 🔹 Eliminar experiencia (opcional - si quieres que los usuarios puedan eliminar sus experiencias)
def eliminar_experiencia(request, experiencia_id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    
    experiencia = get_object_or_404(ExperienciaTutorial, id=experiencia_id, usuario_id=usuario_id)
    
    if request.method == 'POST':
        experiencia.delete()
        messages.success(request, 'Experiencia eliminada correctamente')
    
    return redirect('tutoriales')

# 🔹 Logout
def logout_view(request):
    request.session.flush()
    return redirect('login')

# 🔹 Reset contraseña
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = "reset_password.html"
    success_url = reverse_lazy('password_reset_done')
    form_class = CustomPasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        users = form.get_users(email)

        if not users.exists():
            print(f"No se encontró usuario con email: {email}")
            return redirect(self.success_url)

        for user in users:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = salted_hmac("password-reset", str(user.pk)).hexdigest()
            enlace = self.request.build_absolute_uri(f'/reset/{uid}/{token}/')
            print("Enlace de reseteo (local):", enlace)

        return redirect(self.success_url)

# 🔹 Confirmar y cambiar contraseña
def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        usuario = get_object_or_404(Usuario, pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        usuario = None

    if usuario is None:
        messages.error(request, "Enlace inválido")
        return redirect('login')

    if request.method == 'POST':
        form = CustomSetPasswordForm(usuario, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contraseña cambiada correctamente")
            return redirect('login')
    else:
        form = CustomSetPasswordForm(usuario)

    return render(request, "reset_password_confirm.html", {"form": form})



    # En views.py - agrega esta vista
def debug_database(request):
    from django.db import connection
    import json
    
    try:
        # Verificar conexión actual
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE()")
            current_db = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) as total FROM members_usuario")
            total_usuarios = cursor.fetchone()[0]
            
            cursor.execute("SELECT id, nombre, correo FROM members_usuario ORDER BY id DESC LIMIT 5")
            ultimos_usuarios = cursor.fetchall()
        
        db_info = {
            'current_database': current_db,
            'total_usuarios': total_usuarios,
            'ultimos_usuarios': [{'id': u[0], 'nombre': u[1], 'correo': u[2]} for u in ultimos_usuarios],
            'database_config': connection.settings_dict['NAME']
        }
        return JsonResponse(db_info)
    
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'database_config': connection.settings_dict
        })