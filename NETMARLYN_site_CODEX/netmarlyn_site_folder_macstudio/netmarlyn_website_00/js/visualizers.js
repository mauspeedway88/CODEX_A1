document.addEventListener("DOMContentLoaded", function () {
    const visitasBar = document.getElementById("visitas-bar");
    let baseHeight = 10;
    let visitasEnElAire = 0;

    function dispararVisitaFugaz() {
        if (!visitasBar) return;
        
        visitasEnElAire++;
        let newHeight = Math.min(100, baseHeight + (visitasEnElAire * 5)); 
        
        visitasBar.style.height = newHeight + "%";
        visitasBar.style.backgroundColor = "#ffffff";
        visitasBar.style.boxShadow = "0 0 25px #ffffff";
        
        setTimeout(() => {
            visitasBar.style.backgroundColor = "#00e5ff";
            visitasBar.style.boxShadow = "0 0 15px #00e5ff";
        }, 200); 
        
        setTimeout(() => {
            visitasEnElAire--;
            if (visitasEnElAire < 0) visitasEnElAire = 0;
            
            let fallHeight = Math.min(100, baseHeight + (visitasEnElAire * 5));
            visitasBar.style.height = fallHeight + "%";
        }, 500);
    }

    // EL MOTOR OFICIAL DE NETMARLYN (SÚPER ROBUSTO Y ESCALABLE)
    // Para aguantar 2 millones de monos cerotes entrando al mismo tiempo,
    // NO usamos servicios de terceros gratis. Le preguntamos directamente
    // y en secreto a la Mac Mini (nuestro propio hierro).
    
    const URL_CONTADOR = '/api/live_stats';
    let ultimasVisitasConocidas = -1;

    // Preguntamos calladitos a nuestra propia máquina cada medio segundo.
    setInterval(() => {
        fetch(URL_CONTADOR)
            .then(res => res.json())
            .then(data => {
                const totalActual = data.total_visitas || 0;
                
                // Si es la primera vez, solo guardamos la cantidad actual que tiene la Mac Mini
                if (ultimasVisitasConocidas === -1) {
                    ultimasVisitasConocidas = totalActual;
                    return;
                }
                
                // Si el motor dice que la base de datos creció... disparar luces
                if (totalActual > ultimasVisitasConocidas) {
                    const diferencia = totalActual - ultimasVisitasConocidas;
                    
                    // Disparamos un flashazo por cada nueva persona
                    for(let i=0; i < diferencia; i++) {
                        setTimeout(() => dispararVisitaFugaz(), i * 150);
                    }
                    
                    ultimasVisitasConocidas = totalActual;
                }
            })
            .catch(() => {}); // Si la Mac Mini no responde (error 503), no mostramos error feo.
    }, 500); 

});
