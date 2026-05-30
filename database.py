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
        ('Propio juego', ),
        ('¿Quién quiere ser millonario?', ),
        ('El más inteligente', )]

    open()
    cursor.executemany('INSERT INTO quiz (name) VALUES (?);', quizes)
    conn.commit()
    close()
    print('Se ingresaron los datos de la tabla quiz!')

def add_questions():
    questions = [
        ('¿Cuántos meses en un año tienen 28 días?', 'Todos', 'Uno', 'Ninguno','Dos'),
        ('¿Qué aspecto tendrá el acantilado verde si se cae en el Mar Rojo?', 'Mojado', 'Rojo', 'No cambiará', 'Púrpura'),
        ('¿Con qué mano es mejor mezclar el té?', 'Con una cuchara', 'Derecha', 'Izquierda', 'Cualquiera'),
        ('¿Qué no tiene longitud, profundidad, ancho, o altura pero puede medirse?', 'Tiempo', 'Estupidez', 'El mar','Aire'),
        ('¿Cuándo es posible sacar agua con una red?', 'Cuando el agua está congelada', 'Cuando no hay peces', 'Cuando los peces de colores nadan lejos', 'Cuando la red se rompe'),
        ('¿Qué es más grande que un elefante y no pesa nada?', 'La sombra de un elefante','Un globo','Un paracaídas', 'Una nube')
    ]
    open()
    cursor.executemany('''INSERT INTO question
    (question_name, correct, wrong_1, wrong_2, wrong_3)
    VALUES (?,?, ?, ?, ?);''', questions)
    conn.commit()
    close()
    print('Se ingresaron los datos de la tabla!')


def add_links(): # ESTRUCTURAR CUESTIONARIOS
    links = []

    link = input('Desea ingresar un enlace? (y/n): ')
    while link.lower() == 'y':
        quiz_id = int(input('ID del quiz: ')) 
        question_id = int(input('ID de la pregunta: ')) 

        links.append((quiz_id, question_id))
        link = input('Desea ingresar otro? (y/n): ')

    if links:
        open()
        cursor.executemany('INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?);', links)
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


def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def get_quises():
    open()
    cursor.execute('SELECT id, name FROM quiz;')
    result = cursor.fetchall()
    close()
    return result


def main(): 
    show_tables()
    add_links()

    print(get_next_question(2, 1))
    

if __name__ == "__main__":
    main()
