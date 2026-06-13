from flask import Flask, redirect, url_for, session, request, render_template
from database import get_next_question, get_quises
import random
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NoTieneClave'

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
    session['historial'] = [] # 👈 Almacenará pares de [pregunta, respuesta_elegida]
    
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

def check_answer(pregunta_texto):
    resp_usuario = request.form.get('ans_text')
    resp_correcta = session.get('last_correct')

    if resp_usuario:
        session['totales'] += 1
        # Guardamos en el historial lo que el usuario respondió para mostrarlo al final
        historial_actual = session.get('historial', [])
        historial_actual.append({
            'pregunta': pregunta_texto,
            'elegida': resp_usuario
        })
        session['historial'] = historial_actual

        if resp_usuario == str(resp_correcta):
            session['correctas'] += 1

def calc_stats(total, correct):
    if total:
        return round((correct / total) * 100, 2)
    return 0

def index():
    end_quiz()
    frase_filosofo = {
        "texto": "«El conocimiento es el único bien que crece cuando se comparte y el motor que despierta la verdadera esencia del ser humano.»",
        "autor": "Inspiración Filosófica del Desarrollo"
    }
    return render_template('index.html', frase=frase_filosofo)

def quises_selection():
    if request.method == 'GET':
        end_quiz()
        raw_quises = get_quises()
        
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

    # Para capturar correctamente la pregunta anterior en el historial antes de traer la nueva de la DB
    pregunta_actual_texto = request.form.get('current_question_text', '')

    if request.method == 'POST':
        check_answer(pregunta_actual_texto)

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
    
    # Calculamos porcentajes proporcionales para renderizar el largo de las barras gráficas
    pct_correctas = round((correct / total) * 100, 2) if total else 0
    pct_incorrectas = round((incorrect / total) * 100, 2) if total else 0
    
    historial_respuestas = session.get('historial', [])

    return render_template('result.html',
                            totales=total,
                            correctas=correct,
                            incorrectas=incorrect,
                            porcentaje=percent,
                            pct_correctas=pct_correctas,
                            pct_incorrectas=pct_incorrectas,
                            historial=historial_respuestas)

app.add_url_rule('/', 'index', index, methods=['GET'])
app.add_url_rule('/quizes', 'quises_selection', quises_selection, methods=['GET', 'POST'])
app.add_url_rule('/test', 'test', test, methods=['GET', 'POST'])
app.add_url_rule('/result', 'result', result, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)