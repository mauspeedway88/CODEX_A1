/**
 * MAUNET V31.0 — MOTOR EXPRESIVO PROCEDURAL
 * ==========================================
 * gesture_engine.js
 *
 * OPCIÓN 2: Generación 100% procedural. No hay variantes pre-definidas.
 * Cada gesto se genera en el momento muestreando rangos paramétricos independientes
 * + modificadores probabilísticos. Matemáticamente imposible repetir la misma pose.
 *
 * 20 estados emocionales × combinatoria infinita de poses.
 * Modificadores apilables: nod, brow_asym, shoulder_pop, chin_up, lean_in, jaw_retórica.
 */

// ══════════════════════════════════════════════════════════════════════════════
// ESPACIOS PARAMÉTRICOS DE GESTOS (Opción 2 — Generación Procedural)
//
// Cada parámetro tiene [min, max] para muestreo uniforme independiente.
// La COMBINACIÓN de parámetros independientes crea diversidad infinita.
// mods: probabilidades de modificadores adicionales que se apilan.
// ══════════════════════════════════════════════════════════════════════════════
const GESTURE_SPACES = {

    // ─────────────────────────────────────────────────────────────────────────
    // ESTADOS POSITIVOS
    // ─────────────────────────────────────────────────────────────────────────

    ALEGRIA_LEVE: {
        hX:  [0.04, 0.12], hY:  [-0.10, 0.10],
        chX: [0.02, 0.08], chY: [-0.06, 0.06],
        bD:  [0.30, 0.65], bI:  [0.30, 0.65],
        sR:  [0.02, 0.08], sL:  [-0.08, -0.02],
        dur: [1800, 2800],
        mods: { nod: 0.25, brow_asym: 0.30, shoulder_pop: 0.20 }
    },

    ALEGRIA_INTENSA: {
        hX:  [0.08, 0.18], hY:  [-0.14, 0.14],
        chX: [0.05, 0.14], chY: [-0.10, 0.10],
        bD:  [0.55, 0.95], bI:  [0.55, 0.95],
        sR:  [0.06, 0.14], sL:  [0.06, 0.14],
        dur: [1600, 2400],
        mods: { nod: 0.60, brow_asym: 0.25, shoulder_pop: 0.70, double_nod: 0.40 }
    },

    CARCAJADA: {
        // Inclinación hacia atrás + hombros activos = risa física
        hX:  [-0.10, -0.02], hY: [-0.12, 0.12],
        chX: [-0.14, -0.04], chY: [-0.08, 0.08],
        bD:  [0.40, 0.90],   bI:  [0.40, 0.90],
        sR:  [0.08, 0.16],   sL:  [0.08, 0.16],
        dur: [2000, 3200],
        mods: { lean_back: 1.0, shoulder_pop: 0.90, bounce: 0.70 }
    },

    ADMIRACION: {
        hX:  [-0.12, 0.02], hY:  [-0.14, 0.14],
        chX: [-0.12, -0.01], chY: [-0.10, 0.10],
        bD:  [0.75, 1.00],  bI:  [0.75, 1.00],
        sR:  [0.05, 0.14],  sL:  [0.05, 0.14],
        dur: [1800, 2600],
        mods: { brow_asym: 0.55, shoulder_pop: 0.60, chin_back: 0.45 }
    },

    APROBACION_MAXIMA: {
        hX:  [0.12, 0.22], hY:  [-0.04, 0.04],
        chX: [0.08, 0.16], chY: [-0.04, 0.04],
        bD:  [0.15, 0.35], bI:  [0.15, 0.35],
        sR:  [0.06, 0.14], sL:  [-0.14, -0.06],
        dur: [1200, 2000],
        mods: { nod: 1.00, double_nod: 0.65, shoulder_pop: 0.50 }
    },

    // ─────────────────────────────────────────────────────────────────────────
    // ESTADOS NEGATIVOS / SERIOS
    // ─────────────────────────────────────────────────────────────────────────

    TRISTEZA: {
        // Cabeza caída, hombros caídos, cejas hacia abajo-interior
        hX:  [0.14, 0.25], hY:  [-0.06, 0.06],
        chX: [0.10, 0.20], chY: [-0.04, 0.04],
        bD:  [-0.20, -0.05], bI: [-0.20, -0.05],
        sR:  [-0.06, -0.01], sL: [0.01, 0.06],
        dur: [2500, 4000],
        mods: { slow_lean: 1.00, brow_asym: 0.20 }
    },

    DESAPROBACION: {
        hX:  [0.06, 0.16], hY:  [-0.08, 0.08],
        chX: [0.04, 0.10], chY: [-0.06, 0.06],
        bD:  [-0.15, -0.02], bI: [-0.15, -0.02],
        sR:  [0.02, 0.08], sL:  [-0.08, -0.02],
        dur: [2000, 3000],
        mods: { brow_asym: 0.45, head_shake: 0.55 }
    },

    FRUSTRACION: {
        hX:  [0.10, 0.20], hY:  [-0.10, 0.10],
        chX: [0.06, 0.14], chY: [-0.08, 0.08],
        bD:  [-0.25, -0.08], bI: [-0.25, -0.08],
        sR:  [0.03, 0.10], sL:  [0.03, 0.10],
        dur: [1600, 2400],
        mods: { head_shake: 0.70, brow_asym: 0.35 }
    },

    // ─────────────────────────────────────────────────────────────────────────
    // ESTADOS DE DISCURSO
    // ─────────────────────────────────────────────────────────────────────────

    ENFASIS_CRITICO: {
        // Proyección frontal intensa — "escucha esto"
        hX:  [0.14, 0.24], hY:  [-0.05, 0.05],
        chX: [0.08, 0.16], chY: [-0.04, 0.04],
        bD:  [-0.12, 0.02], bI:  [-0.12, 0.02],
        sR:  [0.04, 0.12], sL:  [-0.12, -0.04],
        dur: [1400, 2200],
        mods: { lean_in: 0.70, brow_asym: 0.30, chin_down: 0.50 }
    },

    HABLANDO_NORMAL: {
        hX:  [0.03, 0.10], hY:  [-0.08, 0.08],
        chX: [0.01, 0.06], chY: [-0.06, 0.06],
        bD:  [0.05, 0.20], bI:  [0.05, 0.20],
        sR:  [0.01, 0.07], sL:  [-0.07, -0.01],
        dur: [1500, 2200],
        mods: { brow_asym: 0.40, shoulder_pop: 0.20 }
    },

    REFLEXION_PAUSA: {
        // Mirada hacia arriba-diagonal — procesando internamente
        hX:  [-0.20, -0.08], hY: [-0.18, 0.18],
        chX: [0.02, 0.10],   chY: [-0.10, 0.10],
        bD:  [0.20, 0.50],   bI:  [0.20, 0.50],
        sR:  [-0.02, 0.05],  sL:  [-0.05, 0.02],
        dur: [1800, 2800],
        mods: { brow_asym: 0.60, chin_up: 0.40 }
    },

    TRANSICION: {
        // Barrido lateral — cambio de tema
        hX:  [0.02, 0.08], hY:  [0.18, 0.32],
        chX: [0.01, 0.05], chY: [0.10, 0.20],
        bD:  [0.10, 0.30], bI:  [0.10, 0.30],
        sR:  [0.02, 0.08], sL:  [-0.04, 0.02],
        dur: [600, 900],
        mods: { sweep_return: 1.00 }  // siempre vuelve al centro
    },

    // ─────────────────────────────────────────────────────────────────────────
    // ESTADOS INTERACTIVOS
    // ─────────────────────────────────────────────────────────────────────────

    PREGUNTA_ACTIVA: {
        // Ladeo de curiosidad hacia el alumno
        hX:  [0.08, 0.16], hY:  [-0.18, 0.18],
        chX: [0.03, 0.08], chY: [-0.12, 0.12],
        bD:  [0.60, 1.00], bI:  [0.30, 0.80],
        sR:  [0.01, 0.08], sL:  [-0.08, -0.01],
        dur: [2000, 2800],
        mods: { brow_asym: 0.80, head_tilt: 0.70, lean_in: 0.40 }
    },

    AFIRMACION_INTENSA: {
        hX:  [0.10, 0.20], hY:  [-0.04, 0.04],
        chX: [0.05, 0.12], chY: [-0.04, 0.04],
        bD:  [0.10, 0.30], bI:  [0.10, 0.30],
        sR:  [0.04, 0.12], sL:  [-0.12, -0.04],
        dur: [1200, 1800],
        mods: { nod: 1.00, double_nod: 0.55, brow_asym: 0.25 }
    },

    REACCION_ESTUDIANTE: {
        hX:  [-0.06, 0.08], hY:  [-0.12, 0.12],
        chX: [-0.06, 0.06], chY: [-0.08, 0.08],
        bD:  [0.50, 1.00],  bI:  [0.50, 1.00],
        sR:  [0.04, 0.14],  sL:  [0.04, 0.14],
        dur: [1400, 2200],
        mods: { brow_asym: 0.65, shoulder_pop: 0.55, nod: 0.40 }
    },

    CURIOSIDAD: {
        hX:  [0.04, 0.12], hY:  [-0.22, 0.22],
        chX: [0.02, 0.08], chY: [-0.14, 0.14],
        bD:  [0.40, 0.85], bI:  [0.20, 0.65],
        sR:  [0.02, 0.10], sL:  [-0.10, -0.02],
        dur: [2000, 3000],
        mods: { brow_asym: 0.85, head_tilt: 0.75, lean_in: 0.30 }
    },

    SORPRESA_MAXIMA: {
        // Retroceso + cejas al máximo — el más dramático
        hX:  [-0.14, -0.02], hY: [-0.16, 0.16],
        chX: [-0.16, -0.04], chY: [-0.12, 0.12],
        bD:  [0.88, 1.00],   bI:  [0.88, 1.00],
        sR:  [0.10, 0.18],   sL:  [0.10, 0.18],
        dur: [1600, 2400],
        mods: { chin_back: 1.00, shoulder_pop: 0.80, brow_asym: 0.30 }
    },

    // ─────────────────────────────────────────────────────────────────────────
    // ESTADOS DE ESCUCHA Y ATENCIÓN
    // ─────────────────────────────────────────────────────────────────────────

    ESCUCHANDO: {
        hX:  [0.08, 0.18], hY:  [-0.12, 0.12],
        chX: [0.04, 0.10], chY: [-0.06, 0.06],
        bD:  [0.55, 0.90], bI:  [0.55, 0.90],
        sR:  [0.03, 0.10], sL:  [-0.06, 0.02],
        dur: [3000, 5000],
        mods: { brow_asym: 0.50, head_tilt: 0.45, lean_in: 0.60 }
    },

    PENSANDO: {
        hX:  [-0.35, -0.22], hY: [0.14, 0.38],
        chX: [0.04,  0.12],  chY: [0.08, 0.24],
        bD:  [0.28, 0.55],   bI:  [0.15, 0.45],
        sR:  [-0.02, 0.06],  sL:  [-0.06, 0.02],
        dur: [2000, 3500],
        mods: { brow_asym: 0.70, chin_up: 0.55 }
    },

    NEUTRAL: {
        hX:  [0.02, 0.08], hY:  [-0.06, 0.06],
        chX: [0.00, 0.04], chY: [-0.04, 0.04],
        bD:  [0.02, 0.12], bI:  [0.02, 0.12],
        sR:  [0.00, 0.04], sL:  [-0.04, 0.00],
        dur: [2500, 3500],
        mods: { brow_asym: 0.20 }
    },

    // ESPECIAL: Giro hacia pizarra (contextual, no emocional)
    LOOK_BOARD: {
        hX:  [0.02, 0.08], hY:  [0.28, 0.42],
        chX: [0.01, 0.05], chY: [0.14, 0.22],
        bD:  [0.12, 0.28], bI:  [0.10, 0.22],
        sR:  [0.02, 0.08], sL:  [-0.04, 0.02],
        dur: [2500, 4000],
        mods: {} // sin modificadores — acción dirigida, no emocional
    },
};

// ══════════════════════════════════════════════════════════════════════════════
// FUNCIÓN DE MUESTREO PROCEDURAL
// ══════════════════════════════════════════════════════════════════════════════

/** Muestrea uniformemente en [min, max] */
function rng(min, max) { return min + Math.random() * (max - min); }

/** Aplica modificadores probabilísticos sobre la pose generada */
function applyMods(pose, mods) {
    if (!mods) return;

    // NOD — asentimiento (movimiento secuencial de pitch)
    if (mods.nod && Math.random() < mods.nod) {
        pose._nod = true;
    }
    // DOUBLE_NOD — doble asentimiento
    if (mods.double_nod && Math.random() < mods.double_nod) {
        pose._doubleNod = true;
    }
    // BROW_ASYM — una ceja diferente a la otra (más natural)
    if (mods.brow_asym && Math.random() < mods.brow_asym) {
        const delta = rng(-0.25, 0.25);
        pose.bD = Math.max(-0.3, Math.min(1.0, pose.bD + delta));
    }
    // SHOULDER_POP — hombro sube y baja (énfasis físico)
    if (mods.shoulder_pop && Math.random() < mods.shoulder_pop) {
        pose._shoulderPop = Math.random() < 0.5 ? 'R' : 'L';
    }
    // LEAN_IN — refuerza la inclinación hacia adelante
    if (mods.lean_in && Math.random() < mods.lean_in) {
        pose.hX  = Math.min(0.28, pose.hX + rng(0.04, 0.10));
        pose.chX = Math.min(0.18, pose.chX + rng(0.02, 0.06));
    }
    // CHIN_UP — mirada hacia arriba
    if (mods.chin_up && Math.random() < mods.chin_up) {
        pose.hX = -Math.abs(pose.hX) - rng(0.05, 0.12);
    }
    // CHIN_BACK — retroceso dramático (para sorpresa)
    if (mods.chin_back && Math.random() < mods.chin_back) {
        pose.hX  = -Math.abs(rng(0.04, 0.10));
        pose.chX = -Math.abs(rng(0.06, 0.14));
    }
    // CHIN_DOWN — mirada grave/enfática
    if (mods.chin_down && Math.random() < mods.chin_down) {
        pose.hX = Math.abs(pose.hX) + rng(0.02, 0.08);
    }
    // HEAD_TILT — fuerza un lado aleatorio (curiosidad/pregunta)
    if (mods.head_tilt && Math.random() < mods.head_tilt) {
        pose.hY = (Math.random() < 0.5 ? 1 : -1) * (Math.abs(pose.hY) + rng(0.05, 0.12));
    }
    // HEAD_SHAKE — negación sutil (desaprobación)
    if (mods.head_shake && Math.random() < mods.head_shake) {
        pose._headShake = true;
    }
    // LEAN_BACK — retroceso físico (carcajada, sorpresa)
    if (mods.lean_back && Math.random() < mods.lean_back) {
        pose.hX  = -Math.abs(rng(0.06, 0.14));
        pose.chX = -Math.abs(rng(0.08, 0.18));
    }
    // BOUNCE — rebote de hombros (risa)
    if (mods.bounce && Math.random() < mods.bounce) {
        pose._bounce = true;
    }
    // SLOW_LEAN — llegada lenta (tristeza)
    if (mods.slow_lean) { pose._slow = true; }
    // SWEEP_RETURN — retorno al centro (transición)
    if (mods.sweep_return) { pose._sweepReturn = true; }
}

// ══════════════════════════════════════════════════════════════════════════════
// DISPATCHER PRINCIPAL — executeGesture()
// ══════════════════════════════════════════════════════════════════════════════

window._lastGestureName = null;

window.executeGesture = function(name, intensityOverride) {
    const space = GESTURE_SPACES[name];
    if (!space || !window.maunetSetGoals) return;

    // ── Generar pose 100% procedural ────────────────────────────────────────
    const pose = {
        hX:  rng(...space.hX),
        hY:  rng(...space.hY),
        chX: rng(...space.chX),
        chY: rng(...space.chY),
        bD:  rng(...space.bD),
        bI:  rng(...space.bI),
        sR:  rng(...space.sR),
        sL:  rng(...space.sL),
        dur: rng(...space.dur),
    };

    // ── Aplicar modificadores probabilísticos ─────────────────────────────
    applyMods(pose, space.mods);

    // ── Intensidad opcional — x2.0 cuando viene del habla ────────────────
    const k = intensityOverride || 1.0;
    // Clamps generosos para que intensity=2.0 sea claramente visible
    const clamp = (v, mn, mx) => Math.max(mn, Math.min(mx, v));

    window.maunetSetGoals({
        headX:   clamp(pose.hX  * k, -0.46,  0.46),
        headY:   clamp(pose.hY  * k, -0.35,  0.35),  // [V31.3] Limite estricto de rotación lateral (yaw)
        chestX:  clamp(pose.chX * k, -0.30,  0.30),
        chestY:  clamp(pose.chY * k, -0.38,  0.38),
        browD:   clamp(pose.bD  * k, -0.30,  1.35),  // cejas amplificadas
        browI:   clamp(pose.bI  * k, -0.30,  1.35),
        shouldR: clamp(pose.sR  * k, -0.22,  0.22),
        shouldL: clamp(pose.sL  * k, -0.22,  0.22),
    });

    window._lastGestureName = name;
    const dur = Math.round(pose.dur);

    // ── Ejecutar comportamientos secuenciales (mods con timing) ──────────
    if (pose._nod) {
        const base = clamp(pose.hX * k, -0.46, 0.46);
        setTimeout(() => window.maunetSetGoals({ headX: base + 0.18 }), 160);
        setTimeout(() => window.maunetSetGoals({ headX: base - 0.06 }), 340);
        setTimeout(() => window.maunetSetGoals({ headX: base + 0.06 }), 500);
    }

    if (pose._doubleNod) {
        const base = clamp(pose.hX * k, -0.46, 0.46);
        setTimeout(() => window.maunetSetGoals({ headX: base + 0.20 }), 650);
        setTimeout(() => window.maunetSetGoals({ headX: base - 0.05 }), 820);
        setTimeout(() => window.maunetSetGoals({ headX: base + 0.08 }), 980);
    }

    if (pose._shoulderPop) {
        const side   = pose._shoulderPop === 'R' ? 'shouldR' : 'shouldL';
        const popDir = pose._shoulderPop === 'R' ? 1 : -1;
        setTimeout(() => window.maunetSetGoals({ [side]: 0.20 * popDir }), 200);
        setTimeout(() => window.maunetSetGoals({ [side]: 0.05 * popDir }), 450);
    }

    if (pose._headShake) {
        const dir = Math.random() < 0.5 ? 1 : -1;
        setTimeout(() => window.maunetSetGoals({ headY:  0.24 * dir  }), 0);
        setTimeout(() => window.maunetSetGoals({ headY: -0.20 * dir  }), 240);
        setTimeout(() => window.maunetSetGoals({ headY:  0.14 * dir  }), 460);
        setTimeout(() => window.maunetSetGoals({ headY:  0           }), 650);
    }

    if (pose._bounce) {
        [0, 280, 560, 840].forEach((t, i) => {
            const up = i % 2 === 0 ? 0.20 : 0.08;
            setTimeout(() => window.maunetSetGoals({ shouldR: up, shouldL: up }), t);
        });
    }

    if (pose._sweepReturn) {
        setTimeout(() => window.maunetSetGoals({ headY: 0, chestY: 0 }), dur);
    }

    // ── Auto-restauración: solo cuando NO está hablando ──────────────────
    if (!pose._sweepReturn) {
        setTimeout(() => {
            const state = window.maunetGetState ? window.maunetGetState() : {};
            if (!state.isSpeaking && window._lastGestureName === name) {
                window.executeGesture('NEUTRAL', 0.5);
            }
        }, dur + Math.random() * 200);
    }

    console.log(`[V31 GESTURE] ${name} ×${k} → hX:${(pose.hX*k).toFixed(2)} hY:${(pose.hY*k).toFixed(2)} bD:${(pose.bD*k).toFixed(2)} dur:${dur}ms`);
};

// ══════════════════════════════════════════════════════════════════════════════
// TRIGGERS SEMÁNTICOS (ES + EN)
// ══════════════════════════════════════════════════════════════════════════════
const GESTURE_TRIGGERS = [
    { pattern: /\b(importante|atenci[oó]n|f[ií]jate|recuerda|crucial|fundamental|escucha bien|key|important|listen up|pay attention|nota que)\b/i,          gesture: 'ENFASIS_CRITICO'     },
    { pattern: /\b(incre[ií]ble|wow|impresionante|brillante|amazing|wonderful|genial|fascinante|asombroso|extraordinario|formidable)\b/i,                     gesture: 'ADMIRACION'          },
    { pattern: /\b(sorprendente|¡qué sorpresa|no lo puedo creer|jamás lo hubiera|asombrosa|unbelievable|shocking|mind-blowing)\b/i,                           gesture: 'SORPRESA_MAXIMA'     },
    { pattern: /\b(¿sab[ií]as|curiosamente|interesante|¿te preguntas|did you know|interesting|fascinantemente|curioso dato)\b/i,                             gesture: 'CURIOSIDAD'          },
    { pattern: /\b(¿y t[uú]|¿qu[eé] piensas|¿recuerdas|¿puedes|qu[eé] opinas|what do you think|can you|do you remember|cuéntame)\b/i,                       gesture: 'PREGUNTA_ACTIVA'     },
    { pattern: /\b(exactamente|correcto|perfecto|muy bien|excelente|as[ií] es|eso es|effectively|great|good job|right|brillante respuesta)\b/i,               gesture: 'AFIRMACION_INTENSA'  },
    { pattern: /\b(¡qu[eé] bien|fantástico|maravilloso|lo lograste|excelente trabajo|wonderful|you did it|great job|congratulations|felicidades)\b/i,         gesture: 'ALEGRIA_INTENSA'     },
    { pattern: /\b(jaja|haha|qué gracioso|es chistoso|hilarante|funny|hilarious|me hace reír|me divierte)\b/i,                                               gesture: 'CARCAJADA'           },
    { pattern: /\b(la pizarra|en la pizarra|aqu[ií]|mira esto|observa|ve esto|look at this|observe|the board|como ven|como puedes ver)\b/i,                   gesture: 'LOOK_BOARD'          },
    { pattern: /\b(pensemos|veamos|reflexion[ea]|analicemos|consideremos|let.s think|hmm|buena pregunta|interesante pregunta|un momento)\b/i,                 gesture: 'REFLEXION_PAUSA'     },
    { pattern: /\b(ahora bien|siguiente|pasemos a|cambiando de tema|por otro lado|siguiente punto|now then|moving on|continuemos|ahora vemos)\b/i,            gesture: 'TRANSICION'          },
    { pattern: /\b(¿entendiste|¿me sigues|¿tiene sentido|est[aá] claro|do you understand|are you following|¿lo capt[as]|¿quedó claro)\b/i,                   gesture: 'REACCION_ESTUDIANTE' },
    { pattern: /\b(lamentablemente|es una pena|qué triste|no es lo mejor|unfortunately|sadly|that.s a shame|lo siento|lo sentimos)\b/i,                      gesture: 'TRISTEZA'            },
    { pattern: /\b(no es correcto|eso no es así|hay un error|equivocado|incorrect|that.s not right|actually no|no del todo|déjame corregir)\b/i,             gesture: 'DESAPROBACION'       },
];

/** Escanea texto y retorna el primer gesto disparado, o null */
window.scanTextForGestures = function(text) {
    if (!text) return null;
    for (const t of GESTURE_TRIGGERS) {
        if (t.pattern.test(text)) return t.gesture;
    }
    return null;
};

// ══════════════════════════════════════════════════════════════════════════════
// ESCUCHA ACTIVA PROCEDURAL — Micro-gestos únicos, sin repetición
// ══════════════════════════════════════════════════════════════════════════════

/** Genera un micro-gesto de escucha activa, 100% procedural */
function generateListeningMicroGesture() {
    if (!window.maunetSetGoals) return;

    // Elegir aleatoriamente qué dimensión mover (combinaciones siempre únicas)
    const moves = [];
    if (Math.random() < 0.65) moves.push('nod');
    if (Math.random() < 0.50) moves.push('brow');
    if (Math.random() < 0.40) moves.push('tilt');
    if (Math.random() < 0.35) moves.push('shoulder');
    if (Math.random() < 0.30) moves.push('lean');
    if (moves.length === 0)    moves.push('brow'); // siempre al menos uno

    const patch = {};

    if (moves.includes('nod')) {
        const base = rng(0.09, 0.16);
        window.maunetSetGoals({ headX: base });
        setTimeout(() => window.maunetSetGoals({ headX: base - rng(0.05, 0.10) }), rng(200, 300));
        setTimeout(() => window.maunetSetGoals({ headX: base - rng(0.02, 0.06) }), rng(420, 550));
    }
    if (moves.includes('brow')) {
        patch.browD = rng(0.50, 0.90);
        patch.browI = rng(0.50, 0.90); // asimétrico por muestreo independiente
        if (Math.random() < 0.30) patch.browD -= rng(0.10, 0.25); // ceño leve en una
    }
    if (moves.includes('tilt')) {
        const dir   = Math.random() < 0.5 ? 1 : -1;
        patch.headY = dir * rng(0.08, 0.16);
        setTimeout(() => window.maunetSetGoals({ headY: dir * rng(0.02, 0.06) }), rng(500, 800));
    }
    if (moves.includes('shoulder')) {
        const side  = Math.random() < 0.5 ? 'shouldR' : 'shouldL';
        const dir   = side === 'shouldR' ? 1 : -1;
        patch[side] = dir * rng(0.06, 0.13);
        setTimeout(() => window.maunetSetGoals({ [side]: dir * rng(0.01, 0.04) }), rng(400, 600));
    }
    if (moves.includes('lean')) {
        patch.headX  = rng(0.10, 0.18);
        patch.chestX = rng(0.04, 0.10);
        setTimeout(() => window.maunetSetGoals({ headX: rng(0.06, 0.10), chestX: rng(0.02, 0.05) }), rng(600, 900));
    }

    if (Object.keys(patch).length > 0) {
        window.maunetSetGoals(patch);
    }
}

window.startActiveListeningLoop = function() {
    const state = window.maunetGetState ? window.maunetGetState() : {};
    if (!state.isListening) return;

    generateListeningMicroGesture();

    // Ritmo orgánico: 1.2s – 3.8s (variable, imprevisible)
    setTimeout(window.startActiveListeningLoop, 1200 + Math.random() * 2600);
};

console.log('[MAUNET V31.0] 🎭 Motor Expresivo Procedural — 20 estados × combinatoria infinita | 14 triggers semánticos bilingües');
