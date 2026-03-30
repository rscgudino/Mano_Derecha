import logging
import requests
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes, ConversationHandler)
from config import NEGOCIO, PROMPT_IA

# --- CONFIGURACIÓN ---
TELEGRAM_BOT_TOKEN = "7953336143:AAF3dohzoE9_m9JmKKHo_QemjRSCeDZVsFk"
# En producción (Vercel), esta URL cambiará a tu link de vercel.app
WEB_URL = os.getenv("WEB_URL", "http://127.0.0.1:5000/api/nuevo_turno")
# Estados de la conversación
NOMBRE, TELEFONO, SERVICIO, FECHA, HORA, CONFIRMAR = range(6)

class BotNegocio:
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN

    async def enviar_a_web(self, datos):
        """Envía el turno a la base de datos de la Web"""
        try:
            response = requests.post(WEB_URL, json=datos, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"⚠️ Error conectando con la Web: {e}")
            return False

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Saludo inicial con la descripción del config.py"""
        nombre_agencia = NEGOCIO["nombre"]
        img_url = "https://images.unsplash.com/photo-1551434678-e076c223a692?w=800&q=80"
        
        saludo = (
            f"🚀 *¡BIENVENIDO A {nombre_agencia.upper()}!*\n\n"
            f"{NEGOCIO['descripcion']}\n\n"
            "🎁 *TENÉS UN REGALO:* 10% OFF en cualquier plan técnico.\n\n"
            "¿Qué querés hacer hoy?"
        )
        
        kb = [[InlineKeyboardButton("📅 Agendar Turno Técnico", callback_data="turno")],
              [InlineKeyboardButton("💬 Hablar con Pedro (WhatsApp)", url=NEGOCIO['redes']['whatsapp'])]]
        
        await update.message.reply_photo(
            photo=img_url,
            caption=saludo,
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="Markdown"
        )

    async def iniciar_turno(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text("Perfecto. ¿Cuál es tu **Nombre y Apellido**?")
        return NOMBRE

    async def recibir_nombre(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['nombre'] = update.message.text
        await update.message.reply_text(f"De diez, {update.message.text}. Ahora pasame tu **WhatsApp**:")
        return TELEFONO

    async def recibir_telefono(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['telefono'] = update.message.text
        # Armamos botones basados en los servicios del config.py
        kb = [[InlineKeyboardButton("Vidriera Digital", callback_data="Vidriera")],
              [InlineKeyboardButton("Bot Recepcionista", callback_data="Bot")],
              [InlineKeyboardButton("Combo Patrón", callback_data="Full")]]
        await update.message.reply_text("¿En qué servicio estás interesado?", reply_markup=InlineKeyboardMarkup(kb))
        return SERVICIO

    async def recibir_servicio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        context.user_data['servicio'] = query.data
        await query.edit_message_text(f"Elegiste: {query.data}. ¿Para qué **fecha**? (Ej: 20/05)")
        return FECHA

    async def recibir_fecha(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['fecha'] = update.message.text
        await update.message.reply_text("¿A qué **hora** te queda bien? (Ej: 15:30)")
        return HORA

    async def recibir_hora(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['hora'] = update.message.text
        d = context.user_data
        resumen = (f"📋 **RESUMEN DE TU TURNO**\n\n"
                   f"👤 Nombre: {d['nombre']}\n"
                   f"🔧 Servicio: {d['servicio']}\n"
                   f"📅 Fecha: {d['fecha']}\n"
                   f"⏰ Hora: {d['hora']}\n"
                   f"📱 WhatsApp: {d['telefono']}\n\n"
                   f"¿Está todo bien?")
        kb = [[InlineKeyboardButton("✅ Confirmar", callback_data="confirmar")],
              [InlineKeyboardButton("❌ Cancelar", callback_data="cancelar")]]
        await update.message.reply_text(resumen, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
        return CONFIRMAR

    async def confirmar_final(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        if query.data == "confirmar":
            exito = await self.enviar_a_web(context.user_data)
            if exito:
                await query.edit_message_text("🎉 **¡LISTO!** Pedro ya recibió tu pedido y te va a contactar.")
            else:
                await query.edit_message_text("⚠️ Guardamos el turno, pero Pedro te confirmará manualmente en un ratito.")
        else:
            await query.edit_message_text("❌ Turno cancelado. Podés volver a empezar con /start.")
        
        return ConversationHandler.END

    def run(self):
        app = ApplicationBuilder().token(self.token).build()
        
        conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.iniciar_turno, pattern="^turno$")],
            states={
                NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.recibir_nombre)],
                TELEFONO: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.recibir_telefono)],
                SERVICIO: [CallbackQueryHandler(self.recibir_servicio)],
                FECHA: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.recibir_fecha)],
                HORA: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.recibir_hora)],
                CONFIRMAR: [CallbackQueryHandler(self.confirmar_final)],
            },
            fallbacks=[CommandHandler("start", self.start)],
        )

        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(conv_handler)
        
        print("🤖 Bot de Mano Derecha encendido y esperando turnos...")
        app.run_polling()

if __name__ == "__main__":
    BotNegocio().run()