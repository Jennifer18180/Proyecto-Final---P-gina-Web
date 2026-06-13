from flask import Flask, redirect, url_for, session, request, render_template
from database import get_next_question, get_quises
import random
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NoTieneClave'

# Mensajes didácticos para la pantalla de juego
MENSAJES_MOTIVADORES = [
    "¡Excelente progreso! Continúa con ese gran entusiasmo.",
    "Cada pregunta es una nueva oportunidad para aprender algo grandioso.",
    "¡Vas por muy buen camino! El conocimiento se construye paso a paso.",
    "No te detengas, estás haciendo un esfuerzo magnífico.",
    "El aprendizaje requiere práctica, ¡y lo estás haciendo genial!",
    "¡Mantén el foco! Estás descubriendo nuevas habilidades hoy.",
    "¡Qué buena concentración! Sigue respondiendo con confianza.",
    "Tu mente se expande con cada desafío. ¡Sigue adelante!"
]

# Diccionario para inyectar descripciones didácticas automáticas a los quizes de la DB
DESCRIPCIONES_QUIZ = {
    1: "Explora conceptos esenciales sobre nutrición, procedencia celular y los misterios cotidianos de lo que consumimos.",
    2: "Desafía tu mente con fundamentos lógicos y preguntas curiosas sobre fenómenos que nos rodean a diario.",
    3: "Un viaje analítico sobre las bases fundamentales de la naturaleza y eventos simples que solemos pasar por alto."
}

def start_quiz(quiz_id):
    session['quiz'] = int(quiz_id)
    session['prev_question'] = 0
    session['correctas'] = 0
    session['totales'] = 0
    
    try:
        conn = sqlite3.connect("quises.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM quiz_content WHERE quiz_id = ?", [quiz_id])
        session['max_preguntas'] = cursor.fetchone()[0] or 5
        cursor.close()
        conn.close()
    except:
        session['max_preguntas'] = 5

def end_quiz():
    session.clear()

def check_answer():
    resp_usuario = request.form.get('ans_text')
    resp_correcta = session.get('last_correct')

    if resp_usuario:
        session['totales'] += 1
        if resp_usuario == str(resp_correcta):
            session['correctas'] += 1

def calc_stats(total, correct):
    if total:
        return round((correct / total) * 100, 2)
    return 0

# 1. NUEVA PÁGINA PRINCIPAL: BIENVENIDA / PRESENTACIÓN
def index():
    end_quiz()
    # Frase filosófica sobre el aprendizaje como motor humano
    frase_filosofo = {
        "texto": "«El conocimiento es el único bien que crece cuando se comparte y el motor que despierta la verdadera esencia del ser humano.»",
        "autor": "Inspiración Filosófica del Desarrollo"
    }
    return render_template('index.html', frase=frase_filosofo)

# 2. NUEVA PÁGINA DE SELECCIÓN: TARJETAS EN CUADRÍCULA (GRID)
def quises_selection():
    if request.method == 'GET':
        end_quiz()
        raw_quises = get_quises() # Trae [(id, name), ...]
        
        # Enriquecemos los datos con descripciones para las tarjetas modernas
        lista_quises_premium = []
        for q_id, q_name in raw_quises:
            desc = DESCRIPCIONES_QUIZ.get(q_id, "Pon a prueba tus conocimientos interactivos con este cuestionario dinámico diseñado para mentes curiosas.")
            lista_quises_premium.append({'id': q_id, 'name': q_name, 'desc': desc})
            
        return render_template('quises.html', quises=lista_quises_premium)
    else:
        quiz_id = request.form.get('quiz_id')
        if quiz_id:
            start_quiz(quiz_id)
            return redirect(url_for('test'))
        return redirect(url_for('quises_selection'))

def test():
    if 'quiz' not in session or 'prev_question' not in session:
        return redirect(url_for('quises_selection'))

    if request.method == 'POST':
        check_answer()

    result = get_next_question(session['prev_question'], session['quiz'])

    if result is None or result == 0:
        return redirect(url_for('result'))
    
    session['prev_question'] = result[0]
    session['last_correct'] = result[2]

    respuestas = list(result[2:6]) 
    random.shuffle(respuestas) 

    preguntas_vistas = session.get('totales', 0) + 1
    max_preguntas = session.get('max_preguntas', 5)
    
    porcentaje_barra = round((preguntas_vistas / max_preguntas) * 100)
    if porcentaje_barra > 100:
        porcentaje_barra = 100

    mensaje_actual = random.choice(MENSAJES_MOTIVADORES)

    return render_template('test.html', 
                           pregunta=result[1], 
                           opciones=respuestas, 
                           progreso=porcentaje_barra,
                           numero_pregunta=preguntas_vistas,
                           total_preguntas=max_preguntas,
                           motivacion=mensaje_actual)

def result():
    if 'totales' not in session:
        return redirect(url_for('quises_selection'))
    
    total = session.get('totales', 0)
    correct = session.get('correctas', 0)
    incorrect = total - correct
    percent = calc_stats(total, correct)

    return render_template('result.html',
                            totales=total,
                            correctas=correct,
                            incorrectas=incorrect,
                            porcentaje=percent)

app.add_url_rule('/', 'index', index, methods=['GET'])
app.add_url_rule('/quizes', 'quises_selection', quises_selection, methods=['GET', 'POST'])
app.add_url_rule('/test', 'test', test, methods=['GET', 'POST'])
app.add_url_rule('/result', 'result', result, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)
