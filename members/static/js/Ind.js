const images = [
    "/static/img/est.jpeg",
    "/static/img/colo.jpeg", 
    "/static/img/cora.jpeg",
    "/static/img/lib.jpeg",
    "/static/img/man.jpeg",
    "/static/img/coj.jpeg",
    "/static/img/ram.jpeg",
];

let currentIndex = 0;
const imageElement = document.getElementById("heroImage");

if (imageElement) {
    console.log("✅ Iniciando slideshow con imágenes:", images);
    
    setInterval(() => {
        currentIndex = (currentIndex + 1) % images.length;
        console.log("🔄 Cambiando a:", images[currentIndex]);
        imageElement.src = images[currentIndex];
    }, 2000);
} else {
    console.error("❌ No se encontró el elemento heroImage");
}

// Interactividad para Preguntas Frecuentes (FAQ)
document.addEventListener("DOMContentLoaded", () => {
    const items = document.querySelectorAll(".faq-item h4");

    items.forEach(titulo => {
        titulo.addEventListener("click", () => {
            const parent = titulo.parentElement;
            const activeItem = document.querySelector(".faq-item.active");

            if (activeItem && activeItem !== parent) {
                activeItem.classList.remove("active");
            }

            parent.classList.toggle("active");
        });
    });
});
