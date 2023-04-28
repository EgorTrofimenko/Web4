from flask import Flask, render_template, url_for, request, redirect, session, flash
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, date, time
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)  # объект

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sadada'

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
@app.route('/login.html', methods=['GET', 'POST'])
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
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Защищенный маршрут, доступный только авторизованным пользователям
@app.route('/')
def index():
    return render_template('index.html')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    color = db.Column(db.String(100))
    material_up = db.Column(db.String(100))
    material_down = db.Column(db.String(100))
    season = db.Column(db.String(100))
    sports = db.Column(db.String(100))
    size = db.Column(db.String(100))
    text = db.Column(db.Text)
    price = db.Column(db.Integer)

    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repl__(self):
        return '<Product %r> %self.id'


@app.route('/dashboard.html')
def dashboard():
    if current_user.is_authenticated:
        # user = User.query.filter_by(username=session['username']).first()
        return redirect(url_for('logout'))
    return redirect(url_for('login'))


def getpath_for_pict(base, model):
    md = model.replace(" ", "_")
    return base + md + '.png'


app.jinja_env.globals.update(getpath_for_pict=getpath_for_pict)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about.html')  # отслеживание
def about():
    return render_template("about.html")  # "Aboutasdfasdf"


@app.route('/brands.html')  # отслеживание
def brands():
    return render_template("brands.html")  # "Aboutasdfasdf"


@app.route('/Nike.html')  # отслеживание
def Nike():
    sneakers_list = Product.query.filter_by(brand="Nike")
    return render_template("Nike.html", sneakers_list=sneakers_list)  # "Aboutasdfasdf"


@app.route('/Adidas.html')  # отслеживание
def Adidas():
    sneakers_list = Product.query.filter_by(brand="Adidas")
    return render_template("Adidas.html", sneakers_list=sneakers_list)


@app.route('/NB.html')  # отслеживание
def NB():
    sneakers_list = Product.query.filter_by(brand="New Balance")
    return render_template("NB.html", sneakers_list=sneakers_list)


@app.route('/header.html')  # отслеживание
def header():
    return render_template("header.html")


@app.route('/end.html')  # отслеживание
def end():
    return render_template("end.html")


@app.route('/footer.html')  # отслеживание
def footer():
    return render_template("footer.html")


@app.route('/store.html')  # отслеживание
def store():
    i = request.args.get("id")
    sneakers_list = Product.query.filter_by(id=i)
    return render_template("store.html", sneakers_list=sneakers_list)


@app.route('/Main_sneck.html')  # отслеживание
def Main_sneck():
    i = request.args.get("id")
    sneakers_list = Product.query.filter_by(id=i)
    return render_template("Main_sneck.html", sneakers_list=sneakers_list)


if __name__ == '__main__':
    app.run(debug=True)  # команда запускает локальный сервер, ошибки выводятся на сайт
