from asyncio.windows_events import NULL
from flask import Flask, render_template, redirect, url_for, request
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root' #depende del usuario que asignaron en heidiSQL
app.config['MYSQL_DATABASE_PASSWORD'] = '1234' #depende de la contraseña que asignaron en heidiSQL
app.config['MYSQL_DATABASE_DB'] = 'petclub'

mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def inicio():
	return render_template('index.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/info')
def info():
	return render_template('info.html')

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/client')
def dataclient():
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT nombre, especie, edad, nombre_owner, cedula, correo FROM cliente")
	datos = cursor.fetchall()
	return render_template('dataclient.html', datos = datos)

@app.route('/hitorialcita')
def historialcita():
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT fecha, hora, fk_cliente FROM cita")
	datos = cursor.fetchall()
	return render_template('histcita.html', datos = datos)	

@app.route('/cita')
def cita():
	return render_template('cita.html')

@app.route('/nuevoregistro')
def nuevoregistro():
	return render_template('nuevoregistro.html')

#Pagina para confirmar los datos ingresados del nuevo cliente
@app.route('/confirmarnuevoregistro', methods=['POST'])
def confirmarnuevoregistro():
	if request.method == 'POST':
		varNombre = request.form['nombre']
		varEspecie = request.form['especie']
		varEdad = request.form['edad']
		varNombreOwner = request.form['nombre_owner']
		varCedula = request.form['cedula']
		varCorreo = request.form['correo']
		varCPassword = request.form['password']
		cursor = mysql.get_db().cursor()
		cursor.execute("insert into cliente values (%s,%s,%s,%s,%s,%s,%s)",(varNombre, varEspecie, varEdad, varNombreOwner, varCedula, varCorreo, varCPassword))
		mysql.get_db().commit()
		return redirect(url_for('inicio'))

@app.route('/confirmarcita', methods=['POST'])
def confirmarcita():
	if request.method == 'POST':
		varfecha = request.form['fecha']
		varHora = request.form['hora']
		varcedula= request.form['fk_cliente']
		cursor = mysql.get_db().cursor()
		cursor.execute("insert into cita values (%s,%s,%s)",(varfecha, varHora, varcedula))
		mysql.get_db().commit()
		return redirect(url_for('historialcita'))

if __name__ == '__main__':
	app.run(port=3000, debug=True)
