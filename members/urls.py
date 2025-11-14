from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
     path('', views.index, name='home'),
    path('Index/', views.index, name='index'),
    path('SobreNosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('NuestroTrabajo/', views.nuestro_trabajo, name='nuestro_trabajo'),
    path('Precios/', views.precios, name='precios'),
    path('Contacto/', views.contacto, name='contacto'),
    path('Cuidados/', views.cuidados, name='cuidados'),
    path('Tutoriales/', views.tutoriales, name='tutoriales'),
    path('Comentarios/', views.comentarios, name='comentarios'),
    path('Equipo/', views.equipo, name='equipo'),
    path('Nueva/', views.nueva, name='nueva'),

    # Registro, login, bienvenida y logout
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('bienvenida/', views.bienvenida, name='bienvenida'),
    path('logout/', views.logout_view, name='logout'),

    # Reset de contraseña usando la vista personalizada
    path('reset_password/', 
         views.CustomPasswordResetView.as_view(), 
         name='reset_password'),
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="reset_password_done.html"), 
         name='password_reset_done'),

    # 🔹 Cambiar contraseña desde enlace usando nuestra vista personalizada
    path('reset/<uidb64>/<token>/', 
         views.custom_password_reset_confirm, 
         name='password_reset_confirm'),

    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"), 
         name='password_reset_complete'),

    path('eliminar_nota/<int:nota_id>/', views.eliminar_nota, name='eliminar_nota'),

     path('guardar_experiencia/', views.guardar_experiencia, name='guardar_experiencia'),
    path('eliminar_experiencia/<int:experiencia_id>/', views.eliminar_experiencia, name='eliminar_experiencia'),

     path('enviar_consulta/', views.enviar_consulta, name='enviar_consulta'),

     path('debug-db/', views.debug_database, name='debug_db'),
]


