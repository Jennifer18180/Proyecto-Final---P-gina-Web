from flask import Flask, redirect, url_for, session, request
from database import get_next_question, get_quises


app = Flask(__name__)

def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['prev_question'] = 0

def end_quiz():
    session.clear()

def quiz_form():
    # ESTABLECER LA PLANTILLA HTML PARA LA LISTA DE QUISES
    quises_list = get_quises() #CREARLA EN LA DATABASE 

    for id, name in quises_list:
        #construir el formulario con los articulos de la tupla
        pass

    return quises
def index():
    if request.method = 'GET':
        start_quiz(-1)

        return quiz_form() # esto devuelve la str de la plantilla
    else:
        quiz_id = request.form.get('quiz')
        start_quiz(quiz_id)
        return redirect(url_for('test'))
    

def test():
    result = get_next_question(session['prev_question'], session['quiz'])
    if result is None or result == 0:
        return redirect(url_for('result'))
    else:
        session['prev_question'] = result[0]
    
    return f'{result}'

def result():
    return 'Aqui se muestra el resultado!'

app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
app.add_url_rule('/test', 'test', test)
app.add_url_rule('/result', 'result', result)

app.config['SECRET_KEY'] = 'LaClaveMasSecretaDelMundo'
if __name__ == "__main__":
    app.run()