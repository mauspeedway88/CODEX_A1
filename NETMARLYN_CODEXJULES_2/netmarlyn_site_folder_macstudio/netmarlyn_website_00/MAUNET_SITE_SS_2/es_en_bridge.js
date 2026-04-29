/**
 * MAUNET V27.0 — MOTOR DE BÚSQUEDA UNIVERSAL BILINGÜE
 * =====================================================
 * Provee dos diccionarios globales:
 *   window.ES_TO_EN      → Traducción ES→EN de ~500 conceptos educativos
 *   window.CONCEPT_TO_EMOJI → Concepto EN → Emoji Unicode (chalk fallback)
 *
 * Regla de diseño: Este archivo NUNCA debe contener lógica de renderizado.
 * Solo datos puros. La función findUniversalIcon en main.js los consume.
 */

// ══════════════════════════════════════════════════════════════════════════════
// DICCIONARIO ES → EN  (Español a Inglés para búsqueda en bóveda de iconos)
// ══════════════════════════════════════════════════════════════════════════════
window.ES_TO_EN = {

    // ── Animales ──────────────────────────────────────────────────────────────
    'caballo': 'horse', 'caballos': 'horse', 'yegua': 'horse', 'potro': 'horse',
    'perro': 'dog', 'perros': 'dog', 'cachorro': 'dog',
    'gato': 'cat', 'gatos': 'cat', 'gatito': 'cat',
    'vaca': 'cow', 'toro': 'cow', 'buey': 'cow', 'ternero': 'cow',
    'cerdo': 'pig', 'puerco': 'pig', 'chancho': 'pig',
    'oveja': 'sheep', 'borrego': 'sheep', 'cordero': 'sheep',
    'gallina': 'chicken', 'pollo': 'chicken', 'gallo': 'rooster',
    'pajaro': 'bird', 'ave': 'bird', 'paloma': 'bird',
    'aguila': 'eagle', 'halcon': 'eagle',
    'buho': 'owl', 'lechuza': 'owl',
    'pinguino': 'penguin', 'pato': 'duck',
    'flamenco': 'flamingo', 'loro': 'parrot',
    'pez': 'fish', 'peces': 'fish', 'tiburon': 'shark',
    'delfin': 'dolphin', 'ballena': 'whale', 'pulpo': 'octopus',
    'cangrejo': 'crab', 'langosta': 'lobster',
    'leon': 'lion', 'tigre': 'tiger', 'leopardo': 'tiger',
    'oso': 'bear',  'panda': 'bear',
    'mono': 'monkey', 'gorila': 'gorilla', 'chimpance': 'gorilla',
    'conejo': 'rabbit', 'liebre': 'rabbit',
    'lobo': 'wolf', 'zorro': 'fox',
    'ciervo': 'deer', 'venado': 'deer',
    'jirafa': 'giraffe', 'cebra': 'zebra',
    'elefante': 'elephant', 'rinoceronte': 'rhino', 'hipopotamo': 'hippo',
    'cocodrilo': 'crocodile', 'serpiente': 'snake', 'vibora': 'snake',
    'tortuga': 'turtle', 'rana': 'frog', 'sapo': 'frog',
    'mariposa': 'butterfly', 'abeja': 'bee', 'hormiga': 'ant',
    'insecto': 'bug', 'arana': 'spider', 'mosquito': 'bug',
    'caracol': 'snail', 'dinosaurio': 'dinosaur', 'dragon': 'dragon',
    'unicornio': 'unicorn', 'colibrí': 'bird', 'kolibri': 'bird',
    'pajaro carpintero': 'bird', 'gaviota': 'bird', 'condor': 'eagle',
    'avestruz': 'bird', 'canguro': 'kangaroo', 'koala': 'bear',
    'mapache': 'fox', 'castor': 'beaver', 'armadillo': 'armadillo',

    // ── Naturaleza / Geografía ─────────────────────────────────────────────
    'sol': 'sun', 'luna': 'moon', 'estrella': 'star', 'estrellas': 'star',
    'planeta': 'planet', 'tierra': 'earth', 'marte': 'planet', 'jupiter': 'planet',
    'nube': 'cloud', 'nubes': 'cloud', 'lluvia': 'rain', 'nieve': 'snow',
    'rayo': 'lightning', 'tormenta': 'lightning', 'viento': 'wind',
    'arcoiris': 'rainbow', 'niebla': 'cloud', 'granizo': 'snow',
    'tornado': 'tornado', 'huracan': 'tornado',
    'fuego': 'fire', 'llama': 'fire', 'humo': 'fire',
    'agua': 'water', 'gota': 'water', 'gotas': 'water',
    'oceano': 'ocean', 'mar': 'ocean', 'lago': 'ocean', 'rio': 'water',
    'montana': 'mountain', 'cerro': 'mountain', 'colina': 'mountain',
    'volcan': 'volcano', 'desierto': 'desert', 'selva': 'tree',
    'bosque': 'tree', 'jungla': 'tree', 'pradera': 'grass',
    'arbol': 'tree', 'arboles': 'tree', 'palma': 'palm-tree',
    'cactus': 'cactus', 'flor': 'flower', 'flores': 'flower',
    'rosa': 'rose', 'girasol': 'sunflower', 'tulipan': 'flower',
    'hoja': 'leaf', 'hojas': 'leaf', 'pasto': 'grass', 'cesped': 'grass',
    'planta': 'flower', 'semilla': 'seed', 'fruto': 'fruit',
    'terraemoto': 'mountain', 'tsunami': 'ocean', 'inundacion': 'water',
    'hielo': 'snow', 'glaciar': 'snow', 'cueva': 'mountain',
    'isla': 'island', 'peninsula': 'map', 'continente': 'earth',
    'mapa': 'map', 'globo': 'earth', 'brujula': 'compass',
    'bandera': 'flag', 'piedra': 'mountain', 'roca': 'mountain',
    'arena': 'desert', 'carbon': 'fire', 'diamante': 'diamond',
    'oro': 'diamond', 'plata': 'diamond', 'cristal': 'diamond',
    'cometa': 'comet', 'meteorito': 'comet', 'asteroide': 'comet',
    'galaxia': 'planet', 'universo': 'planet', 'cosmos': 'planet',
    'cohete': 'rocket', 'satellite': 'satellite', 'satelite': 'satellite',
    'espacio': 'planet', 'astronauta': 'rocket',

    // ── Ciencia ────────────────────────────────────────────────────────────
    'atomo': 'atom', 'molecula': 'atom', 'electron': 'atom', 'neutron': 'atom',
    'celula': 'microscope', 'celulas': 'microscope', 'bacteria': 'microscope',
    'virus': 'microscope', 'adn': 'dna', 'gen': 'dna', 'genes': 'dna',
    'cerebro': 'brain', 'mente': 'brain', 'neurona': 'brain',
    'corazon': 'heart', 'pulmon': 'lungs', 'pulmones': 'lungs',
    'hueso': 'bone', 'esqueleto': 'bone', 'musculo': 'bone',
    'sangre': 'heart', 'vena': 'heart', 'arteria': 'heart',
    'microscopio': 'microscope', 'telescopio': 'telescope',
    'laboratorio': 'beaker', 'tubo': 'beaker', 'frasco': 'beaker',
    'quimica': 'atom', 'fisica': 'atom', 'biologia': 'dna',
    'energia': 'lightning', 'electricidad': 'lightning', 'magnetismo': 'magnet',
    'iman': 'magnet', 'fuerza': 'lightning', 'gravedad': 'earth',
    'luz': 'sun', 'temperatura': 'solar', 'calor': 'fire', 'frio': 'snow',
    'oxigeno': 'atom', 'hidrogeno': 'atom', 'carbono': 'atom',
    'evolucion': 'dna', 'fotosintesis': 'leaf', 'respiracion': 'lungs',
    'ecosistema': 'tree', 'cadena alimenticia': 'fish',
    'termometro': 'thermometer', 'barometro': 'thermometer',
    'lupa': 'microscope', 'prisma': 'triangle',
    'imán': 'magnet', 'experimento': 'beaker',
    'teoria': 'brain', 'hipotesis': 'brain', 'formula': 'calculator',

    // ── Matemáticas ────────────────────────────────────────────────────────
    'numero': 'calculator', 'numeros': 'calculator', 'suma': 'plus',
    'sumar': 'plus', 'resta': 'minus', 'restar': 'minus',
    'multiplicar': 'x', 'multiplicacion': 'x', 'division': 'divide',
    'dividir': 'divide', 'igual': 'equal', 'porcentaje': 'percent',
    'fraccion': 'divide', 'decimal': 'calculator', 'algebra': 'calculator',
    'geometria': 'triangle', 'triangulo': 'triangle', 'rectangulo': 'square',
    'cuadrado': 'square', 'circulo': 'circle', 'esfera': 'circle',
    'cubo': 'box', 'cilindro': 'circle', 'cono': 'triangle',
    'angulo': 'triangle', 'grado': 'triangle', 'radio': 'circle',
    'diametro': 'circle', 'perimetro': 'ruler', 'area': 'ruler',
    'volumen': 'box', 'probablidad': 'calculator', 'estadistica': 'chart',
    'grafica': 'chart', 'grafico': 'chart',
    'regla': 'ruler', 'calculadora': 'calculator', 'compas': 'compass',
    'transportador': 'compass', 'coordenada': 'map',
    'eje': 'chart', 'funcion': 'calculator', 'ecuacion': 'calculator',

    // ── Historia / Social ──────────────────────────────────────────────────
    'rey': 'crown', 'reina': 'crown', 'corona': 'crown', 'principe': 'crown',
    'castillo': 'castle', 'fortaleza': 'castle', 'torre': 'castle',
    'espada': 'sword', 'escudo': 'shield', 'lanza': 'sword', 'arco': 'bow-arrow',
    'piramide': 'triangle', 'templo': 'landmark', 'monumento': 'landmark',
    'columna': 'landmark', 'ruina': 'landmark',
    'barco': 'ship', 'bote': 'ship', 'canoa': 'ship',
    'pergamino': 'scroll', 'libro antiguo': 'scroll', 'mapa antiguo': 'scroll',
    'soldado': 'shield', 'guerrero': 'sword', 'caballero': 'sword',
    'pirata': 'ship', 'capitan': 'ship', 'ancla': 'anchor',
    'revolucion': 'flag', 'guerra': 'sword', 'paz': 'heart',
    'democracia': 'flag', 'constitucion': 'scroll', 'ley': 'scroll',
    'gobierno': 'landmark', 'pais': 'flag', 'nacion': 'flag',
    'civilizacion': 'landmark', 'cultura': 'landmark', 'arte': 'pencil',
    'museo': 'landmark', 'iglesia': 'landmark', 'catedral': 'landmark',
    'comercio': 'money', 'economia': 'money', 'mercado': 'money',
    'agricultura': 'leaf', 'ganaderia': 'cow', 'pesca': 'fish',

    // ── Vida Cotidiana ─────────────────────────────────────────────────────
    'casa': 'house', 'hogar': 'house', 'edificio': 'house', 'apartamento': 'house',
    'puerta': 'door', 'ventana': 'window', 'escalera': 'stairs',
    'cama': 'bed', 'silla': 'chair', 'mesa': 'table', 'sofa': 'sofa',
    'cocina': 'cooking', 'bano': 'bath',
    'coche': 'car', 'carro': 'car', 'auto': 'car', 'camion': 'truck',
    'autobus': 'bus', 'tren': 'train', 'metro': 'train',
    'avion': 'plane', 'helicoptero': 'helicopter',
    'bicicleta': 'bicycle', 'moto': 'bicycle', 'barco': 'ship',
    'semaforo': 'traffic', 'carretera': 'car', 'puente': 'map',
    'hospital': 'hospital', 'escuela': 'school', 'universidad': 'school',
    'banco': 'money', 'supermercado': 'shopping', 'tienda': 'shopping',
    'restaurante': 'restaurant', 'hotel': 'hotel',
    'telefono': 'phone', 'celular': 'phone', 'computadora': 'computer',
    'computador': 'computer', 'laptop': 'laptop', 'tablet': 'tablet',
    'television': 'tv', 'radio': 'radio', 'camara': 'camera',
    'reloj': 'clock', 'calendario': 'calendar', 'dinero': 'money',
    'moneda': 'money', 'billete': 'money', 'tarjeta': 'credit-card',
    'llave': 'key', 'candado': 'lock', 'mochila': 'backpack',
    'maleta': 'luggage', 'paraguas': 'umbrella',
    'ropa': 'shirt', 'camisa': 'shirt', 'pantalon': 'pants',
    'zapato': 'footprints', 'sombrero': 'hat',

    // ── Alimentos ──────────────────────────────────────────────────────────
    'manzana': 'apple', 'pera': 'apple', 'naranja': 'orange', 'limon': 'lemon',
    'platano': 'banana', 'banana': 'banana', 'uva': 'grape', 'fresa': 'strawberry',
    'sandia': 'watermelon', 'melon': 'watermelon', 'mango': 'mango',
    'piña': 'pineapple', 'pina': 'pineapple', 'coco': 'coconut',
    'cereza': 'cherry', 'durazno': 'peach', 'kiwi': 'kiwi',
    'zanahoria': 'carrot', 'tomate': 'tomato', 'papa': 'potato',
    'maiz': 'corn', 'broccoli': 'broccoli', 'lechuga': 'salad',
    'ajo': 'garlic', 'cebolla': 'onion',
    'pan': 'bread', 'arroz': 'rice', 'pasta': 'noodles',
    'pizza': 'pizza', 'hamburguesa': 'hamburger', 'taco': 'taco',
    'sopa': 'soup', 'ensalada': 'salad',
    'carne': 'meat', 'pollo cocido': 'chicken', 'pescado': 'fish',
    'huevo': 'egg', 'leche': 'milk', 'queso': 'cheese',
    'mantequilla': 'butter', 'helado': 'icecream', 'pastel': 'cake',
    'chocolate': 'chocolate', 'dulce': 'candy', 'galleta': 'cookie',
    'cafe': 'coffee', 'te': 'tea', 'agua potable': 'water',
    'jugo': 'juice', 'refresco': 'soda',

    // ── Partes del Cuerpo Humano ───────────────────────────────────────────
    'ojo': 'eye', 'ojos': 'eye', 'oido': 'ear', 'nariz': 'nose',
    'boca': 'mouth', 'diente': 'tooth', 'dientes': 'tooth', 'lengua': 'tongue',
    'mano': 'hand', 'pie': 'footprint', 'pierna': 'footprint',
    'cabeza': 'brain', 'cara': 'user', 'piel': 'user',
    'pestaña': 'eye', 'ceja': 'eye',

    // ── Escuela y Educación ────────────────────────────────────────────────
    'libro': 'book', 'libros': 'book', 'cuaderno': 'notebook',
    'lapiz': 'pencil', 'lapicero': 'pencil', 'pluma': 'pencil', 'boligrafo': 'pencil',
    'borrador': 'eraser', 'tijeras': 'scissors', 'pizarron': 'presentation',
    'mochila': 'backpack', 'lonchera': 'backpack',
    'maestro': 'user', 'profesor': 'user', 'alumno': 'user', 'estudiante': 'user',
    'aula': 'school', 'clase': 'school', 'examen': 'check-square',
    'tarea': 'check-square', 'calificacion': 'star', 'diploma': 'scroll',
    'pintura': 'pencil', 'colores': 'pencil', 'acuarela': 'pencil',

    // ── Deportes ───────────────────────────────────────────────────────────
    'futbol': 'soccer', 'balon': 'soccer', 'arquero': 'soccer',
    'basquetbol': 'basketball', 'voleibol': 'volleyball',
    'beisbol': 'baseball', 'tenis': 'tennis',
    'natacion': 'swim', 'nadar': 'swim',
    'atletismo': 'run', 'correr': 'run', 'saltar': 'jump',
    'ciclismo': 'bicycle', 'gimnasia': 'dumbbell',
    'trofeo': 'trophy', 'medalla': 'medal', 'campeon': 'trophy',

    // ── Música y Arte ──────────────────────────────────────────────────────
    'musica': 'music', 'nota': 'music', 'cancion': 'music',
    'guitarra': 'guitar', 'piano': 'piano', 'violin': 'violin',
    'flauta': 'instrument', 'bateria': 'drum', 'tambor': 'drum',
    'microfono': 'microphone', 'parlante': 'speaker', 'auricular': 'headphones',
    'pintura cuadro': 'image', 'escultura': 'landmark',
    'teatro': 'theater', 'cine': 'movie', 'pelicula': 'movie',
    'baile': 'music', 'danza': 'music',

    // ── Tecnología ─────────────────────────────────────────────────────────
    'internet': 'wifi', 'wifi': 'wifi', 'red': 'network',
    'robot': 'robot', 'inteligencia artificial': 'brain',
    'programacion': 'code', 'codigo': 'code', 'algoritmo': 'code',
    'impresora': 'printer', 'teclado': 'keyboard', 'mouse': 'mouse',
    'disco duro': 'hard-drive', 'usb': 'usb', 'nube digital': 'cloud',
    'correo': 'mail', 'mensaje': 'message', 'video': 'video',
    'aplicacion': 'phone', 'juego video': 'gamepad',
    'pantalla': 'monitor', 'proyector': 'projector',
    'servidor': 'server', 'base datos': 'database',
    'cohete espacial': 'rocket',

    // ── Religión / Mitología ───────────────────────────────────────────────
    'angel': 'star', 'dios': 'star', 'iglesia': 'landmark',
    'biblia': 'book', 'cruz': 'cross', 'estrella david': 'star',
    'zeus': 'lightning', 'poseidon': 'ocean', 'ares': 'sword',
    'osiris': 'pyramid', 'ra': 'sun',

    // ── Clima / Atmósfera ──────────────────────────────────────────────────
    'clima': 'cloud', 'temperatura': 'thermometer',
    'presion': 'thermometer', 'humedad': 'droplets',
    'evaporacion': 'cloud', 'condensacion': 'cloud',
    'precipitacion': 'rain', 'ciclo agua': 'droplets',

    // ── Profesiones ────────────────────────────────────────────────────────
    'doctor': 'stethoscope', 'medico': 'stethoscope', 'enfermero': 'stethoscope',
    'bombero': 'fire', 'policia': 'shield', 'ingeniero': 'settings',
    'arquitecto': 'house', 'cocinero': 'cooking', 'piloto': 'plane',
    'astronauta': 'rocket', 'cientifico': 'microscope',
    'musico': 'music', 'artista': 'pencil', 'escritor': 'pencil',
    'abogado': 'scroll', 'juez': 'scroll',

    // ── Sentimientos / Emociones (Prioridad Icon Font para caras huecas) ──
    'feliz': 'mood-smile', 'felicidad': 'mood-smile', 'alegre': 'mood-smile',
    'triste': 'mood-frown', 'tristeza': 'mood-frown', 'llorar': 'mood-frown',
    'enojado': 'mood-angry', 'enojo': 'mood-angry', 'ira': 'mood-angry',
    'nervioso': 'mood-nervous', 'asustado': 'mood-scared',
    'amor': 'heart', 'amar': 'heart', 'beso': 'heart',
    'miedo': 'alert-circle', 'susto': 'alert-circle', 'sorpresa': 'alert-circle',
    'confusion': 'help-circle', 'duda': 'help-circle', 'pregunta': 'help-circle',

    // ── Símbolos / Abstractos ─────────────────────────────────────────────
    'correcto': 'check', 'incorrecto': 'x', 'peligro': 'alert',
    'advertencia': 'alert', 'prohibido': 'ban', 'permitido': 'check',
    'flecha': 'arrow-right', 'mas': 'plus', 'menos': 'minus',
    'arriba': 'arrow-up', 'abajo': 'arrow-down',
    'inicio': 'home', 'fin': 'flag', 'pausa': 'pause',
    'tiempo': 'clock', 'velocidad': 'gauge', 'fuerza': 'dumbbell',
    'peso': 'scale', 'medida': 'ruler',
};

// ══════════════════════════════════════════════════════════════════════════════
// EMOJI CHALK FALLBACK (~300 conceptos → Unicode emoji)
// Se renderiza en canvas con filtro grayscale(100%) brightness(300%)
// para lograr el aspecto "tiza blanca" sobre pizarra verde.
// Funciona OFFLINE en todos los dispositivos modernos (iOS, Android, Windows, Mac).
// ══════════════════════════════════════════════════════════════════════════════
window.CONCEPT_TO_EMOJI = {
    // ── Animales ──────────────────────────────────────────────────────────────
    'horse': '🐴', 'dog': '🐕', 'cat': '🐈', 'cow': '🐄', 'pig': '🐖',
    'sheep': '🐑', 'chicken': '🐔', 'rooster': '🐓', 'bird': '🐦',
    'eagle': '🦅', 'owl': '🦉', 'penguin': '🐧', 'duck': '🦆',
    'flamingo': '🦩', 'parrot': '🦜', 'peacock': '🦚',
    'fish': '🐟', 'shark': '🦈', 'dolphin': '🐬', 'whale': '🐳',
    'octopus': '🐙', 'crab': '🦀', 'lobster': '🦞',
    'lion': '🦁', 'tiger': '🐯', 'bear': '🐻', 'panda': '🐼',
    'monkey': '🐒', 'gorilla': '🦍', 'rabbit': '🐰', 'wolf': '🐺',
    'fox': '🦊', 'deer': '🦌', 'giraffe': '🦒', 'zebra': '🦓',
    'elephant': '🐘', 'rhino': '🦏', 'hippo': '🦛',
    'crocodile': '🐊', 'snake': '🐍', 'turtle': '🐢', 'frog': '🐸',
    'butterfly': '🦋', 'bee': '🐝', 'ant': '🐜', 'spider': '🕷️',
    'snail': '🐌', 'dragon': '🐉', 'unicorn': '🦄', 'kangaroo': '🦘',
    'koala': '🐨', 'dinosaur': '🦕', 'beaver': '🦫', 'otter': '🦦',
    'bat': '🦇', 'hedgehog': '🦔', 'ferret': '🦨', 'skunk': '🦨',
    'mouse': '🐭', 'hamster': '🐹', 'goat': '🐐', 'camel': '🐪',
    'llama': '🦙', 'bison': '🦬', 'mammoth': '🦣',

    // ── Naturaleza ─────────────────────────────────────────────────────────
    'sun': '☀️', 'moon': '🌙', 'star': '⭐', 'cloud': '☁️',
    'rain': '🌧️', 'snow': '❄️', 'lightning': '⚡', 'tornado': '🌪️',
    'rainbow': '🌈', 'fire': '🔥', 'water': '💧', 'ocean': '🌊',
    'mountain': '⛰️', 'volcano': '🌋', 'desert': '🏜️', 'island': '🏝️',
    'tree': '🌳', 'palm-tree': '🌴', 'cactus': '🌵', 'flower': '🌸',
    'rose': '🌹', 'sunflower': '🌻', 'leaf': '🍃', 'grass': '🌿',
    'mushroom': '🍄', 'seed': '🌱', 'earth': '🌍', 'planet': '🪐',
    'comet': '☄️', 'rocket': '🚀', 'satellite': '🛰️',
    'wind': '💨', 'droplets': '💦',

    // ── Ciencia ────────────────────────────────────────────────────────────
    'atom': '⚛️', 'dna': '🧬', 'microscope': '🔬', 'telescope': '🔭',
    'brain': '🧠', 'heart': '❤️', 'bone': '🦴', 'eye': '👁️',
    'lungs': '🫁', 'ear': '👂', 'tooth': '🦷',
    'beaker': '⚗️', 'magnet': '🧲', 'thermometer': '🌡️',
    'diamond': '💎',

    // ── Objetos cotidianos ─────────────────────────────────────────────────
    'house': '🏠', 'school': '🏫', 'hospital': '🏥', 'castle': '🏰',
    'church': '⛪', 'bank': '🏦', 'museum': '🏛️',
    'car': '🚗', 'bus': '🚌', 'train': '🚂', 'plane': '✈️',
    'ship': '🚢', 'bicycle': '🚴', 'helicopter': '🚁',
    'truck': '🚚', 'tractor': '🚜', 'police-car': '🚓',
    'book': '📚', 'pencil': '✏️', 'ruler': '📏',
    'calculator': '🧮', 'backpack': '🎒', 'scissors': '✂️',
    'clock': '⏰', 'calendar': '📅', 'phone': '📱',
    'computer': '💻', 'laptop': '💻', 'tv': '📺', 'camera': '📷',
    'money': '💰', 'key': '🔑', 'lock': '🔒', 'umbrella': '☂️',
    'crown': '👑', 'sword': '⚔️', 'shield': '🛡️', 'scroll': '📜',
    'map': '🗺️', 'compass': '🧭', 'flag': '🚩', 'anchor': '⚓',
    'trophy': '🏆', 'medal': '🏅', 'gift': '🎁',

    // ── Alimentos ──────────────────────────────────────────────────────────
    'apple': '🍎', 'orange': '🍊', 'banana': '🍌', 'grape': '🍇',
    'strawberry': '🍓', 'watermelon': '🍉', 'pineapple': '🍍',
    'cherry': '🍒', 'peach': '🍑', 'mango': '🥭', 'coconut': '🥥',
    'lemon': '🍋', 'carrot': '🥕', 'corn': '🌽', 'tomato': '🍅',
    'potato': '🥔', 'broccoli': '🥦', 'salad': '🥗',
    'bread': '🍞', 'pizza': '🍕', 'hamburger': '🍔', 'taco': '🌮',
    'rice': '🍚', 'noodles': '🍜', 'soup': '🍲',
    'meat': '🥩', 'egg': '🥚', 'milk': '🥛', 'cheese': '🧀',
    'icecream': '🍦', 'cake': '🎂', 'chocolate': '🍫', 'candy': '🍬',
    'cookie': '🍪', 'coffee': '☕', 'tea': '🍵', 'juice': '🍹',

    // ── Deportes ───────────────────────────────────────────────────────────
    'soccer': '⚽', 'basketball': '🏀', 'baseball': '⚾',
    'football': '🏈', 'tennis': '🎾', 'volleyball': '🏐',
    'swim': '🏊', 'run': '🏃', 'bicycle': '🚴',
    'dumbbell': '🏋️', 'medal': '🏅', 'trophy': '🏆',

    // ── Música / Arte ──────────────────────────────────────────────────────
    'music': '🎵', 'guitar': '🎸', 'piano': '🎹',
    'drum': '🥁', 'violin': '🎻', 'microphone': '🎤',
    'headphones': '🎧', 'speaker': '🔊',
    'movie': '🎬', 'theater': '🎭', 'art': '🎨',

    // ── Tecnología ─────────────────────────────────────────────────────────
    'robot': '🤖', 'wifi': '📶', 'code': '💻',
    'printer': '🖨️', 'keyboard': '⌨️', 'monitor': '🖥️',
    'server': '🖥️', 'database': '🗄️', 'gamepad': '🎮',

    // ── Sentimientos ───────────────────────────────────────────────────────
    'smile': '😊', 'frown': '😢', 'angry': '😠', 'love': '❤️',
    'scared': '😨', 'surprised': '😮', 'confused': '😕',

    // ── Símbolos ───────────────────────────────────────────────────────────
    'check': '✅', 'warning': '⚠️', 'danger': '🚨', 'ban': '🚫',
    'arrow-right': '➡️', 'arrow-left': '⬅️', 'arrow-up': '⬆️', 'arrow-down': '⬇️',
    'plus': '➕', 'minus': '➖', 'question': '❓', 'exclamation': '❗',
    'scale': '⚖️', 'thermometer': '🌡️',
    'triangle': '🔺', 'circle': '🔵', 'square': '🟥',
};
// ══════════════════════════════════════════════════════════════════════════════
// MAPA INVERSO: EMOJI → CONCEPT  (para el interceptor de emojis crudos del LLM)
// Se genera automáticamente invirtiendo CONCEPT_TO_EMOJI.
// El interceptor en speakLLM usa este mapa para convertir 🐴→[ICON:horse] en tiempo real.
// ══════════════════════════════════════════════════════════════════════════════
window.EMOJI_TO_CONCEPT = {};
(function buildReverseMap() {
    const map = window.CONCEPT_TO_EMOJI;
    for (const concept in map) {
        const emoji = map[concept];
        // Un emoji puede tener variantes de skin tone o ZWJ sequences; mapeamos la base
        if (!window.EMOJI_TO_CONCEPT[emoji]) {
            window.EMOJI_TO_CONCEPT[emoji] = concept;
        }
    }
    // Emojis extra frecuentes que el LLM suele insertar directamente
    const extras = {
        '🎉': 'star', '🎊': 'trophy', '✨': 'star', '💫': 'star',
        '🔥': 'fire', '💡': 'sun', '🌟': 'star', '⚡': 'lightning',
        '🧑': 'user', '👦': 'user', '👧': 'user', '👨': 'user', '👩': 'user',
        '👏': 'heart', '🙌': 'heart', '🤝': 'heart', '💪': 'dumbbell',
        '🌍': 'earth', '🌎': 'earth', '🌏': 'earth',
        '📌': 'map', '📍': 'map', '🗺': 'map',
        '⭐': 'star', '🌠': 'star', '🌌': 'planet',
        '🏁': 'flag', '🚩': 'flag', '🏳': 'flag',
        '💥': 'fire', '🌊': 'ocean', '❄': 'snow', '🌬': 'wind',
        '🎵': 'music', '🎶': 'music', '🎤': 'microphone',
        '🧬': 'dna', '🔬': 'microscope', '🔭': 'telescope', '⚗': 'beaker',
        '🤖': 'robot', '💻': 'computer', '📱': 'phone',
        '🏃': 'run', '🚶': 'user', '🧠': 'brain',
    };
    for (const emoji in extras) {
        if (!window.EMOJI_TO_CONCEPT[emoji]) {
            window.EMOJI_TO_CONCEPT[emoji] = extras[emoji];
        }
    }
})();

console.log(`[MAUNET V28.1] 🌐 Bridge bilingüe cargado — ES_TO_EN: ${Object.keys(window.ES_TO_EN).length} palabras | EMOJI→CONCEPT: ${Object.keys(window.EMOJI_TO_CONCEPT).length} | CONCEPT→EMOJI: ${Object.keys(window.CONCEPT_TO_EMOJI).length}`);
