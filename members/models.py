from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=150)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)

    @property
    def email(self):
        return self.correo

    def __str__(self):
        return self.nombre


class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comentario de {self.usuario.nombre}"


from django.db import models

class Nota(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.nombre}"



from django.db import models
class ExperienciaTutorial(models.Model):
    # Opciones para dificultad
    OPCIONES_DIFICULTAD = [
        ('muy_facil', 'Muy fácil'),
        ('facil', 'Fácil'),
        ('moderado', 'Moderado'),
        ('desafiante', 'Desafiante'),
        ('muy_dificil', 'Muy difícil'),
    ]
    
    # Opciones para recomendación
    OPCIONES_RECOMENDACION = [
        ('si', 'Sí, definitivamente'),
        ('tal_vez', 'Tal vez, depende'),
        ('no', 'No lo recomendaría'),
    ]
    
    # Campos del modelo
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tutorial = models.CharField(max_length=100, verbose_name="Tutorial completado")
    dificultad = models.CharField(
        max_length=20, 
        choices=OPCIONES_DIFICULTAD, 
        verbose_name="Nivel de dificultad"
    )
    tiempo = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name="Tiempo que tomó"
    )
    experiencia = models.TextField(verbose_name="Experiencia personal")
    recomendacion = models.CharField(
        max_length=10, 
        choices=OPCIONES_RECOMENDACION, 
        verbose_name="¿Lo recomendarías?"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Experiencia de Tutorial"
        verbose_name_plural = "Experiencias de Tutoriales"
        ordering = ['-fecha_creacion']  # Más recientes primero
    
    def __str__(self):
        return f"{self.usuario.nombre} - {self.tutorial}"


class ConsultaCrochet(models.Model):
    OPCIONES_TIPO = [
        ('tecnica', 'Técnica específica'),
        ('patron', 'Interpretación de patrón'),
        ('materiales', 'Selección de materiales'),
        ('problema', 'Problema con un proyecto'),
        ('diseno', 'Diseño personalizado'),
        ('otro', 'Otro'),
    ]
    
    OPCIONES_NIVEL = [
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]
    
    OPCIONES_URGENCIA = [
        ('baja', 'Baja (Puede esperar)'),
        ('media', 'Media (En los próximos días)'),
        ('alta', 'Alta (Lo antes posible)'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    correo = models.EmailField(verbose_name="Correo para respuesta")
    tipo_consulta = models.CharField(max_length=20, choices=OPCIONES_TIPO)
    nivel = models.CharField(max_length=15, choices=OPCIONES_NIVEL)
    proyecto = models.CharField(max_length=100, verbose_name="Proyecto o técnica")
    descripcion = models.TextField(verbose_name="Descripción del problema")
    urgencia = models.CharField(max_length=10, choices=OPCIONES_URGENCIA)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    respondida = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.usuario.nombre} - {self.get_tipo_consulta_display()}"