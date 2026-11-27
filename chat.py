import logging
import os
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# API Keys (Environment variables ලෙස හෝ කෙලින්ම මෙහි යොදන්න)
TELEGRAM_TOKEN = os.getenv("8800233820:AAFWccO8LeHty7SlAo1QniR2KcsU8pVauj4")
GEMINI_API_KEY = os.getenv("AQ.Ab8RN6JiBnKazFLXEclWDt42oCcw3AtyJbUAg59BgdX9QHi8qg")

# Logging සැහැල්ලුවෙන් තබා ගැනීම (disk/memory ඉතිරි කර ගැනීමට)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
)

# Gemini client ආරම්භ කිරීම
client = genai.Client(api_key=GEMINI_API_KEY)

# /start command එක
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "ආයුබෝවන්! මම ඔබේ AI සහායකයා. මගෙන් ඕනෑම දෙයක් අසන්න."
    )

# සාමාන්‍ය messages වලට පිළිතුරු දීම
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    if not user_text:
        return

    # "Typing..." status එක පෙන්වීම
    await update.message.chat.send_action(action="typing")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text,
        )
        reply_text = response.text or "මට එයට පිළිතුරක් සකසා ගත නොහැකි විය."

        # Telegram message character limit (4096) ආරක්ෂා කිරීම
        for i in range(0, len(reply_text), 4000):
            await update.message.reply_text(reply_text[i : i + 4000])

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text(
            "තාක්ෂණික දෝෂයක් ඇති වුණා. කරුණාකර පසුව නැවත උත්සාහ කරන්න."
        )

def main() -> None:
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()