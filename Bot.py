import telebot

TOKEN = "8483563145:AAHJhXPbCe5wL2UxrFIeyI-bE3lw7GrL-Lo"
PIN_CODE = "7925"
mon_balance = 1000
oper_list = []

bot = telebot.TeleBot(TOKEN)

user_state = {}

kb = telebot.types.ReplyKeyboardMarkup()
kb.add("Проверить баланс", "Пополнить счёт", "Снять деньги со счёта", "История операций")
kb2 = telebot.types.ReplyKeyboardMarkup()
kb2.add("Проверить баланс", "Пополнить счёт", "Снять деньги со счёта", "История операций", "Назад")


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_state[chat_id] = "await_pin"
    bot.send_message(chat_id, "Введите свой пин-код")


@bot.message_handler(func=lambda message: True)
def main_handler(message):
    global mon_balance, kb
    chat_id = message.chat.id
    text = message.text

    # /start
    if chat_id not in user_state:
        bot.send_message(chat_id, "Перед началом работы введите /start")
        return

    # Проверка пина
    if user_state[chat_id] == "await_pin":
        if text != PIN_CODE:
            bot.send_message(chat_id, "Пин неверен, попробуйте ещё раз.")
        else:
            user_state[chat_id] = "logged_in"
            bot.send_message(chat_id, "Добро пожаловать!", reply_markup=kb)
        return

    # Меню
    if user_state[chat_id] == "logged_in":
        if text == "Проверить баланс":
            bot.send_message(chat_id, f"Ваш баланс: {mon_balance}")

        elif text == "Пополнить счёт":
            user_state[chat_id] = "await_topup"
            bot.send_message(chat_id, "Введите сумму пополнения:", reply_markup=kb2)

        elif text == "Снять деньги со счёта":
            user_state[chat_id] = "await_withdrawal"
            bot.send_message(chat_id, "Какую сумму желаете снять? "
                                           "Чтобы выйти в меню напишите 'Назад'", reply_markup=kb2)


        elif text == "История операций":
            bot.send_message(chat_id, f"История операций:\n{oper_list[:]} ", reply_markup=kb)

        else:
            bot.send_message(chat_id, "Неизвестная команда.")

        return

    # Обработка суммы пополнения
    if user_state[chat_id] == "await_topup":
        if text.isdigit() and int(text) > 0:
            mon_balance += int(text)
            oper_list.append(f"Пополение счёта на: {text}, Баланс после операции: {mon_balance}")
            bot.send_message(chat_id, f"Баланс пополнен!\nНовый баланс: {mon_balance}", reply_markup=kb)
            user_state[chat_id] = "logged_in"
        else:
            bot.send_message(chat_id, "Введите число, число должно быть не отрицательным и целым.")

    # Обработка снятия денег
    if user_state[chat_id] == "await_withdrawal":
        if text == "Назад":
            bot.send_message(chat_id, "Возвращаемся в меню", reply_markup=kb)
            user_state[chat_id] = "logged_in"
        elif text.isdigit() and int(text) > 0:
            if mon_balance >= int(text):
                mon_balance -= int(text)
                oper_list.append(f"Снятие денег со счёта на: {text}, Баланс после операции: {mon_balance}")
                bot.send_message(chat_id, f"Операция проведена.\nНовый баланс: {mon_balance}", reply_markup=kb)
                user_state[chat_id] = "logged_in"
            else:
                bot.send_message(chat_id, "Недостаточно средств. Введите сумму заново")
        else:
            bot.send_message(chat_id, "Введите число. Число должно быть не отрицательным и целым")

bot.polling()



