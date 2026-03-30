import os
import sqlite3
import requests
from flask import Flask, render_template, request, jsonify

import sqlite3
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')

# --- CONFIGURACIÓN DE FIERRO (ESTO TIENE QUE ESTAR ACÁ ARRIBA) ---
DB_NAME = "negocio.db"
TELEGRAM_TOKEN = "7953336143:AAF3dohzoE9_m9JmKKHo_QemjRSCeDZVsFk"
MI_CHAT_ID = 6028197335         
GRUPO_TECNICOS_ID = -1002422964864  
ADMIN_KEY = "lanus2026_secreto_99"  # <--- ESTA ES LA QUE TE FALTA
app = Flask(__name__, template_folder='templates')


# --- CONFIGURACIÓN DE FIERRO ---
DB_NAME = "negocio.db"
TELEGRAM_TOKEN = "7953336143:AAF3dohzoE9_m9JmKKHo_QemjRSCeDZVsFk"
MI_CHAT_ID = 6028197335  # Tu ID real verificado

def init_db():
    """Crea las tablas de turnos y consultas si no existen"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tabla para turnos del Bot
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS turnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT, telefono TEXT, servicio TEXT, fecha TEXT, hora TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
    # Tabla para consultas del Formulario Web
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT, whatsapp TEXT, servicio TEXT, mensaje TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
    conn.commit()
    conn.close()

def avisar_a_pedro(mensaje):
    """Envía un mensaje de Telegram a tu chat personal"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": MI_CHAT_ID, 
        "text": mensaje, 
        "parse_mode": "Markdown"
    }
    try:
        # Usamos json=payload para asegurar la compatibilidad
        requests.post(url, json=payload)
    except Exception as e:
        print(f"❌ Error enviando aviso a Telegram: {e}")

@app.route('/')
def index():
    """Sirve la página principal de Mano Derecha"""
    return render_template('index.html')

@app.route('/api/nuevo_turno', methods=['POST'])
def nuevo_turno():
    """Recibe turnos desde el Bot de Telegram"""
    d = request.json
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO turnos (nombre, telefono, servicio, fecha, hora) VALUES (?,?,?,?,?)',
                   (d['nombre'], d['telefono'], d['servicio'], d['fecha'], d['hora']))
    conn.commit()
    conn.close()
    
    # Aviso al celular de Pedro
    msg = f"📅 *¡NUEVO TURNO AGENDADO!*\n\n👤 *Cliente:* {d['nombre']}\n🔧 *Servicio:* {d['servicio']}\n📅 *Fecha:* {d['fecha']}\n⏰ *Hora:* {d['hora']} hs\n📱 *Tel:* {d['telefono']}"
    avisar_a_pedro(msg)
    
    return jsonify({"status": "ok"})

@app.route('/api/consulta_web', methods=['POST'])
def consulta_web():
    """Recibe consultas desde el formulario de la Web"""
    nombre = request.form.get('nombre')
    whatsapp = request.form.get('whatsapp')
    servicio = request.form.get('servicio')
    mensaje = request.form.get('mensaje')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO consultas (nombre, whatsapp, servicio, mensaje) VALUES (?,?,?,?)',
                   (nombre, whatsapp, servicio, mensaje))
    conn.commit()
    conn.close()

    # Aviso al celular de Pedro
    msg = f"📧 *NUEVA CONSULTA WEB*\n\n👤 *Nombre:* {nombre}\n📱 *WA:* {whatsapp}\n🔧 *Interés:* {servicio}\n💬 *Mensaje:* {mensaje}"
    avisar_a_pedro(msg)

    return jsonify({"status": "success"})

@app.route('/admin_panel')
def admin_panel():
    # Esta es la llave maestra, cambiala por algo difícil si querés
    password_maestra = "lanus2026_secreto_99" 
    
    # Buscamos la contraseña que viene en la URL: /admin_panel?key=lanus2026_secreto_99
    auth = request.args.get('key')
    
    if auth != password_maestra:
        return "<h1>🛑 Acceso Denegado</h1><p>Mano Derecha dice que no tenés permiso.</p>", 403

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM turnos ORDER BY timestamp DESC'); t = cursor.fetchall()
    cursor.execute('SELECT * FROM consultas ORDER BY timestamp DESC'); c = cursor.fetchall()
    conn.close()
    return render_template('admin.html', turnos=t, consultas=c)
@app.route('/api/borrar_turno/<int:id>')
def borrar_turno(id):
    key = request.args.get('key')
    # Aquí es donde fallaba porque no encontraba ADMIN_KEY arriba
    if key != ADMIN_KEY: 
        return "Error de Llave", 403
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM turnos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return f"<script>alert('Turno Borrado'); window.location.href='/admin_panel?key={ADMIN_KEY}';</script>"

@app.route('/api/borrar_consulta/<int:id>')
def borrar_consulta(id):
    key = request.args.get('key')
    if key != ADMIN_KEY: 
        return "Error de Llave", 403
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM consultas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return f"<script>alert('Consulta Borrada'); window.location.href='/admin_panel?key={ADMIN_KEY}';</script>"
if __name__ == '__main__':
    init_db()
    # Ejecutamos en el puerto 5000
    app.run(debug=True, port=5000)