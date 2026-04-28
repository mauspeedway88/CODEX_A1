// Test V56.0: Verificar que MEMORY_QUERY_PATTERN detecta las frases coloquiales que antes fallaban

const MEMORY_QUERY_PATTERN = /hemos hablado|hemos platicado|de qu[eé] (hablamos|platicamos|tratamos|conversamos)|qu[eé] hemos (hablado|visto|platicado|tratado)|historial|recuerdas|te acuerdas|recordas|te acordas|qu[eé] (sab[eé]s) de mi|primera (plat|convers|vez|pregunta)|segunda (plat|convers|vez|pregunta)|tercera (plat|convers|vez|pregunta)|cuarta (plat|convers|vez|pregunta)|quinta (plat|convers|vez|pregunta)|ultima (plat|convers|vez|pregunta)|primera pl[aá]tica|primera conversaci[oó]n|primer tema|primer pregun|segund[ao] (tema|pregun)|tercer[ao] (tema|pregun)|cu[aá]ndo (hablamos|platicamos)|res[uú]meme|resume.*conversac|temas.*anteriores|qu[eé] aprendimos|ya hablamos de|mencionaste|hablamos ayer|platicamos ayer|conversamos ayer|no hemos hablado|hemos visto|lo que hemos|qu[eé] temas|nuestras conversaciones|conversaciones anteriores|sesiones anteriores|qu[eé] fue lo (primero|[uú]ltimo)|cu[aá]l fue (mi|la|el) (primer|segund|tercer|cuart|quint|[uú]ltim)|pregunta que te hice|lo primero que (te|le) pregu|lo segundo que|primer[ao] interacc|de qu[eé] trat[oó] (la|mi|tu) primer|qu[eé] (hice|pregunt[eé]) primero|principio de la sesi[oó]n|inicio de nuestra|antes de este tema|antes que esto|lo que pregunt[eé] (hoy|antes|ayer)|qu[eé] te pregunt[eé]|lo que te dije|qu[eé] dij[ei]ste|qu[eé] me contaste|de qu[eé] habl[eé]|qu[eé] habl[aá]bamos|nuestra (ultima|previa|anterior) conversaci[oó]n|repas[aá]me|refresc[aá]me|recu[eé]rdame|tenemos historial|tienes memoria|qu[eé] recuerdas|qu[eé] recorda[sz]|sobre qu[eé] habl[aá]bamos|temas pasados|lo anterior|qu[eé] fue lo [uú]ltimo (que|de)|convers\w*\s+(primer|segund|tercer|cuart|quint|[uú]ltim)|tema\s+(primer|segund|tercer|cuart|quint|[uú]ltim)|te quedast|te cortast|quedaste en|platicamos hace|hablamos hace|hace \d+ d[ií]as?|me dijiste|me hablaste|me contaste de|me explicaste|viste de|acordate|rep[ií]te(me|lo)|repet[ií](me|lo)|d[ei]me otra vez|dec[ií]me otra vez|tema principal|hablaste de|plat[ií]came|lo de ayer|lo de hoy|qu[eé] onda con lo|despu[eé]s de|antes de eso|seguido de|siguiente tema|tema.*(despu[eé]s|siguiente|anterior)|que me dijiste|que me hablaste|hace rato.*(dijiste|hablaste|explicaste|contaste)|de qu[eé] (enfermedad|tema|cosa)|cu[aá]l (enfermedad|tema)|recordar(lo|la)|quiero recordar|vimos de|hablamos de/i;

// Los inputs que ANTES fallaban y ahora deben pasar
const tests = [
    { input: "hace rato que me dijiste de ifel", expect: true },
    { input: "repetime Cuál fue el primer tema", expect: true },
    { input: "viste de la candidiasis", expect: true },
    { input: "el tema principal de ayer", expect: true },
    { input: "Cuál es el primer tema de días anteriores", expect: true },
    { input: "resumíme todos los temas de hace 3 días", expect: true },
    { input: "cuando fue que hablamos de la torre eifel", expect: true },
    { input: "de que enfermedad sexual te pregunte", expect: true },
    { input: "cual fue el tema seguido despues de hablar de la torre eifel", expect: true },
    { input: "yome acuerdo quemehablastes de una enfermedad , despues de la torre eifel", expect: true },
    // Sanity: preguntas normales NO deben activar el pattern
    { input: "explicame la polinización vía abejas", expect: false },
    { input: "que es un motor de gasolina rotativo", expect: false },
    { input: "hola como estas", expect: false },
    { input: "computadora macintosh 126k de los 80s", expect: false },
];

let pass = 0, fail = 0;
for (const t of tests) {
    const result = MEMORY_QUERY_PATTERN.test(t.input);
    const ok = result === t.expect;
    if (ok) {
        pass++;
    } else {
        fail++;
        console.log(`❌ FAIL: "${t.input}" → got ${result}, expected ${t.expect}`);
    }
}
console.log(`\n${pass}/${tests.length} passed, ${fail} failed.`);
if (fail === 0) console.log("✅ ALL TESTS PASSED!");
