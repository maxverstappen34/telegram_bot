
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler,filters


TOKEN = "8833186570:AAEAUw6dcMxB7RLnxRJn4bHe2T2WtLmsXKw"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your bot. How can I assist you today?")
    
async def echo(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    print("Bot is running...")
    app.run_polling()