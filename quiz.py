from flask import Flask, redirect, url_for, session, request, render_template
from database import get_next_question, get_quises

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NoTieneClave'


def start_quiz(quiz_id):
    # Convertimos explicitamente a int (para mantener la integridad del dato acorde a la DB)
    session['quiz'] = int(quiz_id)
    session['prev_question'] = 0
    session['correctas'] = 0
    session['totales'] = 0


def end_quiz():
    session.clear()

def check_answer():
    resp_usuario = request.form.get('ans_text')
    resp_correcta = session.get('last_correct')

    if resp_usuario:
        session['totales'] += 1
        if resp_usuario == str(resp_correcta):
            session['correctas'] += 1


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
    # si no hay un quiz activo en la session, regresa al index
    if 'quiz' not in session or 'prev_question' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        check_answer()

    result = get_next_question(session['prev_question'], session['quiz'])

    if result is None or result == 0:
        return redirect(url_for('result'))
    
    session['prev_question'] = result[0]
    session['last_correct'] = result[2]

    respuestas = list(result[2:6]) # MEZCLEN LAS RESPUESTAS
    print(session.get('totales', 'correctas'))
    return render_template('test.html', pregunta=result[1], opciones=respuestas)
    


def result():
    return 'RESULTADO DEL TEST'


# Configuración de Rutas
app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
app.add_url_rule('/test', 'test', test, methods=['GET', 'POST'])
app.add_url_rule('/result', 'result', result)

if __name__ == "__main__":
    app.run(debug=True)
