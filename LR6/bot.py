from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Кнопки обычной клавиатуры (под строкой ввода)
    reply_keyboard = [
        [KeyboardButton("👋 Привет"), KeyboardButton("ℹ О боте")],
        [KeyboardButton("❓ Помощь")],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    # Инлайн-кнопка под сообщением
    inline_keyboard = [
        [InlineKeyboardButton("Нажми меня", callback_data="pressed")]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)

    await update.message.reply_text(
        "Привет! Я учебный бот с кнопками.\n"
        "Выбери что-нибудь на клавиатуре или нажми на инлайн-кнопку 👇",
        reply_markup=markup,
    )

    await update.message.reply_text(
        "Вот инлайн-кнопка:", reply_markup=inline_markup
    )


# Обработка текстов с обычной клавиатуры
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "👋 Привет":
        await update.message.reply_text("Привет-привет! ✌")
    elif text == "ℹ О боте":
        await update.message.reply_text("Я простой учебный бот для лабы по Python и Telegram.")
    elif text == "❓ Помощь":
        await update.message.reply_text("Нажми кнопки или используй команду /start, чтобы увидеть клавиатуру.")
    else:
        await update.message.reply_text(f"Ты отправил: {text}")


# Обработка инлайн-кнопок (callback_data)
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # чтобы Телеграм не думал, что кнопка зависла

    if query.data == "pressed":
        await query.message.reply_text("Ты нажал инлайн-кнопку! ✅")


def main():
    # Сюда вставь токен бота
    app = ApplicationBuilder().token("8512612379:AAFsRIyWlrqNABXM-zKMQDUAiRBuThuzJhw").build()

    # Команда /start
    app.add_handler(CommandHandler("start", start))

    # Обработка текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Обработка нажатий инлайн-кнопок
    app.add_handler(CallbackQueryHandler(button_callback))

    # Запуск бота — СИНХРОННЫЙ вызов, БЕЗ asyncio.run
    app.run_polling()


if __name__ == "__main__":
    main()
