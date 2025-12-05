import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
# from telebot import apihelper
#
# apihelper.proxy = {
#     "https": "socks5://tW4DMw:R22K0D@168.80.83.176:8000"
# }

BOT_TOKEN = "8588268136:AAFOKZU5y87f-M4vqendfZS8CtXYGr43F6c"

bot = telebot.TeleBot(BOT_TOKEN)

# --- Состояния ---
STATE_MENU = "MENU"
STATE_CHOOSE_SIZE = "CHOOSE_SIZE"
STATE_CHOOSE_TYPE = "CHOOSE_TYPE"
STATE_ASK_ADDRESS = "ASK_ADDRESS"
STATE_CONFIRM = "CONFIRM"

# Состояния по пользователям: chat_id -> state
user_state = {}
# Данные по заказу: chat_id -> {size, type, address}
user_order = {}


def get_menu_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🍕 Заказать пиццу"))
    kb.add(KeyboardButton("❓ Помощь"))
    return kb


def get_size_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("Маленькая"), KeyboardButton("Средняя"), KeyboardButton("Большая"))
    kb.add(KeyboardButton("Отмена"))
    return kb


def get_type_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("Пепперони"), KeyboardButton("4 сыра"))
    kb.add(KeyboardButton("Ветчина и грибы"))
    kb.row(KeyboardButton("Назад"), KeyboardButton("Отмена"))
    return kb


def get_confirm_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("✅ Подтвердить"))
    kb.add(KeyboardButton("✏ Изменить адрес"))
    kb.add(KeyboardButton("❌ Отмена"))
    return kb


def set_state(chat_id, state):
    user_state[chat_id] = state


def get_state(chat_id):
    return user_state.get(chat_id, STATE_MENU)


def get_order(chat_id):
    if chat_id not in user_order:
        user_order[chat_id] = {}
    return user_order[chat_id]


# --- /start ---
@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    set_state(chat_id, STATE_MENU)
    bot.send_message(
        chat_id,
        "Привет! Я бот-пиццерия.\nНажми кнопку, чтобы начать 👇",
        reply_markup=get_menu_keyboard(),
    )


# --- Основной обработчик текста (FSM) ---
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text
    state = get_state(chat_id)
    order = get_order(chat_id)

    # --- 1. Главное меню ---
    if state == STATE_MENU:
        if text == "🍕 Заказать пиццу":
            set_state(chat_id, STATE_CHOOSE_SIZE)
            bot.send_message(
                chat_id,
                "Выберите размер пиццы:",
                reply_markup=get_size_keyboard(),
            )
        elif text == "❓ Помощь":
            bot.send_message(
                chat_id,
                "Я помогаю оформить заказ пиццы.\n"
                "Нажми '🍕 Заказать пиццу' и следуй шагам.",
                reply_markup=get_menu_keyboard(),
            )
        else:
            bot.send_message(
                chat_id,
                "Я тебя не понял. Используй кнопки ниже 👇",
                reply_markup=get_menu_keyboard(),
            )

    # --- 2. Выбор размера ---
    elif state == STATE_CHOOSE_SIZE:
        if text in ["Маленькая", "Средняя", "Большая"]:
            order["size"] = text
            set_state(chat_id, STATE_CHOOSE_TYPE)
            bot.send_message(
                chat_id,
                "Отлично! Теперь выберите начинку:",
                reply_markup=get_type_keyboard(),
            )
        elif text == "Отмена":
            set_state(chat_id, STATE_MENU)
            bot.send_message(
                chat_id,
                "Заказ отменён. Возвращаемся в меню.",
                reply_markup=get_menu_keyboard(),
            )
        else:
            bot.send_message(
                chat_id,
                "Пожалуйста, выберите размер пиццы с помощью кнопок.",
                reply_markup=get_size_keyboard(),
            )

    # --- 3. Выбор начинки ---
    elif state == STATE_CHOOSE_TYPE:
        if text in ["Пепперони", "4 сыра", "Ветчина и грибы"]:
            order["type"] = text
            set_state(chat_id, STATE_ASK_ADDRESS)
            bot.send_message(
                chat_id,
                "Теперь отправьте адрес доставки (напишите текстом):",
            )
        elif text == "Назад":
            set_state(chat_id, STATE_CHOOSE_SIZE)
            bot.send_message(
                chat_id,
                "Вернулись к выбору размера.",
                reply_markup=get_size_keyboard(),
            )
        elif text == "Отмена":
            set_state(chat_id, STATE_MENU)
            bot.send_message(
                chat_id,
                "Заказ отменён. Возвращаемся в меню.",
                reply_markup=get_menu_keyboard(),
            )
        else:
            bot.send_message(
                chat_id,
                "Пожалуйста, выберите начинку с помощью кнопок.",
                reply_markup=get_type_keyboard(),
            )

    # --- 4. Ввод адреса ---
    elif state == STATE_ASK_ADDRESS:
        order["address"] = text
        set_state(chat_id, STATE_CONFIRM)

        size = order.get("size")
        pizza_type = order.get("type")
        address = order.get("address")

        bot.send_message(
            chat_id,
            f"Проверьте заказ:\n\n"
            f"Размер: {size}\n"
            f"Начинка: {pizza_type}\n"
            f"Адрес: {address}\n\n"
            f"Всё верно?",
            reply_markup=get_confirm_keyboard(),
        )

    # --- 5. Подтверждение заказа ---
    elif state == STATE_CONFIRM:
        if text == "✅ Подтвердить":
            size = order.get("size")
            pizza_type = order.get("type")
            address = order.get("address")

            bot.send_message(
                chat_id,
                f"Заказ принят! 🎉\n\n"
                f"Пицца: {size}, {pizza_type}\n"
                f"Адрес доставки: {address}\n"
                f"Курьер уже выехал 😉",
                reply_markup=get_menu_keyboard(),
            )
            set_state(chat_id, STATE_MENU)

        elif text == "✏ Изменить адрес":
            set_state(chat_id, STATE_ASK_ADDRESS)
            bot.send_message(
                chat_id,
                "Отправьте новый адрес доставки:",
            )

        elif text == "❌ Отмена":
            set_state(chat_id, STATE_MENU)
            bot.send_message(
                chat_id,
                "Заказ отменён.",
                reply_markup=get_menu_keyboard(),
            )
        else:
            bot.send_message(
                chat_id,
                "Пожалуйста, используйте кнопки ниже.",
                reply_markup=get_confirm_keyboard(),
            )


if __name__ == "__main__":
    print("Бот запущен! Ctrl+C для остановки.")
    bot.infinity_polling()
