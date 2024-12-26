from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Настройки базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверка на существование пользователя
        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Регистрация прошла успешно! Теперь можно войти.')
        return redirect(url_for('login'))

    return render_template('register.html')


# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Вы вошли на сайт!')
            return redirect(url_for('index'))

        flash('Неверный логин или пароль.')
    return render_template('login.html')


# Выход
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы вышли из своего аккаунта.')
    return redirect(url_for('login'))


# Список всех терминов
@app.route('/terms')
def terms():
    all_terms = Term.query.order_by(Term.term).all()
    return render_template('terms.html', terms=all_terms)


# Мои термины
@app.route('/my_terms', methods=['GET', 'POST'])
def my_terms():
    if 'user_id' not in session:
        flash('Пожалуйста, войдите на сайт.')
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        term = request.form['term']
        definition = request.form['definition']

        new_term = Term(term=term, definition=definition, user_id=user_id)
        db.session.add(new_term)
        db.session.commit()

        flash('Термин добавлен!')

    my_terms = Term.query.filter_by(user_id=user_id).all()
    return render_template('my_terms.html', terms=my_terms)


# Удаление термина
@app.route('/delete_term/<int:term_id>')
def delete_term(term_id):
    if 'user_id' not in session:
        flash('Пожалуйста, войдите на сайт.')
        return redirect(url_for('login'))

    term = Term.query.get_or_404(term_id)

    # Удалить можно только свои термины
    if term.user_id != session['user_id']:
        flash('Вы не можете удалить чужой термин.')
        return redirect(url_for('my_terms'))

    db.session.delete(term)
    db.session.commit()
    flash('Термин удалён.')
    return redirect(url_for('my_terms'))


# Переводчик
@app.route('/translate', methods=['GET', 'POST'])
def translate():
    translated_text = None

    if request.method == 'POST':
        text = request.form['text']
        terms = Term.query.all()

        # Замена слов на их определения
        for term in terms:
            text = text.replace(term.term, f'{term.term} ({term.definition})')

        translated_text = text

    return render_template('translate.html', translated_text=translated_text)


if __name__ == '__main__':
    app.run(debug=True)
