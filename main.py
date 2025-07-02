from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("欢迎使用BIN查询机器人，请发送6位BIN号即可。")

async def handle_bin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    bin_input = text.split()[0][:6]
    if not bin_input.isdigit() or len(bin_input) != 6:
        await update.message.reply_text("请输入有效的6位数字BIN号。")
        return

    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_input}")
        if response.status_code == 200:
            data = response.json()
            info = f"""💳 BIN: {bin_input}
Bank: {data.get('bank', {}).get('name', 'N/A')}
Scheme: {data.get('scheme', 'N/A').upper()}
Type: {data.get('type', 'N/A')}
Brand: {data.get('brand', 'N/A')}
Country: {data.get('country', {}).get('name', 'N/A')} ({data.get('country', {}).get('alpha2', '')})"""
            await update.message.reply_text(info)
        else:
            await update.message.reply_text("未找到该BIN的信息。")
    except:
        await update.message.reply_text("查询失败，请稍后再试。")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_bin))
    app.run_polling()
