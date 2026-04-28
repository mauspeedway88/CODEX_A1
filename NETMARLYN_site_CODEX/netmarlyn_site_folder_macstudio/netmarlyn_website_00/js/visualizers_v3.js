document.addEventListener("DOMContentLoaded", function () {
    const visitasBar = document.getElementById("visitas-bar-top");
    let baseHeight = 0;
    let visitasEnElAire = 0;

    function dispararVisitaFugaz() {
        if (!visitasBar) return;
        
        visitasEnElAire++;
        
        let newWidth = Math.min(100, baseHeight + (visitasEnElAire * 5)); 
        visitasBar.style.width = newWidth + "%";
        
        setTimeout(() => {
            visitasEnElAire--;
            if (visitasEnElAire < 0) visitasEnElAire = 0;
            
            let fallWidth = Math.min(100, baseHeight + (visitasEnElAire * 5));
            visitasBar.style.width = fallWidth + "%";
        }, 1000);
    }

    const URL_CONTADOR = '/api/live_stats';
    let ultimasVisitasConocidas = -1;

    setInterval(() => {
        fetch(URL_CONTADOR)
            .then(res => res.json())
            .then(data => {
                const totalActual = data.total_visitas || 0;
                
                if (ultimasVisitasConocidas === -1) {
                    ultimasVisitasConocidas = totalActual;
                    return;
                }
                
                if (totalActual > ultimasVisitasConocidas) {
                    const diferencia = totalActual - ultimasVisitasConocidas;
                    
                    for(let i=0; i < diferencia; i++) {
                        setTimeout(() => dispararVisitaFugaz(), i * 150);
                    }
                    
                    ultimasVisitasConocidas = totalActual;
                }
            })
            .catch(() => {});
    }, 500); 

    // AUTO-REGISTRO: avisar que YO entré
    fetch('/api/visitas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            path: window.location.pathname,
            is_new: !sessionStorage.getItem('nm_visitado'),
            timestamp: new Date().toISOString()
        })
    }).then(() => {
        sessionStorage.setItem('nm_visitado', 'true');
    }).catch(() => {});

});
