import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from datetime import datetime
from zoneinfo import ZoneInfo
import random
import requests
import json

# Configuración básica
TOKEN = "7725269349:AAGuTEMxnYYre1AA4BcO-_RL7N7Rz-cI3iU"  # Reemplaza con tu token real
BOT_USERNAME = "@DICIPLINE_TG_BOT"  # Reemplaza con el username de tu bot
# Configuración avanzada de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ======================================
# FUNCIONES AVANZADAS DEL BOT
# ======================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menú principal interactivo con botones"""
    keyboard = [
        [InlineKeyboardButton("⏰ Hora Mundial", callback_data='time_menu')],
        [InlineKeyboardButton("📊 Calculadora", callback_data='calc_menu')],
        [InlineKeyboardButton("🎲 Juegos", callback_data='games_menu')],
        [InlineKeyboardButton("ℹ️ Info Usuario", callback_data='user_info')],
        [InlineKeyboardButton("🌤 Clima", callback_data='weather_menu')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"✨ *¡Bienvenido a {BOT_USERNAME}!* ✨\n\n"
        "🔹 *Bot multifunción para pruebas*\n"
        "🔹 *Token en código* (solo testing)\n\n"
        "Selecciona una función:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def world_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra la hora en diferentes zonas con formato bonito"""
    time_zones = {
        "🌍 UTC": "UTC",
        "🇪🇸 Madrid": "Europe/Madrid",
        "🇲🇽 CDMX": "America/Mexico_City",
        "🇺🇸 NY": "America/New_York",
        "🇦🇷 Buenos Aires": "America/Argentina/Buenos_Aires",
        "🇨🇱 Santiago": "America/Santiago",
        "🇯🇵 Tokio": "Asia/Tokyo"
    }
    
    time_msg = "🕒 *Horas Mundiales* 🕒\n\n"
    for city, tz in time_zones.items():
        now = datetime.now(ZoneInfo(tz))
        time_msg += f"{city}: `{now.strftime('%H:%M:%S')}`\n"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Actualizar", callback_data='time_update')],
        [InlineKeyboardButton("🏠 Menú Principal", callback_data='main_menu')]
    ]
    
    await update.message.reply_text(
        time_msg,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra información detallada del usuario"""
    user = update.effective_user
    chat = update.effective_chat
    
    user_msg = (
        f"👤 *Información de Usuario*\n\n"
        f"🆔 *ID:* `{user.id}`\n"
        f"📛 *Nombre:* {user.full_name}\n"
        f"🔖 *Username:* @{user.username if user.username else 'N/A'}\n"
        f"💬 *Chat ID:* `{chat.id}`\n"
        f"📅 *Registrado:* Pendiente\n"
        f"🌐 *Idioma:* {user.language_code if user.language_code else 'Desconocido'}\n\n"
        f"🤖 *Es bot:* {'✅ Sí' if user.is_bot else '❌ No'}"
    )
    
    await update.message.reply_text(
        user_msg,
        parse_mode='Markdown'
    )

async def calculator_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menú de calculadora con operaciones básicas"""
    keyboard = [
        [InlineKeyboardButton("➕ Sumar", callback_data='calc_add'),
         InlineKeyboardButton("➖ Restar", callback_data='calc_sub')],
        [InlineKeyboardButton("✖️ Multiplicar", callback_data='calc_mul'),
         InlineKeyboardButton("➗ Dividir", callback_data='calc_div')],
        [InlineKeyboardButton("🏠 Menú Principal", callback_data='main_menu')]
    ]
    
    await update.message.reply_text(
        "🧮 *Calculadora* - Selecciona una operación:",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def games_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menú de juegos simples"""
    keyboard = [
        [InlineKeyboardButton("🎲 Dado", callback_data='game_dice')],
        [InlineKeyboardButton("🎯 Dardos", callback_data='game_darts')],
        [InlineKeyboardButton("🏀 Basketball", callback_data='game_basketball')],
        [InlineKeyboardButton("🔮 Adivina el número", callback_data='game_guess')],
        [InlineKeyboardButton("🏠 Menú Principal", callback_data='main_menu')]
    ]
    
    await update.message.reply_text(
        "🎮 *Juegos* - Selecciona un juego:",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def send_random_game(update: Update, context: ContextTypes.DEFAULT_TYPE, game_type: str):
    """Envía un juego interactivo de Telegram"""
    game_emoji = {
        'dice': '🎲',
        'darts': '🎯',
        'basketball': '🏀'
    }
    
    await context.bot.send_game(
        chat_id=update.effective_chat.id,
        game_short_name=game_type,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                f"Jugar {game_emoji.get(game_type, '🎮')}", 
                callback_data=f'play_{game_type}'
            )
        ]])
    )

async def weather_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menú de clima (requiere API key)"""
    keyboard = [
        [InlineKeyboardButton("📍 Por ubicación", callback_data='weather_location')],
        [InlineKeyboardButton("🏙 Por ciudad", callback_data='weather_city')],
        [InlineKeyboardButton("🏠 Menú Principal", callback_data='main_menu')]
    ]
    
    await update.message.reply_text(
        "🌤 *Clima* - Selecciona una opción:\n\n"
        "⚠️ *Nota:* Función en desarrollo, requiere API key",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ======================================
# MANEJADORES DE MENÚS Y CALLBACKS
# ======================================

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador central de callbacks"""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    
    if callback_data == 'main_menu':
        await start(update, context)
    elif callback_data == 'time_menu' or callback_data == 'time_update':
        await world_time(update, context)
    elif callback_data == 'user_info':
        await user_info(update, context)
    elif callback_data == 'calc_menu':
        await calculator_menu(update, context)
    elif callback_data == 'games_menu':
        await games_menu(update, context)
    elif callback_data == 'weather_menu':
        await weather_menu(update, context)
    elif callback_data.startswith('game_'):
        game_type = callback_data.split('_')[1]
        await send_random_game(update, context, game_type)
    elif callback_data.startswith('play_'):
        await query.answer(text="⚠️ Función de juego completa requiere configuración adicional", show_alert=True)
    elif callback_data.startswith('calc_'):
        await query.answer(text="🔢 Ingresa dos números separados por espacio. Ejemplo: 5 3")
    else:
        await query.answer(text="⚙️ Función en desarrollo")

# ======================================
# CONFIGURACIÓN Y EJECUCIÓN DEL BOT
# ======================================

def main():
    """Configuración principal del bot"""
    try:
        app = Application.builder().token(TOKEN).build()
        
        # Comandos
        app.add_handler(CommandHandler('start', start))
        app.add_handler(CommandHandler('time', world_time))
        app.add_handler(CommandHandler('info', user_info))
        app.add_handler(CommandHandler('calc', calculator_menu))
        app.add_handler(CommandHandler('games', games_menu))
        
        # Callbacks
        app.add_handler(CallbackQueryHandler(handle_callback))
        
        # Mensajes
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        logger.info(f"🤖 Bot {BOT_USERNAME} iniciado correctamente")
        app.run_polling()
    except Exception as e:
        logger.error(f"❌ Error crítico: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador de mensajes no comandos"""
    text = update.message.text.lower()
    
    # Respuestas inteligentes
    responses = {
        'hola': ['¡Hola! 👋', '¿Cómo estás?', '¡Buenos días! ☀️'],
        'adiós': ['Hasta luego 👋', 'Nos vemos pronto 😊', '¡Que tengas un buen día! 🌟'],
        'gracias': ['De nada 😊', '¡Es un placer ayudar!', '¡Gracias a ti! 🙏'],
        'bot': ['¡Sí, soy un bot! 🤖', 'Bot a tus órdenes ⚡', '¿Necesitas ayuda? 💡']
    }
    
    for keyword, replies in responses.items():
        if keyword in text:
            await update.message.reply_text(random.choice(replies))
            return
    
    # Si no reconoce el mensaje
    await update.message.reply_text(
        "No entiendo ese mensaje. Prueba con /start para ver las opciones",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Menú Principal", callback_data='main_menu')]
        ])
    )

if __name__ == '__main__':
    main()