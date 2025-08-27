from flask import Flask, render_template, send_file, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os

app = Flask(__name__, template_folder='htmls')
app.config['SECRET_KEY'] = 'SuperSecretKey'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
db_path = os.path.join(INSTANCE_DIR, 'db.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class Client(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100))
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, default=None)
    phoneNumber = db.Column(db.String(100), default=None)
    className = "Client"

    def check_password(self, password):
        return self.password == password

    def __init__(self, name, surname, password, email, phoneNumber):
        self.name = name
        self.surname = surname
        self.password = password
        self.phoneNumber = phoneNumber
        self.email = email
        max_id = 0

        for client in Client.query:
            if client.id > max_id:
                max_id = client.id

        for driver in Driver.query:
            if driver.id > max_id:
                max_id = driver.id

        for admin in Admin.query:
            if admin.id > max_id:
                max_id = admin.id
        self.id = max_id + 1


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100))
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, default=None)
    experience = db.Column(db.String(100), default=None)
    phoneNumber = db.Column(db.String(100), default=None)
    className = "Admin"

    def check_password(self, password):
        return self.password == password

    def __init__(self, name, surname, password, experience, phoneNumber, email):
        self.name = name
        self.surname = surname
        self.password = password
        self.phoneNumber = phoneNumber
        self.email = email
        self.experience = experience
        max_id = 0

        for client in Client.query:
            if client.id > max_id:
                max_id = client.id

        for driver in Driver.query:
            if driver.id > max_id:
                max_id = driver.id

        for admin in Admin.query:
            if admin.id > max_id:
                max_id = admin.id
        self.id = max_id + 1


class Driver(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100))
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, default=None)
    experience = db.Column(db.String(100), default=None)
    phoneNumber = db.Column(db.String(100), default=None)
    cargoID = db.Column(db.Integer, default=-1)
    className = "Driver"

    def check_password(self, password):
        return self.password == password

    def __init__(self, name, surname, password, experience, phoneNumber, email, cargoID):
        self.name = name
        self.surname = surname
        self.password = password
        self.phoneNumber = phoneNumber
        self.email = email
        self.experience = experience
        self.cargoID = cargoID
        max_id = 0

        for client in Client.query:
            if client.id > max_id:
                max_id = client.id

        for driver in Driver.query:
            if driver.id > max_id:
                max_id = driver.id

        for admin in Admin.query:
            if admin.id > max_id:
                max_id = admin.id
        self.id = max_id + 1


class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer, nullable=False)
    cargoInformation = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    routeId = db.Column(db.Integer, nullable=False)
    addInfo = db.Column(db.String(100), nullable=False)
    driverId = db.Column(db.Integer)
    clientId = db.Column(db.Integer, nullable=False)
    isDone = db.Column(db.Boolean, default=0)

    def __init__(self, weight, cargoInformation, size, routeId, addInfo, client_id):
        self.weight = weight
        self.cargoInformation = cargoInformation
        self.size = size
        self.routeId = routeId
        self.addInfo = addInfo
        self.driverId = -1
        self.clientId = client_id
        counter = 1
        for cargo in Cargo.query:
            if cargo.id != counter:
                self.id = counter
                break
            else:
                counter += 1
        self.id = counter


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    start = db.Column(db.String(100), nullable=False)
    end = db.Column(db.String(100), nullable=False)

    def __init__(self, payment, distance, start, end):
        self.payment = payment
        self.distance = distance
        self.start = start
        self.end = end
        counter = 1
        for route in Route.query:
            if route.id != counter:
                self.id = counter
                break
            else:
                counter += 1
        self.id = counter


@login_manager.user_loader
def load_user(user_id):
    client = Client.query.get(int(user_id))
    if client:
        return client
    driver = Driver.query.get(int(user_id))
    if driver:
        return driver
    admin = Admin.query.get(int(user_id))
    if admin:
        return admin


@app.route('/logIn', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = Client.query.filter_by(email=email).first()
    if user is not None:
        if user and user.check_password(password):
            login_user(user)

            return jsonify({'message': 'Logged in successfully'}), 200
    driver = Driver.query.filter_by(email=email).first()
    if driver is not None:
        if driver and driver.check_password(password):
            login_user(driver)

            return jsonify({'message': 'Logged in successfully'}), 200
    admin = Admin.query.filter_by(email=email).first()
    if admin is not None:
        if admin and admin.check_password(password):
            login_user(admin)

            return jsonify({'message': 'Logged in successfully'}), 200
    return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/request', methods=['POST'])
def reque():
    try:
        weight = request.form['weight']
        isinstance(float(weight), float)

        cargoInformation = request.form['cargoInformation']
        size = request.form['size']
        route = request.form['route']
        addInfo = request.form['addInfo']

        newCargo = Cargo(weight, cargoInformation, size, route, addInfo, current_user.id)
        db.session.add(newCargo)
        db.session.commit()
        return jsonify({'message': 'Sended successfully'}), 200
    except():
        return jsonify({'message': 'Something wrong'}), 400


@app.route('/driverAccept', methods=['POST'])
def driverAccept():
    try:
        driverRouteId = request.form['driverRouteId']
        current_user.cargoID = driverRouteId
        Cargo.query.filter_by(id=driverRouteId).first().driverId = current_user.id

        db.session.commit()
        return jsonify({'message': 'Accept successfully'}), 200
    except():
        return jsonify({'message': 'Something wrong'}), 400


@app.route('/driverConfirm', methods=['POST'])
def driverConfirm():
    try:
        Cargo.query.filter_by(id=current_user.cargoID).first().isDone = True
        current_user.cargoID = -1
        db.session.commit()
        return jsonify({'message': 'Confirm successfully'}), 200
    except():
        return jsonify({'message': 'Something wrong'}), 400


@app.route('/getReport', methods=['POST'])
def getReport():
    try:
        clients_count = Client.query.count()
        active_drivers_count = Driver.query.filter_by(is_active=True).count()
        done_cargos_count = Cargo.query.filter_by(isDone=True).count()
        not_done_cargos_count = Cargo.query.filter_by(isDone=False).count()

        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        data = [['Item', 'Count'],
                ['Clients', clients_count],
                ['Active Drivers', active_drivers_count],
                ['Done Cargos', done_cargos_count],
                ['Not Done Cargos', not_done_cargos_count]]
        table = Table(data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)

        doc.build([table])
        pdf_buffer.seek(0)

        filename = 'report.pdf'
        with open(filename, 'wb') as f:
            f.write(pdf_buffer.getvalue())

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return str(e)


@app.route('/logIn', methods=["GET"])
def logIn():
    return render_template('logIn.html')


@app.route('/addDriver', methods=['POST'])
def addDriver():
    try:
        clientEmail = request.form['clientEmail']
        ourClient = Client.query.filter_by(email=clientEmail).first()
        if ourClient:
            db.session.delete(ourClient)

            newDriver = Driver(name=ourClient.name, surname=ourClient.surname, password=ourClient.password,
                               experience=0, phoneNumber=ourClient.phoneNumber, email=ourClient.email, cargoID=-1)
            db.session.add(newDriver)
            db.session.commit()

            return jsonify({'message': 'Done successfully'}), 200
        else:
            return jsonify({'message': 'Client not found'}), 404
    except():
        return jsonify({'message': 'Something wrong'}), 400


@app.route('/signUp', methods=['POST'])
def signUp():
    try:
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']

        newClient = Client(name=name, surname=surname, password=password, email=email, phoneNumber=-1)
        db.session.add(newClient)
        db.session.commit()
        login_user(newClient)

        return jsonify({'message': 'Sign up successfully'}), 200
    except():
        return jsonify({'message': 'Something wrong'}), 400


@app.route('/quitAccount', methods=["POST"])
def quitAcc():
    logout_user()
    return render_template('index.html')


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/contacts', methods=["GET"])
def contacts():
    return render_template('contacts.html')


@app.route('/news', methods=["GET"])
def news():
    return render_template('news.html')


@app.route('/account', methods=["GET"])
def account():
    try:
        routes = Route.query.all()
        client = Client.query.get(current_user.id)
        if client:
            all_user_cargo = Cargo.query.filter_by(clientId=current_user.id, isDone=False).all()
            return render_template('account.html', routes=routes, all_user_cargo=all_user_cargo)
        driver = Driver.query.get(current_user.id)
        if driver:
            driverCargo = Cargo.query.filter_by(driverId=current_user.id, isDone=False).all()
            allCargo = Cargo.query.all()
            return render_template('account.html', routes=routes, allCargo=allCargo, driverCargo=driverCargo)
        admin = Admin.query.get(current_user.id)
        if admin:
            return render_template('account.html')
    except:
        return render_template('logIn.html')


@app.route('/transportation', methods=["GET"])
def transportation():
    return render_template('transportation.html')


@app.route("/sitemap")
def sitemap():
    from flask import make_response, request, render_template
    from urllib.parse import urlparse

    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc

    static_urls = list()
    for rule in app.url_map.iter_rules():
        if not str(rule).startswith("/admin") and not str(rule).startswith("/user"):
            if "GET" in rule.methods and len(rule.arguments) == 0:
                url = {
                    "loc": f"{host_base}{str(rule)}"
                }
                static_urls.append(url)

    xml_sitemap = render_template("sitemap.html", static_urls=static_urls, host_base=host_base)
    response = make_response(xml_sitemap)

    return response


@app.route('/header.html', methods=["GET"])
def header():
    return render_template('header.html')


@app.route('/footer.html', methods=["GET"])
def footer():
    return render_template('footer.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
