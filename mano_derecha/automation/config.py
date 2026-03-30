import os

# --- CREDENCIALES DE ACCESO ---
# En Railway/Vercel, configuraremos estas variables en sus paneles.
TOKEN = os.getenv("TELEGRAM_TOKEN", "7953336143:AAF3dohzoE9_m9JmKKHo_QemjRSCeDZVsFk")
MONGO_URI = os.getenv("MONGO_URI", "TU_CADENA_DE_CONEXION_DE_MONGO_AQUI")
MI_CHAT_ID = int(os.getenv("MI_CHAT_ID", "6028197335"))
GRUPO_TECNICOS_ID = int(os.getenv("GRUPO_TECNICOS_ID", "-1002422964864"))
ADMIN_KEY = "lanus2026_secreto_99"

# --- CONFIGURACIÓN DEL NEGOCIO ---
NEGOCIO = {
    "nombre": "Mano Derecha",
    "rubro": "Digitalización de Procesos Locales.",
    "descripcion": 'Mano Derecha es la solución tecnológica "de fierro" para el que labura día a día. Nos especializamos en la Digitalización de Procesos Locales, transformando el mostrador de los negocios de Lanús en un sistema moderno y automático.',
    "horario": "24/7",
    "telefono": "1144940576",
    "email": "",
    "direccion": "Lanus Buenos Aires",
    "servicios": [
        {'nombre': 'Tu Vidriera Digital (Web de Alta Calidad)', 'descripcion': 'Creamos una página web profesional y rápida para que los vecinos te encuentren primero en Google.'},
        {'nombre': 'El Recepcionista Inteligente (Bot)', 'descripcion': 'Instalamos un asistente automático que atiende los mensajes al toque.'},
        {'nombre': 'Agenda y Pedidos en Piloto Automático', 'descripcion': 'Organizamos tus turnos y pedidos de mercadería de forma digital.'},
        {'nombre': 'Tu Negocio Bajo Control (Reportes)', 'descripcion': 'Te enviamos un informe sencillo directamente a tu celular.'}
    ],
    "faq": [
        {'pregunta': '¿Es muy difícil de usar?', 'respuesta': 'Quedate tranquilo, Pedro se encarga de todo. Vos solo recibís notificaciones.'},
        {'pregunta': '¿Tengo que pagar una fortuna?', 'respuesta': 'Para nada. Es una renta mensual cómoda para el que la pelea día a día.'}
    ],
    "redes": {
        'instagram': 'https://www.instagram.com/', 
        'facebook': 'https://www.facebook.com/', 
        'whatsapp': 'https://wa.me/1144940576', 
        'web': 'www.ManoDerecha.com'
    }
}

# --- CEREBRO IA (TU PROMPT ORIGINAL) ---
PROMPT_IA = """Actúa como asistente virtual de Mano Derecha.

INFORMACIÓN:
- Negocio: Mano Derecha
- Rubro: Digitalización de Procesos Locales.
- Descripción: Mano Derecha es la solución tecnológica "de fierro" para el que labura día a día. Nos especializamos en la Digitalización de Procesos Locales, transformando el mostrador de los negocios de Lanús en un sistema moderno y automático.
- Horario: 24/7
- Dirección: Lanus Buenos Aires
- Teléfono: 1144940576

SERVICIOS:
   • Tu Vidriera Digital: Web profesional para captar clientes 24/7.
   • El Recepcionista Inteligente (Bot): Asistente que atiende mensajes al toque.
   • Agenda y Pedidos Pro: Organización digital de turnos sin errores.
   • Reportes de Bolsillo: Informe claro de tus resultados mensuales.

OBJETIVO:
1. Atender clientes amablemente.
2. Ayudar a agendar turnos.
3. Responder dudas usando el estilo de "dar una mano".

RESPONDE EN FORMATO JSON:
{
  "mensaje": "Texto para el cliente",
  "accion": "pedir_nombre|pedir_telefono|pedir_servicio|pedir_fecha|pedir_hora|confirmar",
  "datos": {}
}
"""