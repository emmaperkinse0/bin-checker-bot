from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("欢迎使用BIN查询机器人，请发送6位BIN号，多个BIN号请用空格分隔。")

# Handle BIN command
async def handle_bin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # 将输入的BIN号按空格拆分成多个BIN
    bin_inputs = text.split()

    # 存储查询结果的列表
    results = []

    for bin_input in bin_inputs:
        # 验证BIN号是否为6位数字
        if not bin_input.isdigit() or len(bin_input) != 6:
            await update.message.reply_text(f"输入的BIN号 '{bin_input}' 无效，请确保它是6位数字。")
            return

        try:
            # 请求BIN查询接口
            response = requests.get(f"https://lookup.binlist.net/{bin_input}")
            if response.status_code == 200:
                data = response.json()
                info = f"""
BIN号: {bin_input}
银行: {data.get('bank', {}).get('name', '未知')}
卡片类型: {data.get('scheme', '未知')}
卡片种类: {data.get('type', '未知')}
品牌: {data.get('brand', '未知')}
国家: {data.get('country', {}).get('name', '未知')}
"""
                results.append(info)
            else:
                results.append(f"未找到BIN号 {bin_input} 的相关信息。")
        except Exception as e:
            results.append(f"查询BIN号 {bin_input} 时发生错误：{str(e)}")

    # 将所有结果作为一条消息返回
    await update.message.reply_text("\n\n".join(results))

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_bin))
    app.run_polling()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_bin))
    app.run_polling()
