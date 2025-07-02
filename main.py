from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os

# 设置你的Bot Token
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 启动命令，发送欢迎消息
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("欢迎使用BIN查询机器人！请输入BIN号进行查询。")

# 处理BIN查询
async def handle_bin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    bin_input = text.split()[0][:6]

    # 检查BIN号是否合法
    if not bin_input.isdigit() or len(bin_input) != 6:
        await update.message.reply_text("请输入有效的6位BIN号。")
        return

    try:
        # 发送请求获取BIN信息
        response = requests.get(f"https://lookup.binlist.net/{bin_input}")
        if response.status_code == 200:
            data = response.json()
            info = f"BIN: {bin_input}\n" \
                   f"银行: {data.get('bank', {}).get('name', '未知')}\n" \
                   f"卡片类型: {data.get('scheme', '未知')}\n" \
                   f"卡片类型: {data.get('type', '未知')}\n" \
                   f"品牌: {data.get('brand', '未知')}\n" \
                   f"国家: {data.get('country', {}).get('name', '未知')}"
            await update.message.reply_text(info)
        else:
            await update.message.reply_text("未能查询到此BIN的相关信息。")
    except Exception as e:
        await update.message.reply_text("查询时出错，请稍后再试。")

# 设置并运行Bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_bin))
    app.run_polling()
