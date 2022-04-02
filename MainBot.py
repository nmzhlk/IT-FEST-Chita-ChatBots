import sqlite3

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import Updater, MessageHandler, Filters

TOKEN = ""  # Insert your own bot token here

TARGET_ID = 0

connection = sqlite3.connect("applications.db", check_same_thread=False)
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS applications ([id] INTEGER PRIMARY KEY, 
    [surname] TEXT, [name] TEXT, [patronymic] TEXT, [birthday] TEXT, [phone] TEXT, [email] TEXT, 
    [info] TEXT, [position] TEXT, [education] TEXT, [status] TEXT)"""
)

reply_keyboard = [
    [KeyboardButton("✅ Новая заявка")],
    [KeyboardButton("❓ Помощь")]
]
reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)


def start(update, context):
    update.message.reply_text("Здравствуйте! 👋")
    update.message.reply_text("Я — бот для подачи заявки на собеседование.")
    update.message.reply_text("Для подачи заявки, используйте кнопку Новая заявка ✅", reply_markup=reply_markup)


def helper(update, context):
    update.message.reply_text(
        "❗ Чтобы подать заявку, Вам нужно ввести следующие данные:\n\n"
        "1. ФИО\n"
        "2. Дата рождения\n"
        "3. Номер телефона\n"
        "4. Email\n"
        "5. Дополнительная информация\n"
        "6. Желаемая должность из предложенного списка\n"
        "7. Уровень образования")

    update.message.reply_text("Для подачи заявки, используйте кнопку Новая заявка ✅", reply_markup=reply_markup)


def apply(update, context):
    update.message.reply_text("✅ Давайте заполним новую заявку :)\n\n"
                              "❗ Для успешной работы бота, вводите номер пункта перед данными!\n"
                              "❓ Например: 1. Иванов Иван Иванович")

    update.message.reply_text("1. Введите своё ФИО")


def button(update, context):
    query = update.callback_query
    query.answer()

    show = "".join([char for char in query.data][3:])

    if query.data.startswith("6."):
        query.edit_message_text(text=f"6. Выбрана должность: {show} ✅")
        cursor.execute("UPDATE applications SET position = ? WHERE id = ?", (show, TARGET_ID))
        connection.commit()

    if query.data.startswith("7."):
        query.edit_message_text(text=f"7. Уровень образования: {show} ✅")
        cursor.execute("UPDATE applications SET education = ? WHERE id = ?", (show, TARGET_ID))
        connection.commit()


def interpreter(update, context):
    message = update.message.text
    global TARGET_ID

    if message == "✅ Новая заявка":
        apply(update, context)

    if message == "❓ Помощь":
        helper(update, context)

    if message.startswith("1."):
        message_split = message.split()
        if len(message_split) == 4:
            TARGET_ID += 1
            cursor.execute("INSERT OR REPLACE INTO applications (id) VALUES (?)", (TARGET_ID,))
            cursor.execute("UPDATE applications SET status = ? WHERE id = ?", ("Новая", TARGET_ID))
            cursor.execute("UPDATE applications SET surname = ? WHERE id = ?",
                           (message_split[1], TARGET_ID))
            cursor.execute("UPDATE applications SET name = ? WHERE id = ?",
                           (message_split[2], TARGET_ID))
            cursor.execute("UPDATE applications SET patronymic = ? WHERE id = ?",
                           (message_split[3], TARGET_ID))
            connection.commit()
            update.message.reply_text(
                f"✅ Сохранено: {message_split[1]} {message_split[2]} {message_split[3]}")
            update.message.reply_text("2. Введите свою дату рождения\n"
                                      "❗ Формат даты: ДД.ММ.ГГГГ")
        else:
            update.message.reply_text("❗ ФИО введено не полностью, повторите ввод")

    if message.startswith("2."):
        message_split = message.split(".")[1:]
        if len(message_split) == 3:
            db_date = message.split()[-1]
            cursor.execute("UPDATE applications SET birthday = ? WHERE id = ?",
                           (db_date, TARGET_ID))
            connection.commit()
            update.message.reply_text(f"✅ Сохранено: {db_date}")
            update.message.reply_text("3. Введите номер телефона\n"
                                      "❗ Допускаются только цифры")
        else:
            update.message.reply_text("❗ Дата рождения введена неверно, повторите ввод\n"
                                      "❗ Формат даты: ДД.ММ.ГГГГ")

    if message.startswith("3."):
        phone = [char for char in message][3:]
        if len(phone) == 11:
            db_date = "".join(phone)
            cursor.execute("UPDATE applications SET phone = ? WHERE id = ?",
                           (db_date, TARGET_ID))
            connection.commit()
            update.message.reply_text(f"✅ Сохранено: {db_date}")
            update.message.reply_text("4. Введите Email\n"
                                      "❗ Обязательно должен быть символ «@»")
        else:
            update.message.reply_text("❗ Номер телефона введён неверно, повторите ввод\n"
                                      "❗ Допускаются только цифры")

    if message.startswith("4."):
        email = [char for char in message][3:]
        if "@" in email:
            db_date = "".join(email)
            cursor.execute("UPDATE applications SET email = ? WHERE id = ?",
                           (db_date, TARGET_ID))
            connection.commit()
            update.message.reply_text(f"✅ Сохранено: {db_date}")
            update.message.reply_text("5. Введите дополнительную информацию о себе\n"
                                      "❓ Например: Ваши проекты или награды за успехи "
                                      "в профессиональной деятельности")
        else:
            update.message.reply_text("❗ Email введён неверно, повторите ввод\n"
                                      "❗ Обязательно должен быть символ «@»")

    if message.startswith("5."):
        db_date = "".join([char for char in message][3:])
        cursor.execute("UPDATE applications SET info = ? WHERE id = ?",
                       (db_date, TARGET_ID))
        connection.commit()
        update.message.reply_text(f"✅ Сохранено: {db_date}")

        position_keyboard = [
            [InlineKeyboardButton("Менеджер по продажам",
                                  callback_data="6. Менеджер по продажам")],
            [InlineKeyboardButton("Менеджер по рекламе",
                                  callback_data="6. Менеджер по рекламе")],
            [InlineKeyboardButton("Бухгалтер",
                                  callback_data="6. Бухгалтер")],
            [InlineKeyboardButton("Системный администратор",
                                  callback_data="6. Системный администратор")],
            [InlineKeyboardButton("Технический специалист",
                                  callback_data="6. Технический специалист")]
        ]
        position_markup = InlineKeyboardMarkup(position_keyboard)
        update.message.reply_text("6. Выберите должность", reply_markup=position_markup)

        education_keyboard = [
            [InlineKeyboardButton("Среднее общее",
                                  callback_data="7. Среднее общее")],
            [InlineKeyboardButton("Среднее специальное",
                                  callback_data="7. Среднее специальное")],
            [InlineKeyboardButton("Среднее профессиональное",
                                  callback_data="7. Среднее профессиональное")],
            [InlineKeyboardButton("Высшее",
                                  callback_data="7. Высшее")]
        ]
        education_markup = InlineKeyboardMarkup(education_keyboard)
        update.message.reply_text("7. Выберите уровень образования", reply_markup=education_markup)

        update.message.reply_text("❗ Когда закончите, используйте кнопку Завершить",
                                  reply_markup=ReplyKeyboardMarkup([["🏁 Завершить"]],
                                                                   one_time_keyboard=True,
                                                                   resize_keyboard=True))

    if message == "🏁 Завершить":
        finish(update, context)


def finish(update, context):
    data = cursor.execute("SELECT * FROM applications WHERE id = ?", (TARGET_ID,)).fetchall()
    update.message.reply_text(f"✅ Данные Вашей заявки:\n\n"
                              f"1. ФИО: {data[0][1]} {data[0][2]} {data[0][3]}\n"
                              f"2. Дата рождения: {data[0][4]}\n"
                              f"3. Номер телефона: {data[0][5]}\n"
                              f"4. Email: {data[0][6]}\n"
                              f"5. Дополнительная информация: {data[0][7]}\n"
                              f"6. Выбранная должность: {data[0][8]}\n"
                              f"7. Уровень образования: {data[0][9]}")
    connection.commit()
    update.message.reply_text("✅ Ваша заявка на собеседование сохранена!", reply_markup=reply_markup)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("finish", finish))
    dp.add_handler(MessageHandler(Filters.text, interpreter))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
