import sqlite3

DB = "quises.sqlite"
conn = None
cursor = None


def open():
    global conn, cursor
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    # parametros de config de la db
    cursor.execute('PRAGMA foreign_keys=on')


def close():
    cursor.close()
    conn.close()


def execute_query(query):
    cursor.execute(query)
    conn.commit()


def create_tables():
    tables = [
        '''CREATE TABLE IF NOT EXISTS quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL);''',

        '''CREATE TABLE IF NOT EXISTS question (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_name TEXT NOT NULL,
    correct VARCHAR(100) NOT NULL,
    wrong_1 VARCHAR(10) NOT NULL,
    wrong_2 VARCHAR(10) NOT NULL,
    wrong_3 VARCHAR(10) NOT NULL);''',

        '''CREATE TABLE IF NOT EXISTS quiz_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES quiz (id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES question (id) ON DELETE CASCADE);'''
    ]

    open()
    for sql in tables:
        execute_query(sql)
    close()
    print('Tablas creadas exitosamente')


def add_quises():
    quizes = [
        ('CUESTIONARIO 1: INVENTOS POR ACCIDENTE', ),
        ('CUESTIONARIO 2: EL PASADO DE LA TECNOLOGÍA DIARIA', ),
        ('CUESTIONARIO 3: EL ORIGEN DE LOS ALIMENTOS', )
        ('CUESTIONARIO 4: TRADICIONES Y FRASES HEREDADAS', )
        ('CUESTIONARIO 5: MITOLOGÍA Y MÚSICA EN LA VIDA REAL', )]

    open()
    cursor.executemany('INSERT INTO quiz (name) VALUES (?);', quizes)
    conn.commit()
    close()
    print('Se ingresaron los datos de la tabla quiz!')


def add_questions():
    questions = [
        # === CUESTIONARIO 1: INVENTOS POR ACCIDENTE === (1-7)
        ('¿Qué golosina se inventó por accidente cuando se dejaron granos de trigo hervidos secándose por días?', 'Las hojuelas de maíz (Corn Flakes)', 'Las gomitas', 'El chocolate con leche', 'El chicle'),
        ('¿Qué objeto de oficina se inventó intentando crear un pegamento ultra fuerte pero resultó ser lo contrario?', 'Las notas adhesivas (Post-it)', 'La cinta correctora', 'El clip', 'El marcador resaltador'),
        ('¿Cómo se descubrió que las microondas podían calentar comida rápidamente?', 'A un científico se le derritió una barra de chocolate en el bolsillo', 'Un cocinero dejó caer carne en una estación de radio', 'Se inventó buscando cascos climatizados para astronautas', 'Se notó que los pájaros cerca de antenas tenían más calor'),
        ('¿Cuál era la función original de la plastilina Play-Doh antes de ser un juguete?', 'Limpiar el hollín y manchas de carbón de las paredes', 'Aislar cables eléctricos', 'Masilla para fugas en barcos', 'Pegamento experimental para prótesis dentales'),
        ('¿Por qué se cocinaron las papas fritas de bolsa (Chips) de forma tan delgada por primera vez?', 'Para molestar a un cliente exigente que se quejaba de que eran gruesas', 'Porque se quedaron sin aceite y debían cocinarse rápido', 'Por un error de una máquina cortadora rota', 'Intentando crear platos comestibles'),
        ('¿Cómo se descubrió el vidrio templado de seguridad que no se astilla?', 'A un químico se le cayó un frasco con plástico líquido seco y no se rompió', 'Observando cómo las telas de araña resistían el granizo', 'Dejando enfriar vidrio derretido en agua congelada', 'Intentando fabricar un acuario para un tiburón'),
        ('¿Qué buscaba crear el científico que terminó descubriendo el teflón por accidente?', 'Un nuevo gas refrigerante para neveras que no fuera tóxico', 'Un escudo protector para las balas del ejército', 'Una pintura para que los barcos navegaran más rápido', 'Un lubricante de alta densidad para aviones'),

        # === CUESTIONARIO 2: EL PASADO DE LA TECNOLOGÍA DIARIA === (8-12)
        ('¿Cuál fue el motivo original por el cual se inventó el sistema de mensajería SMS?', 'Para que las compañías telefónicas enviaran avisos de red a los usuarios', 'Para que los adolescentes se comunicaran sin llamar', 'Para enviar coordenadas en misiones de rescate', 'Como un sistema secreto de espionaje militar'),
        ('¿Para qué servía originalmente la tecnología Bluetooth antes de convertirse en estándar de audio?', 'Para conectar computadoras portátiles con teléfonos celulares y transferir datos', 'Para rastrear equipaje en los aeropuertos', 'Para sincronizar relojes públicos digitales', 'Para mandar señales de radio a los submarinos'),
        ('Antes de las pantallas táctiles, ¿cómo funcionaba el mecanismo interno del primer mouse?', 'Usaba dos ruedas metálicas perpendiculares que registraban el movimiento', 'Tenía una esfera de goma gigante en la parte superior', 'Funcionaba con sensores de luz solar', 'Era un lápiz óptico amarrado a una cuerda'),
        ('¿Qué significaba originalmente la palabra "Pixel" en el mundo tecnológico?', 'Es una abreviatura de "Picture Element" (Elemento de imagen)', 'El apellido del ingeniero que lo patentó', 'El nombre de una pequeña pieza de las televisiones antiguas', 'Un término matemático para referirse al infinito'),
        ('¿Cuál fue la primera función que tuvo la popular plataforma YouTube cuando se lanzó en 2005?', 'Un sitio web de citas en línea mediante videos', 'Un repositorio de videos de música educativa', 'Una plataforma exclusiva para trailers de cine', 'Un servicio de almacenamiento de archivos pesados'),

        # === CUESTIONARIO 3: EL ORIGEN DE LOS ALIMENTOS === (13-17)
        ('¿Cómo nació la famosa galleta con chispas de chocolate (Chocolate Chip Cookie)?', 'Una repostera rompió chocolate pensando que se derretiría por completo, pero quedó entero', 'Fue diseñada por un médico para combatir la falta de azúcar', 'Nació por un concurso de cocina en Francia', 'Un panadero dejó caer cacao en polvo sobre pan dulce'),
        ('¿Por qué el sándwich se llama "Sándwich"?', 'Por un conde inglés que pidió la carne entre panes para comer mientras jugaba cartas', 'Por una ciudad alemana donde solo se comía pan con embutidos', 'Es una palabra derivada del latín que significa "comida rápida"', 'Por el nombre del barco donde se inventó'),
        ('¿Cuál fue la razón por la que se crearon los cereales de desayuno a finales del siglo XIX?', 'Como parte de una dieta vegetariana estricta para pacientes de un sanatorio', 'Para alimentar a los soldados en tiempos de escasez', 'Como un postre económico para las fiestas escolares', 'Una estrategia de marketing para vender más leche'),
        ('¿De dónde es originaria la planta del tomate, ingrediente estrella de la comida italiana?', 'De América del Sur (llevado a Europa después)', 'De Italia', 'De Grecia', 'De la región mediterránea de África'),
        ('¿Qué alimento se usó originalmente en México y Centroamérica como moneda de cambio?', 'Los granos de cacao', 'Los granos de maíz de color dorado', 'Las semillas de calabaza', 'Las vainas de vainilla'),

        # === CUESTIONARIO 4: TRADICIONES Y FRASES HEREDADAS === (18-22)
        ('¿Por qué la gente dice "Cruzar los dedos" para atraer la buena suerte?', 'Era una antigua costumbre cristiana para hacer una cruz secreta de protección', 'Venía de los arqueros medievales que estiraban los dedos', 'Un ejercicio de relajación romano', 'Un método de los comerciantes para ocultar mentiras'),
        ('¿De dónde viene la costumbre de que los novios no vean a la novia vestida de blanco antes de la boda?', 'De la época de matrimonios arreglados, para evitar que el novio se arrepintiera', 'Una antigua ley de la iglesia para mantener la sorpresa', 'Una superstición de los costureros reales de Francia', 'Una tradición vikinga para evitar raptos'),
        ('¿Por qué tiramos monedas a las fuentes de agua o deseos?', 'Por la antigua creencia de que las fuentes eran hogares de dioses y se les pagaba tributo', 'Comenzó como un impuesto municipal en la antigua Roma', 'Para ayudar a las personas sin hogar que recogían el dinero', 'Un truco de los constructores para probar la profundidad'),
        ('¿Por qué se usa un anillo de compromiso específicamente en el dedo anular?', 'Los romanos creían que de ese dedo salía una vena que iba directo al corazón', 'Porque es el dedo que menos se usa y el anillo no se daña', 'Por una norma de etiqueta de la realeza británica', 'Porque era el único dedo donde el metal no estorbaba al trabajar'),
        ('¿Cuál es el origen de la piñata tradicional en las festividades?', 'Se originó en China como tradición agrícola, pasó a Italia/España y luego a América', 'Nació puramente en la cultura azteca para celebrar el año nuevo', 'Fue inventada por un panadero para vender dulces', 'Comenzó como un juego de feria infantil en Inglaterra'),

        # === CUESTIONARIO 5: MITOLOGÍA Y MÚSICA EN LA VIDA REAL === (23-33) 28
        ('¿Cuál es el origen de la palabra "Cereal" que desayunamos casi todos los días?', 'Viene de Ceres, la diosa romana de la agricultura y las cosechas', 'Del latín "Cerebrum" porque alimenta el cerebro', 'Del nombre del primer científico que analizó el trigo', 'De una palabra indígena que significa "semilla molida"'),
        ('¿Por qué el logotipo de los centros médicos incluye una serpiente enroscada en una vara?', 'Es la Vara de Esculapio, el dios griego de la medicina y la curación', 'Representa el veneno que se transforma en antídoto', 'Un símbolo medieval de los alquimistas que cambiaban de piel', 'Un homenaje a los primeros cirujanos del antiguo Egipto'),
        ('¿De dónde proviene la expresión tener un "Talón de Aquiles" para referirse a una debilidad?', 'La madre de Aquiles lo sumergió en un río mágico sosteniéndolo por el talón, quedando desprotegido', 'De un famoso atleta olímpico romano que se lesionó', 'De un calzado militar antiguo que causaba heridas', 'De un error de traducción de un texto de medicina antiguo'),
        ('¿Qué significa realmente la palabra "Clásico" en la música o literatura?', 'Originalmente se refería a los ciudadanos de la clase más alta y ejemplar en Roma', 'Que es algo muy viejo o antiguo', 'Que aburre a la mayoría de las personas', 'Que utiliza instrumentos de cuerda de madera'),
        ('¿Cuál es el origen de la palabra "Pánico" (miedo intenso)?', 'Viene de Pan, el dios griego que asustaba a los viajeros con ruidos en los bosques', 'Del latín "Panis" (pan), por el miedo al hambre', 'Del nombre de una fortaleza inexpugnable en Grecia', 'De un antiguo dialecto que significaba "perder la razón"')
        ('¿Cuántos meses en un año tienen 28 días?',
         'Todos', 'Uno', 'Ninguno', 'Dos'),
        ('¿Qué aspecto tendrá el acantilado verde si se cae en el Mar Rojo?',
         'Mojado', 'Rojo', 'No cambiará', 'Púrpura'),
        ('¿Con qué mano es mejor mezclar el té?',
         'Con una cuchara', 'Derecha', 'Izquierda', 'Cualquiera'),
        ('¿Qué no tiene longitud, profundidad, ancho, o altura pero puede medirse?',
         'Tiempo', 'Estupidez', 'El mar', 'Aire'),
        ('¿Cuándo es posible sacar agua con una red?', 'Cuando el agua está congelada',
         'Cuando no hay peces', 'Cuando los peces de colores nadan lejos', 'Cuando la red se rompe'),
        ('¿Qué es más grande que un elefante y no pesa nada?',
         'La sombra de un elefante', 'Un globo', 'Un paracaídas', 'Una nube')
    ]
    open()
    cursor.executemany('''INSERT INTO question
    (question_name, correct, wrong_1, wrong_2, wrong_3)
    VALUES (?,?, ?, ?, ?);''', questions)
    conn.commit()
    close()
    print('Se ingresaron los datos de la tabla!')


def add_links():  # ESTRUCTURAR CUESTIONARIOS
    links = []

    link = input('Desea ingresar un enlace? (y/n): ')
    while link.lower() == 'y':
        quiz_id = int(input('ID del quiz: '))
        question_id = int(input('ID de la pregunta: '))

        links.append((quiz_id, question_id))
        link = input('Desea ingresar otro? (y/n): ')

    if links:
        open()
        cursor.executemany(
            'INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?);', links)
        conn.commit()
        close()


def destroy_db():
    tables = ['quiz_content', 'quiz', 'question']
    open()
    for table in tables:
        execute_query(f'DROP TABLE IF EXISTS {table};')
    close()
    print('😂')


def show_tables():
    tables = ['quiz', 'question', 'quiz_content']
    open()

    for table in tables:
        print(f'=== TABLA: {table} ===')
        try:
            cursor.execute(f'SELECT * FROM {table};')
            data = cursor.fetchall()

            if not data:
                print('La tabla esta vacia.')
            else:
                for reg in data:
                    print(reg)

        except sqlite3.DatabaseError as error:
            print('Error:', error)
    close()


def get_next_question(question_id=0, quiz_id=1):
    open()

    query = '''
        SELECT
            quiz_content.id,
            question.question_name,
            question.correct,
            question.wrong_1,
            question.wrong_2,
            question.wrong_3
        FROM quiz_content
        JOIN question ON quiz_content.question_id = question.id
        WHERE quiz_content.id > ?
        AND quiz_content.quiz_id = ?
        ORDER BY quiz_content.id
        LIMIT 1'''

    cursor.execute(query, [question_id, quiz_id])
    result = cursor.fetchone()
    close()
    return result


# def show(table):
#     query = 'SELECT * FROM ' + table
#     open()
#     cursor.execute(query)
#     print(cursor.fetchall())
#     close()


# def show_tables():
#     show('question')
#     show('quiz')
#     show('quiz_content')


def get_quises():
    open()
    cursor.execute('SELECT id, name FROM quiz ORDER BY id;')
    result = cursor.fetchall()
    close()
    return result

def run():
    destroy_db()
    create_tables()
    add_questions()
    add_quises()
    show_tables()

def set_quiz():
    show_tables()
    add_links()

if __name__ == "__main__":
    #run()
    create_tables()
    set_quiz()
    #destroy_db()