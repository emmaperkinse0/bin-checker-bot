from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 启动命令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("欢迎使用 BIN 查询机器人，请发送一个 6 位的 BIN 号即可查询相关信息。")

# 处理 BIN 号
async def handle_bin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    bin_input = text.split()[0][:6]
    if not bin_input.isdigit() or len(bin_input) != 6:
        await update.message.reply_text("请输入有效的 6 位 BIN 号。")
        return

    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_input}")
        if response.status_code == 200:
            data = response.json()
            info = f"""💳 BIN: {bin_input}
银行: {data.get('bank', {}).get('name', '未找到')}
卡种: {data.get('scheme', '未找到').upper()}
卡类型: {data.get('type', '未找到')}
品牌: {data.get('brand', '未找到')}
国家: {data.get('country', {}).get('name', '未找到')} ({data.get('country', {}).get('alpha2', '')})"""
            await update.message.reply_text(info)
        else:
            await update.message.reply_text("未能查询到该 BIN 的相关信息。")
    except:
        await update.message.reply_text("查询发生错误，请稍后再试。")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_bin))
    app.run_polling()
