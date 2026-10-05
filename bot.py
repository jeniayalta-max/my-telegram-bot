import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from anthropic import Anthropic

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")

client = Anthropic(api_key=CLAUDE_API_KEY)

SYSTEM_PROMPT = "Ты дружелюбный помощник, отвечающий от имени владельца этого бота. Отвечай кратко и естественно."

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_text}]
    )

    answer = response.content[0].text
    await update.message.reply_text(answer)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    app.run_polling()

if __name__ == "__main__":
    main()
