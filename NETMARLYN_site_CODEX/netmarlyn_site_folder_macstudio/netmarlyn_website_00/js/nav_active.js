document.addEventListener("DOMContentLoaded", function () {
    // --- SISTEMA INTELIGENTE DE MENÚ ACTIVO ---
    // Detectar qué página está abierta y pintar ese link de verde neón
    const navLinks = document.querySelectorAll(".top-nav a");
    
    // Obtener el nombre del archivo actual (ejemplo: "colegios.html" o "")
    let currentPath = window.location.pathname.split("/").pop();
    
    // Si la ruta está vacía o es la de inicio por defecto
    if (currentPath === "" || currentPath === "/") {
        currentPath = "index.html";
    }
    
    // Limpiar cualquier active previo hardcodeado en el HTML
    navLinks.forEach(link => link.classList.remove("active"));
    
    // Asignar active dinámicamente
    navLinks.forEach(link => {
        // Limpiar el href del link (quitar ?v=...) para comparar solo el nombre del archivo
        let linkHref = link.getAttribute("href").split("?")[0];
        
        // Si el enlace apunta a la página donde estamos parados
        if (linkHref === currentPath) {
            link.classList.add("active");
        }
    });
});
