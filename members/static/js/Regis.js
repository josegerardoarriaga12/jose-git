
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const email = form.querySelector("input[type='email']");
    const password = form.querySelectorAll("input[type='password']")[0];
    const confirmPassword = form.querySelectorAll("input[type='password']")[1];

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.value)) {
            alert("Por favor, introduce un correo electrónico válido.");
            return;
        }

        if (password.value !== confirmPassword.value) {
            alert("Las contraseñas no coinciden. Por favor, verifica.");
            return;
        }

        alert("✅ ¡Registro exitoso! Te damos la bienevenida a la comunidad de Coco_Crochet");
        
        form.reset();
    });
});

    

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


document.addEventListener('DOMContentLoaded', function() {
    const noteTitle = document.getElementById('id_titulo');
    const noteContent = document.getElementById('id_contenido');
    const charCount = document.getElementById('charCount');
    const saveBtn = document.querySelector('.save-note-btn');
    const noteForm = document.querySelector('.note-creator');
    
    // Contador de caracteres (si quieres mantenerlo)
    if (noteContent && charCount) {
        noteContent.addEventListener('input', function() {
            charCount.textContent = this.value.length;
        });
        
        // Inicializar contador
        charCount.textContent = noteContent.value.length;
    }
    
    // Validación antes de enviar el formulario
    if (noteForm) {
        noteForm.addEventListener('submit', function(e) {
            if (!noteTitle.value.trim() || !noteContent.value.trim()) {
                e.preventDefault(); // Prevenir envío si está vacío
                alert('Por favor, completa tanto el título como el contenido de la nota.');
            }
            // Si los campos están llenos, el formulario se enviará normalmente a Django
        });
    }
    
    // Animaciones para mejorar la experiencia de usuario
    const noteItems = document.querySelectorAll('.note-item');
    noteItems.forEach(item => {
        item.addEventListener('click', function() {
            this.style.transform = 'scale(1.02)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });
    
    // Confirmación mejorada para eliminar notas
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que quieres eliminar esta nota? Esta acción no se puede deshacer.')) {
                e.preventDefault();
            }
        });
    });
    
    // Efecto de carga en el botón guardar
    if (saveBtn) {
        saveBtn.addEventListener('click', function() {
            if (noteTitle.value.trim() && noteContent.value.trim()) {
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';
                this.disabled = true;
                
                // Re-habilitar después de 3 segundos por si hay error
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-save"></i> Guardar Nota';
                    this.disabled = false;
                }, 3000);
            }
        });
    }
});


