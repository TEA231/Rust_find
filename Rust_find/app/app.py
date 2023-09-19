from flask import Flask, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@db/servers_db'
db = SQLAlchemy(app)


class Servers_p(db.Model):
    name_s = db.Column(db.Text, primary_key=True)
    old_s = db.Column(db.Text)
    online_s = db.Column(db.Text)
    connect_s = db.Column(db.Text)
    online_id_s = db.Column(db.Integer)


class Servers_l(db.Model):
    name_s = db.Column(db.Text, primary_key=True)
    old_s = db.Column(db.Text)
    online_s = db.Column(db.Text)
    connect_s = db.Column(db.Text)
    online_id_s = db.Column(db.Integer)


@app.route('/', methods=['POST', 'GET'])
@app.route('/main', methods=['POST', 'GET'])
def main():
    return render_template('main.html')
    

@app.route('/servers', methods=['POST', 'GET'])
def servers():
    return render_template('servers.html')


@app.route('/monuments', methods=['POST', 'GET'])
def monuments():
    return render_template('monuments.html')


@app.route('/servers_p', methods=['POST', 'GET'])
def setvers_p_d():
    articles = Servers_p.query.order_by(Servers_p.online_id_s.desc()).all()
    return render_template('servers_p.html', articles=articles)


@app.route('/servers_l', methods=['POST', 'GET'])
def servers_l_d():
    articles = Servers_l.query.order_by(Servers_l.online_id_s.desc()).all()
    return render_template('servers_l.html', articles=articles)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
