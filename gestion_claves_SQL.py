from flask import Flask, request, render_template_string
import sqlite3
import hashlib

app = Flask(__name__)

#cracion de tabla
def inicializar_bd():
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            clave TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

inicializar_bd()

#hash claves
def encriptar_clave(clave_plana):
    return hashlib.sha256(clave_plana.encode()).hexdigest()

#HTML 
html_registro = '''
<!doctype html>
<title>Registro</title>
<h2>Registro de Usuario</h2>
<form method="POST">
  Usuario: <input type="text" name="usuario"><br>
  Contraseña: <input type="password" name="clave"><br>
  <input type="submit" value="Registrar">
</form>
<p><a href="/login">Ir a Login</a></p>
{% if mensaje %}
  <p><strong>{{ mensaje }}</strong></p>
{% endif %}
'''

#HTML para sesion
html_login = '''
<!doctype html>
<title>Inicio de Sesión</title>
<h2>Login</h2>
<form method="POST">
  Usuario: <input type="text" name="usuario"><br>
  Contraseña: <input type="password" name="clave"><br>
  <input type="submit" value="Ingresar">
</form>
<p><a href="/">Volver al Registro</a></p>
{% if mensaje %}
  <p><strong>{{ mensaje }}</strong></p>
{% endif %}
'''

@app.route("/", methods=["GET", "POST"])
def registro():
    mensaje = ""
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave_plana = request.form["clave"]
        if usuario and clave_plana:
            clave_hash = encriptar_clave(clave_plana)
            conexion = sqlite3.connect("usuarios.db")
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES (?, ?)", (usuario, clave_hash))
            conexion.commit()
            conexion.close()
            mensaje = f"Usuario '{usuario}' registrado correctamente con clave segura."
        else:
            mensaje = "Todos los campos son obligatorios."
    return render_template_string(html_registro, mensaje=mensaje)
@app.route("/login", methods=["GET", "POST"])
def login():
    mensaje = ""
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave_plana = request.form["clave"]
        clave_hash = encriptar_clave(clave_plana)
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND clave = ?", (usuario, clave_hash))
        resultado = cursor.fetchone()
        conexion.close()
        if resultado:
            mensaje = f"Bienvenido/a, {usuario}."
        else:
            mensaje = "Usuario o contraseña incorrecta."
    return render_template_string(html_login, mensaje=mensaje)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5800)
