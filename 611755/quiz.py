from flask import Flask, redirect, url_for, session, request, render_template
from database import get_next_question, get_quises
import random
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NoTieneClave'


def start_quiz(quiz_id):
    session['quiz'] = int(quiz_id)
    session['prev_question'] = 0
    session['correctas'] = 0
    session['totales'] = 0
    
    # Obtenemos el total real de preguntas de este quiz para calcular el % perfecto
    try:
        conn = sqlite3.connect("quises.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM quiz_content WHERE quiz_id = ?", [quiz_id])
        session['max_preguntas'] = cursor.fetchone()[0] or 5 # 5 por defecto si falla
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


def index():
    if request.method == 'GET':
        end_quiz()
        quises_list = get_quises()
        return render_template('index.html', quises=quises_list)
    else:
        quiz_id = request.form.get('quiz')
        if quiz_id:
            start_quiz(quiz_id)
            return redirect(url_for('test'))
        return redirect(url_for('index'))


def test():
    if 'quiz' not in session or 'prev_question' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        check_answer()

    result = get_next_question(session['prev_question'], session['quiz'])

    if result is None or result == 0:
        return redirect(url_for('result'))
    
    session['prev_question'] = result[0]
    session['last_correct'] = result[2]

    # Mezclamos las opciones
    respuestas = list(result[2:6]) 
    random.shuffle(respuestas) 

    # CÁLCULO DEL PORCENTAJE EXACTO Y REAL
    # El progreso actual representa las preguntas que ya va a responder (ej: pregunta 1 de 5 = 20%)
    preguntas_vistas = session.get('totales', 0) + 1
    max_preguntas = session.get('max_preguntas', 5)
    
    porcentaje_barra = round((preguntas_vistas / max_preguntas) * 100)
    if porcentaje_barra > 100:
        porcentaje_barra = 100

    return render_template('test.html', 
                           pregunta=result[1], 
                           opciones=respuestas, 
                           progreso=porcentaje_barra)


def result():
    if 'totales' not in session:
        return redirect(url_for('index'))
    
    total = session.get('totales', 0)
    correct = session.get('correctas', 0)
    incorrect = total - correct
    percent = calc_stats(total, correct)

    return render_template('result.html',
                            totales=total,
                            correctas=correct,
                            incorrectas=incorrect,
                            porcentaje=percent)

app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
app.add_url_rule('/test', 'test', test, methods=['GET', 'POST'])
app.add_url_rule('/result', 'result', result, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)
