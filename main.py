from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os
import logging

# 设置日志记录
logging.basicConfig(filename='bin_queries.log', level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 启动命令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("欢迎使用 BIN 查询机器人，请发送一个 6 位的 BIN 号即可查询相关信息。")

# 处理 BIN 号查询
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

            # 记录查询到的 BIN 信息
            logging.info(f"BIN 查询: {bin_input} | 结果: {info}")
        else:
            await update.message.reply_text("未能查询到该 BIN 的相关信息。")
    except Exception as e:
        await update.message.reply_text(f"查询发生错误：{str(e)}")
        logging.error(f"查询错误: {str(e)}")

if __name__ == '__main__':
    # 获取端口，默认 5000
    port = os.environ.get("PORT", 5000)

    # 创建机器人实例
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 添加处理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_bin))

    # 运行机器人，绑定到指定端口
    app.run_polling(port=port)
