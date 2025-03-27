import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from datetime import datetime
import pytz

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

# Función para crear teclados inline
def build_menu(buttons, n_cols=2):
    return [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

# Comandos mejorados con emojis y botones
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['help']} Ayuda", callback_data='help')],
        [InlineKeyboardButton(f"{EMOJIS['info']} Información", callback_data='info')],
        [InlineKeyboardButton(f"{EMOJIS['user']} Mis datos", callback_data='user_info')],
        [InlineKeyboardButton(f"{EMOJIS['time']} Hora actual", callback_data='current_time')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
    {EMOJIS['start']} *¡Hola! Soy tu Bot Avanzado* {EMOJIS['start']}

    🌟 *¿Qué puedo hacer por ti hoy?* 🌟
    
    Puedes usar los botones o los comandos:
    /start - Iniciar el bot
    /help - Mostrar ayuda
    /info - Información del bot
    /time - Hora actual
    /userinfo - Tus datos de usuario
    /id - Tu ID de Telegram
    """
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = f"""
    {EMOJIS['help']} *Menú de Ayuda* {EMOJIS['help']}

    📌 *Comandos disponibles:*
    
    /start - {EMOJIS['start']} Inicia el bot
    /help - {EMOJIS['help']} Muestra este mensaje
    /info - {EMOJIS['info']} Información del bot
    /time - {EMOJIS['time']} Hora en diferentes zonas
    /userinfo - {EMOJIS['user']} Tus datos de usuario
    /id - {EMOJIS['id']} Muestra tu ID de Telegram
    /settings - {EMOJIS['settings']} Configuraciones (próximamente)
    
    🔍 También puedes usar los botones interactivos!
    """
    
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['back']} Volver al inicio", callback_data='start')],
        [InlineKeyboardButton(f"{EMOJIS['info']} Ver información", callback_data='info')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        help_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = f"""
    {EMOJIS['info']} *Información del Bot* {EMOJIS['info']}
    
    🤖 *Nombre:* Bot Avanzado
    📅 *Versión:* 2.0
    🛠 *Desarrollador:* Tu Nombre
    📌 *Funciones:*
    - Información de usuario
    - Consulta de hora
    - Interacción con botones
    - Comandos personalizados
    
    🌐 *Código fuente:* [GitHub Repo](https://github.com/tu-usuario/tu-repo)
    """
    
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['back']} Volver", callback_data='start')],
        [InlineKeyboardButton(f"{EMOJIS['help']} Ayuda", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        info_text,
        parse_mode='Markdown',
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    time_zones = {
        "Madrid": "Europe/Madrid",
        "México": "America/Mexico_City",
        "Argentina": "America/Argentina/Buenos_Aires",
        "Colombia": "America/Bogota",
        "Chile": "America/Santiago",
        "Perú": "America/Lima",
        "EEUU (NY)": "America/New_York",
        "EEUU (LA)": "America/Los_Angeles",
        "Londres": "Europe/London",
        "Tokio": "Asia/Tokyo"
    }
    
    time_text = f"{EMOJIS['time']} *Horas Mundiales* {EMOJIS['time']}\n\n"
    
    for city, tz in time_zones.items():
        now = datetime.now(pytz.timezone(tz))
        time_text += f"⏳ *{city}:* `{now.strftime('%H:%M:%S')}`\n"
    
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['back']} Volver", callback_data='start')],
        [InlineKeyboardButton(f"{EMOJIS['time']} Actualizar", callback_data='current_time')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        time_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def userinfo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    
    user_info = f"""
    {EMOJIS['user']} *Información de Usuario* {EMOJIS['user']}
    
    👤 *Nombre:* {user.full_name}
    🆔 *ID:* `{user.id}`
    📝 *Username:* @{user.username if user.username else 'No tiene'}
    💬 *Chat ID:* `{chat.id}`
    📅 *Fecha registro Telegram:* Pendiente
    🌐 *Idioma:* {user.language_code if user.language_code else 'No especificado'}
    
    🔍 *Más datos técnicos:*
    - Tipo chat: {chat.type}
    - Bot: {'✅ Sí' if user.is_bot else '❌ No'}
    """
    
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['id']} Ver solo ID", callback_data='show_id')],
        [InlineKeyboardButton(f"{EMOJIS['back']} Volver", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        user_info,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    await update.message.reply_text(
        f"{EMOJIS['id']} *Tu ID de Telegram es:* `{user.id}` {EMOJIS['id']}",
        parse_mode='Markdown'
    )

# Manejo de mensajes mejorado
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    response = ""
    
    greetings = ['hola', 'hello', 'hi', 'buenos días', 'buenas tardes']
    farewells = ['adiós', 'bye', 'hasta luego', 'nos vemos']
    
    if any(g in text for g in greetings):
        response = f"{EMOJIS['success']} ¡Hola! ¿Cómo estás hoy? {random.choice(['😊', '👋', '🤗'])}"
    elif any(f in text for f in farewells):
        response = f"{EMOJIS['success']} ¡Hasta luego! Que tengas un buen día {random.choice(['🌟', '✨', '🌞'])}"
    elif 'gracias' in text:
        response = f"{EMOJIS['success']} ¡De nada! Estoy aquí para ayudarte {EMOJIS['help']}"
    elif 'bot' in text:
        response = f"{EMOJIS['info']} ¡Sí, soy un bot! Pero intento ser útil {EMOJIS['success']}"
    else:
        response = f"{EMOJIS['warning']} No entiendo ese mensaje. Prueba con /help {EMOJIS['help']}"
    
    await update.message.reply_text(response)

# Manejo de callbacks (botones)
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'start':
        await start_command(update, context)
    elif query.data == 'help':
        await help_command(update, context)
    elif query.data == 'info':
        await info_command(update, context)
    elif query.data == 'user_info':
        await userinfo_command(update, context)
    elif query.data == 'current_time':
        await time_command(update, context)
    elif query.data == 'show_id':
        await id_command(update, context)

# Manejo de errores
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning(f'Update {update} caused error {context.error}')
    
    if update.message:
        await update.message.reply_text(
            f"{EMOJIS['error']} ¡Ups! Algo salió mal. Intenta nuevamente o usa /help {EMOJIS['help']}"
        )

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    
    # Comandos
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('info', info_command))
    app.add_handler(CommandHandler('time', time_command))
    app.add_handler(CommandHandler('userinfo', userinfo_command))
    app.add_handler(CommandHandler('id', id_command))
    
    # Callbacks (botones)
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # Mensajes
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Errores
    app.add_error_handler(error)
    
    logger.info("Bot iniciado... Presiona Ctrl+C para detenerlo")
    app.run_polling()