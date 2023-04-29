from flask import Flask, render_template, request, url_for, redirect  # , jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from datetime import datetime, timedelta
from random import randint

# import phonenumbers
# from validate_email import validate_email
import ast

from AlexZapl_db import db

from forex_python.converter import CurrencyRates
import bcrypt

db_debug = False
orders = []
uses = []
app = Flask(__name__)
langs = ['eng', 'lt', 'ru']
loans_history = {}

app.config.update(
    SECRET_KEY='it is nat a secret key PhPHpHPHPHPhPhPHpHhPhppHhp'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


def hashed_password(plain_text_password):
    # Мы добавляем "соль" к нашему пароль, чтобы сделать его декодирование невозможным
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(login):
    return User(login)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return 'Пока'


@app.route('/')
def index():
    # Система языков
    lang = request.args.get('lang', 'eng')
    if lang == 'eng':
        content_ = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[1].strip())

        Buttons = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[0].strip())

    elif lang == 'lt':
        content_ = ast.literal_eval(open('langs\\lt.lang', 'r', encoding='utf-8').readlines()[1].strip())

        Buttons = ast.literal_eval(open('langs\\lt.lang', 'r', encoding='utf-8').readlines()[0].strip())
    elif lang == 'ru':
        content_ = ast.literal_eval(open('langs\\ru.lang', 'r', encoding='utf-8').readlines()[1].strip())

        Buttons = ast.literal_eval(open('langs\\ru.lang', 'r', encoding='utf-8').readlines()[0].strip())

    else:
        lang = 'eng'

        content_ = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[1].strip())

        Buttons = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[0].strip())

    if str(current_user.__class__) == "<class 'flask_login.mixins.AnonymousUserMixin'>":
        log = "1"
        a = 'login'
        log2 = 'Login'
    else:
        log = '2'
        a = 'logout'
        log2 = 'Logout'

    return render_template('index.html', a=a, log2=log2, **content_, **Buttons, lang=lang)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Система языков
    lang = request.args.get('lang', 'eng')
    if lang == 'eng':
        Buttons = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[0].strip())
    elif lang == 'lt':
        Buttons = ast.literal_eval(open('langs\\lt.lang', 'r', encoding='utf-8').readlines()[0].strip())
    elif lang == 'ru':
        Buttons = ast.literal_eval(open('langs\\ru.lang', 'r', encoding='utf-8').readlines()[0].strip())
    else:
        lang = 'eng'

        Buttons = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[0].strip())

    # Проверка есть ли такой пользователь
    if request.method == 'POST':
        row = db.users.get('login', request.form['login'])
        if not row:
            return render_template('login.html', error='Неправильный логин или пароль', a="/register", log2='Sign up',
                                   **Buttons, lang=lang)
        if request.form['password'] == row.password:
            user = User(row.login)  # Создаем пользователя
            login_user(user)  # Логинем пользователя
            if db_debug:
                print('LOGIN DEBUG: login succes')
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Неправильный логин или пароль', a="/register", log2='Sign up',
                                   **Buttons, lang=lang)
    return render_template('login.html', a="/register", log2='Sign up', **Buttons, lang=lang)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Система языков
    lang = request.args.get('lang', 'eng')
    if lang == 'eng':
        Buttons = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[0].strip())
    elif lang == 'lt':
        Buttons = ast.literal_eval(open('langs\\lt.lang', 'r', encoding='utf-8').readlines()[0].strip())
    elif lang == 'ru':
        Buttons = ast.literal_eval(open('langs\\ru.lang', 'r', encoding='utf-8').readlines()[0].strip())
    else:
        lang = 'eng'

        Buttons = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[0].strip())

    # Регистрация
    if request.method == 'POST':
        for key in request.form:
            if not request.form[key]:
                return render_template('register.html', message='Все поля должны быть заполнены!', a='login',
                                       log2='Log in', **Buttons, lang=lang)
        #
        if request.form['password'] != request.form['password_check']:
            return render_template('register.html', message='Пароли не совпадают', a='login', log2='Log in', **Buttons,
                                   lang=lang)

        if db.users.get('login', request.form['login']):
            return render_template('register.html', message='Данное имя пользователя существует', a='login',
                                   log2='Log in', **Buttons, lang=lang)
        elif db.users.get('email', request.form['email']) or db.users.get('phone_number', request.form['phone_number']):
            return render_template('register.html', message='Данная почта или номер телефона уже используется',
                                   a='login', log2='Log in', **Buttons, lang=lang)
        # Подготовка данных для бд
        login_date = datetime.now()
        reg_all = db.users.get_all()
        id_ = reg_all[-1].id + 1 if reg_all else 1
        data_users = {'login': request.form['login'], 'password': request.form['password'],
                      'login_date': login_date.date(), 'id': id_, 'phone_number': request.form['phone_number'],
                      'email': request.form['email'], 'name': request.form['name'], 'fname': request.form['fname'],
                      'cash': 0}
        # Генерация карты
        cardid_gen = True
        cvv_gen = True
        cardid_ = 0
        cvv_ = ""
        while cardid_gen:
            cardid_ = f'7777 {randint(0, 9)}{randint(0, 9)}{randint(0, 9)}{randint(0, 9)} {randint(0, 9)}{randint(0, 9)}{randint(0, 9)}{randint(0, 9)} {randint(0, 9)}{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}'
            if cardid_ == db.card.get('cardid', cardid_):
                pass
            else:
                break
        enddate = login_date + timedelta(days=360 * 5 + 1)
        while cvv_gen:
            cvv_ = f'{randint(1, 9)}{randint(0, 9)}{randint(0, 9)}'
            if cvv_ == db.card.get('cvv', cvv_):
                pass
            else:
                break
        # Добавление в бд
        data_card = {'userid': id_, 'cardid': cardid_, 'enddate': enddate, 'cvv': cvv_, 'currency': 'EUR', 'cash': 0}
        db.users.put(data=data_users)
        db.card.put(data=data_card)
        return render_template('register.html', message='Регистрация прошла успешно', a='login', log2='Log in',
                               **Buttons, lang=lang)

    return render_template('register.html', message="Register", a='login', log2='Log in', **Buttons, lang=lang)


@app.route('/banking/card')
@login_required
def card():
    # Система языков
    lang = request.args.get('lang', 'eng')
    if lang == 'eng':
        Buttons = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[0].strip())
    elif lang == 'lt':
        Buttons = ast.literal_eval(open('langs\\lt.lang', 'r', encoding='utf-8').readlines()[0].strip())
    elif lang == 'ru':
        Buttons = ast.literal_eval(open('langs\\ru.lang', 'r', encoding='utf-8').readlines()[0].strip())
    else:
        lang = 'eng'

        Buttons = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[0].strip())

    # Подгрузка данных карты
    user = f'{str(current_user.id)}'
    print(user)
    id_ = db.users.get('login', user)
    print(id_.id)
    carduser_ = db.card.get('userid', id_.d)
    cardnumber = carduser_.cardid
    expires_ = str(carduser_.enddate)
    name_ = f'{id_.name} {id_.fname}'
    cvv_ = carduser_.cvv
    expires = f'{expires_[5]}{expires_[6]}/{expires_[2]}{expires_[3]}'

    log = '2'
    a = 'logout'
    log2 = 'Logout'

    return render_template('card.html', name=name_, expires=expires, card_number=cardnumber, cvv=cvv_, a=a, log2=log2,
                           **Buttons, lang=lang)


@app.route('/contacts')
def contacts():
    # Система языков
    lang = request.args.get('lang', 'eng')
    if lang == 'eng':
        Buttons = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[0].strip())
    elif lang == 'lt':
        Buttons = ast.literal_eval(open('langs\\lt.lang', 'r', encoding='utf-8').readlines()[0].strip())
    elif lang == 'ru':
        Buttons = ast.literal_eval(open('langs\\ru.lang', 'r', encoding='utf-8').readlines()[0].strip())
    else:
        lang = 'eng'

        Buttons = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[0].strip())

    if str(current_user.__class__) == "<class 'flask_login.mixins.AnonymousUserMixin'>":
        log = "1"
        a = 'login'
        log2 = 'Login'
    else:
        log = '2'
        a = 'logout'
        log2 = 'Logout'

    return render_template('contacts.html', a=a, log2=log2, **Buttons)


@app.route('/banking/loans', methods=['GET', 'POST'])
@login_required
def loans():
    # Система языков
    lang = request.args.get('lang', 'eng')
    if lang == 'eng':
        content_ = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[2].strip())

        Buttons = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[0].strip())
    elif lang == 'lt':
        content_ = ast.literal_eval(open('langs\\lt.lang', 'r', encoding='utf-8').readlines()[2].strip())

        Buttons = ast.literal_eval(open('langs\\lt.lang', 'r', encoding='utf-8').readlines()[0].strip())
    elif lang == 'ru':
        content_ = ast.literal_eval(open('langs\\ru.lang', 'r', encoding='utf-8').readlines()[2].strip())

        Buttons = ast.literal_eval(open('langs\\ru.lang', 'r', encoding='utf-8').readlines()[0].strip())
    else:
        lang = 'eng'

        content_ = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[2].strip())

        Buttons = ast.literal_eval(open('langs\\eng.lang', 'r', encoding='utf-8').readlines()[0].strip())

    log = '2'
    a = 'logout'
    log2 = 'Logout'

    if request.method == 'POST':
        for key in request.form:
            print(key, request.form.get(key), key.__class__)
        # Проверка ввода данных
        if 'loan' in request.form:
            date = datetime.strptime(request.form.get('dateend'), '%Y-%m-%d').date()
            delta = date - datetime.now().date()
            rem_days = delta.total_seconds() / (24 * 3600)

            loan2 = request.form.get("loan")
            # Проверка времени на сдачу + подготовка данных
            if rem_days < 10:
                return render_template('loans.html', err='Кредит меньше чем на 10 дней нельзя брать', a=a, log2=log2,
                                       **Buttons, **content_, lang=lang)
            elif rem_days > 730:
                return render_template('loans.html', err='Кредит больше чем на 2 года нельзя брать', a=a, log2=log2,
                                       **Buttons, **content_, lang=lang)

            if ',' in loan2:
                loan = float(loan2.replace(',', '.'))
            if '.' in loan2:
                loan = float(loan2)
                oplm2 = round(loan / (rem_days / 30) * 1.121, 2)
                oplt2 = round(oplm2 * (rem_days / 30), 2)
                c = CurrencyRates()
                oplm = f"{oplm2}$/{round(c.convert('USD', 'EUR', oplm2), 2)}€"
                oplt = f"{oplt2}$/{round(c.convert('USD', 'EUR', oplt2), 2)}€"

            else:
                return render_template('loans.html', err='Не правильный способ ввода', a=a, log2=log2, **Buttons,
                                       **content_, lang=lang)
            err = ''
            user = f'{str(current_user.id)}'
            loans_history[user] = [loan, oplm, oplt2, rem_days, request.form.get('dateend')]
            print(f'{loans_history}\n{loans_history[user]}')
            return render_template('loans.html', a=a, log2=log2, oplm=oplm, oplt=oplt, err=err, **Buttons, **content_,
                                   lang=lang, loan=f'{loan}$')
        # Подготовка к получению кредита
        elif 'getcr' in request.form:
            user = f'{str(current_user.id)}'
            userloans = loans_history[user]
            print(userloans[1])
            return render_template('loans.html', a=a, log2=log2, **Buttons, **content_, lang=lang, getcr=True,
                                   loan=userloans[1])
        # кредит идёт в бд
        elif 'tot-getcr' in request.form:
            user = f'{str(current_user.id)}'
            print(user)
            id_ = db.users.get('login', user)
            print(id_.id)
            userloans = loans_history[user]

            data_loans = {'userid': id_.id, 'dateend': userloans[4], 'loan': userloans[2]}
            print(data_loans)
            db.loans.put(data=data_loans)

    return render_template('loans.html', a=a, log2=log2, **Buttons, **content_, lang=lang)


@app.errorhandler(404)
def err404(e):
    return render_template('404page.html'), 404

@app.errorhandler(500)
def err500(e):
    return render_template('500page.html'), 500


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=1000)
