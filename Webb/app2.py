# Подключение необходимых библиотек и модулей
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Создание приложения Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ss1'

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
db = SQLAlchemy(app)

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Определение модели пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

with app.app_context():
    db.create_all()

# Функция для загрузки пользователя из базы данных
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Маршрут для регистрации нового пользователя
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('login'))
    return render_template('register.html')


# Маршрут для авторизации пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Неверное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')


# Маршрут для выхода из учетной записи
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Защищенный маршрут, доступный только авторизованным пользователям
@app.route('/')
def index():
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)
