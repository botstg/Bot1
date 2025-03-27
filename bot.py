import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuración básica
TOKEN = "7725269349:AAGuTEMxnYYre1AA4BcO-_RL7N7Rz-cI3iU"  # Reemplaza con tu token real
BOT_USERNAME = "@DICIPLINE_TG_BOT"  # Reemplaza con el username de tu bot

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Comandos
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('¡Hola! Soy un bot simple. ¿En qué puedo ayudarte?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Comandos disponibles:
    /start - Inicia el bot
    /help - Muestra este mensaje de ayuda
    /info - Muestra información sobre el bot
    """
    await update.message.reply_text(help_text)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Soy un bot de ejemplo creado para demostrar cómo desplegar en GitHub Actions.')

# Manejo de mensajes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if 'hola' in text:
        response = '¡Hola! ¿Cómo estás?'
    elif 'adiós' in text:
        response = '¡Hasta luego!'
    else:
        response = 'No entiendo ese mensaje. Prueba con /help'
    
    await update.message.reply_text(response)

# Manejo de errores
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    
    # Comandos
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('info', info_command))
    
    # Mensajes
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errores
    app.add_error_handler(error)
    
    logger.info("Bot iniciado...")
    app.run_polling()