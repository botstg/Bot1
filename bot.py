import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from datetime import datetime
from zoneinfo import ZoneInfo  # Alternativa moderna a pytz (incluida en Python 3.9+)

# Configuración básica
TOKEN = "7725269349:AAGuTEMxnYYre1AA4BcO-_RL7N7Rz-cI3iU"  # Reemplaza con tu token real
BOT_USERNAME = "@DICIPLINE_TG_BOT"  # Reemplaza con el username de tu bot
# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Emojis para decoración
EMOJIS = {
    "start": "🚀",
    "help": "❓",
    "info": "ℹ️",
    "time": "⏰",
    "user": "👤",
    "id": "🆔",
    "settings": "⚙️",
    "error": "❌",
    "success": "✅",
    "warning": "⚠️",
    "back": "🔙"
}

# Función para mostrar la hora en diferentes zonas
async def show_time(update: Update):
    time_zones = {
        "Madrid": ZoneInfo("Europe/Madrid"),
        "México": ZoneInfo("America/Mexico_City"),
        "Argentina": ZoneInfo("America/Argentina/Buenos_Aires"),
        "Colombia": ZoneInfo("America/Bogota")
    }
    
    time_text = f"{EMOJIS['time']} <b>Horas Mundiales</b> {EMOJIS['time']}\n\n"
    
    for city, tz in time_zones.items():
        now = datetime.now(tz)
        time_text += f"🕒 <b>{city}:</b> <code>{now.strftime('%H:%M:%S')}</code>\n"
    
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['back']} Volver", callback_data='start')],
        [InlineKeyboardButton(f"{EMOJIS['time']} Actualizar", callback_data='time')]
    ]
    
    await update.message.reply_text(
        time_text,
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Comando de inicio simplificado
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['time']} Hora actual", callback_data='time')],
        [InlineKeyboardButton(f"{EMOJIS['info']} Info bot", callback_data='info')]
    ]
    
    await update.message.reply_text(
        f"{EMOJIS['start']} <b>Bot de Pruebas Activo</b> {EMOJIS['start']}\n\n"
        "Este es un bot de prueba con el token incluido directamente en el código.",
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Manejador de botones
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'time':
        await show_time(update)
    elif query.data == 'info':
        await query.edit_message_text(
            f"{EMOJIS['info']} <b>Bot de Pruebas</b>\n\n"
            "Token incluido directamente en el código.\n"
            "Solo para desarrollo y pruebas.",
            parse_mode='HTML'
        )
    elif query.data == 'start':
        await start(update, context)

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    
    # Comandos
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('time', show_time))
    
    # Botones
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # Errores
    app.add_error_handler(lambda u, c: logger.error(f"Error: {c.error}"))
    
    logger.info(f"Iniciando bot @{BOT_USERNAME}...")
    app.run_polling()