
const enlaceTel = document.getElementById("telefono");
const esMovil = /Mobi|Android|iPhone/i.test(navigator.userAgent);

if (!esMovil) {
  enlaceTel.addEventListener("click", function(event) {
    event.preventDefault();
    alert("Llama al número desde tu teléfono móvil.");
  });
}