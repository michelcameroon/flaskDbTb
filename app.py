from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///solarCalc4.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#migrate = Migrate(app, db)
app.app_context().push()

class Battery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nameBrand = db.Column(db.String(100), nullable=False)
    voltage = db.Column(db.Integer, nullable=False)
    energyInWatth = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/batteries')
def list_batteries():
    batteries = Battery.query.all()
    return render_template('list.html', batteries=batteries)

@app.route('/battery/new', methods=['GET', 'POST'])
def new_battery():
    if request.method == 'POST':
        nameBrand = request.form['nameBrand']
        voltage = request.form['voltage']
        energyInWatth = request.form['energyInWatth']
        new_battery = Battery(nameBrand=nameBrand, voltage=voltage, energyInWatth=energyInWatth)
        db.session.add(new_battery)
        db.session.commit()
        return redirect(url_for('list_batteries'))
    return render_template('new.html')

@app.route('/battery/update/<int:id>', methods=['GET', 'POST'])
def update_battery(id):
    battery = Battery.query.get_or_404(id)
    if request.method == 'POST':
        battery.nameBrand = request.form['nameBrand']
        battery.voltage = request.form['voltage']
        battery.energyInWatth = request.form['energyInWatth']
        db.session.commit()
        return redirect(url_for('list_batteries'))
    return render_template('update.html', battery=battery)

@app.route('/battery/delete/<int:id>', methods=['GET', 'POST'])
def delete_battery(id):
    battery = Battery.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(battery)
        db.session.commit()
        return redirect(url_for('list_batteries'))
    return render_template('delete.html', battery=battery)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
