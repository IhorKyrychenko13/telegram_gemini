
import os
import telebot
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    prompt = f"Ты — эксперт по Нидерландам. Вопрос: {message.text}\nОтвет:"
    try:
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text.strip())
    except Exception as e:
        print("Ошибка Gemini:", e)
        bot.reply_to(message, "⚠️ Ошибка при обращении к Gemini API.")

print("Бот запущен")
bot.polling()
