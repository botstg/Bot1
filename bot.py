import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from datetime import datetime
from zoneinfo import ZoneInfo

# ⚠️ ATENCIÓN: Esto es SOLO PARA PRUEBAS LOCALES ⚠️
# Nunca hagas commit/push de este token a repositorios públicos
TOKEN = "7725269349:AAGuTEMxnYYre1AA4BcO-_RL7N7Rz-cI3iU"
BOT_USERNAME = "@DICIPLINE_TG_BOT"

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Función para crear menús de botones
def create_menu(buttons, columns=2):
    return [buttons[i:i+columns] for i in range(0, len(buttons), columns)]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🕒 Hora Actual", callback_data='time')],
        [InlineKeyboardButton("ℹ️ Información", callback_data='info')],
        [InlineKeyboardButton("🔍 Mi Información", callback_data='user_info')]
    ]
    
    reply_markup = InlineKeyboardMarkup(create_menu(keyboard[0], 2))
    
    await update.message.reply_text(
        f"👋 ¡Hola! Soy {BOT_USERNAME}\n"
        "🔹 Bot de prueba con todas las funciones\n"
        "🔹 Token incluido en código (SOLO PRUEBAS)\n\n"
        "Selecciona una opción:",
        reply_markup=reply_markup
    )

async def show_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    zones = {
        "🇪🇸 Madrid": "Europe/Madrid",
        "🇲🇽 CDMX": "America/Mexico_City",
        "🇦🇷 Buenos Aires": "America/Argentina/Buenos_Aires"
    }
    
    time_msg = "🕒 <b>Horas mundiales:</b>\n\n"
    for city, tz in zones.items():
        time_msg += f"{city}: <code>{datetime.now(ZoneInfo(tz)).strftime('%H:%M:%S')}</code>\n"
    
    await update.message.reply_text(time_msg, parse_mode='HTML')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'time':
        await show_time(update, context)
    elif query.data == 'info':
        await query.edit_message_text(
            "ℹ️ <b>Información del Bot</b>\n\n"
            f"Nombre: {BOT_USERNAME}\n"
            "Modo: Pruebas\n"
            "⚠️ Token en código (solo testing)",
            parse_mode='HTML'
        )

if __name__ == '__main__':
    try:
        app = Application.builder().token(TOKEN).build()
        
        # Handlers
        app.add_handler(CommandHandler('start', start))
        app.add_handler(CallbackQueryHandler(button_handler))
        
        logger.info(f"Iniciando bot {BOT_USERNAME}...")
        app.run_polling()
    except Exception as e:
        logger.error(f"Error crítico: {e}")