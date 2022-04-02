import sqlite3

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import Updater, MessageHandler, Filters

TOKEN_ADMIN = ""  # Insert your own bot token here

TARGET_ID = 0

connection = sqlite3.connect("applications.db", check_same_thread=False)
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS applications ([id] INTEGER PRIMARY KEY, 
    [surname] TEXT, [name] TEXT, [patronymic] TEXT, [birthday] TEXT, [phone] TEXT, [email] TEXT, 
    [info] TEXT, [position] TEXT, [education] TEXT, [status] TEXT)"""
)

inline_keyboard = [
    [InlineKeyboardButton("👌 Принять заявку",
                          callback_data="ACCEPT")],
    [InlineKeyboardButton("✅ Подтвердить заявку",
                          callback_data="CONFIRM")],
    [InlineKeyboardButton("❌ Отклонить заявку",
                          callback_data="DECLINE")]
]
inline_markup = InlineKeyboardMarkup(inline_keyboard)

reply_keyboard = [
    [KeyboardButton("✋ Все заявки")],
    [KeyboardButton("👌 Принятые заявки")],
    [KeyboardButton("✅ Подтверждённые заявки")],
    [KeyboardButton("❌ Отклонённые заявки")],
    [KeyboardButton("❓ Помощь")]
]
reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)


def start(update, context):
    update.message.reply_text("Здравствуйте!")
    update.message.reply_text("Я — администратор заявок.")
    update.message.reply_text("Нажимайте на кнопки, чтобы продолжить", reply_markup=reply_markup)


def helper(update, context):
    update.message.reply_text("Я умею принимать, подтверждать и отклонять заявки")
    update.message.reply_text("Я могу выводить все заявки и фильтровать их по статусам")


def every(update, context):
    data = cursor.execute("SELECT * FROM applications").fetchall()
    if data:
        update.message.reply_text("✅ Вывожу список ВСЕХ заявок")
        for piece in range(len(data)):
            update.message.reply_text(f"ID: {data[piece][0]}\n"
                                      f"Статус заявки: {data[piece][10]}\n"
                                      f"1. ФИО: {data[piece][1]} {data[piece][2]} {data[piece][3]}\n"
                                      f"2. Дата рождения: {data[piece][4]}\n"
                                      f"3. Номер телефона: {data[piece][5]}\n"
                                      f"4. Email: {data[piece][6]}\n"
                                      f"5. Дополнительная информация: {data[piece][7]}\n"
                                      f"6. Выбранная должность: {data[piece][8]}\n"
                                      f"7. Уровень образования: {data[piece][9]}", reply_markup=inline_markup)
    else:
        update.message.reply_text("❗ Нет заявок")


def accepted(update, context):
    data = cursor.execute("SELECT * FROM applications WHERE status = ?", ("Принята",)).fetchall()
    if data:
        update.message.reply_text("✅ Вывожу список ПРИНЯТЫХ заявок")
        for piece in range(len(data)):
            update.message.reply_text(f"ID: {data[piece][0]}\n"
                                      f"Статус заявки: {data[piece][10]}\n"
                                      f"1. ФИО: {data[piece][1]} {data[piece][2]} {data[piece][3]}\n"
                                      f"2. Дата рождения: {data[piece][4]}\n"
                                      f"3. Номер телефона: {data[piece][5]}\n"
                                      f"4. Email: {data[piece][6]}\n"
                                      f"5. Дополнительная информация: {data[piece][7]}\n"
                                      f"6. Выбранная должность: {data[piece][8]}\n"
                                      f"7. Уровень образования: {data[piece][9]}", reply_markup=inline_markup)
    else:
        update.message.reply_text("❗ Нет ПРИНЯТЫХ заявок")


def confirmed(update, context):
    data = cursor.execute("SELECT * FROM applications WHERE status = ?", ("Подтверждена",)).fetchall()
    if data:
        update.message.reply_text("✅ Вывожу список ПОДТВЕРЖДЁННЫХ заявок")
        for piece in range(len(data)):
            update.message.reply_text(f"ID: {data[piece][0]}\n"
                                      f"Статус заявки: {data[piece][10]}\n"
                                      f"1. ФИО: {data[piece][1]} {data[piece][2]} {data[piece][3]}\n"
                                      f"2. Дата рождения: {data[piece][4]}\n"
                                      f"3. Номер телефона: {data[piece][5]}\n"
                                      f"4. Email: {data[piece][6]}\n"
                                      f"5. Дополнительная информация: {data[piece][7]}\n"
                                      f"6. Выбранная должность: {data[piece][8]}\n"
                                      f"7. Уровень образования: {data[piece][9]}", reply_markup=inline_markup)
    else:
        update.message.reply_text("❗ Нет ПОДТВЕРЖДЁННЫХ заявок")


def declined(update, context):
    data = cursor.execute("SELECT * FROM applications WHERE status = ?", ("Отклонена",)).fetchall()
    if data:
        update.message.reply_text("✅ Вывожу список ОТКЛОНЁННЫХ заявок")
        for piece in range(len(data)):
            update.message.reply_text(f"ID: {data[piece][0]}\n"
                                      f"Статус заявки: {data[piece][10]}\n"
                                      f"1. ФИО: {data[piece][1]} {data[piece][2]} {data[piece][3]}\n"
                                      f"2. Дата рождения: {data[piece][4]}\n"
                                      f"3. Номер телефона: {data[piece][5]}\n"
                                      f"4. Email: {data[piece][6]}\n"
                                      f"5. Дополнительная информация: {data[piece][7]}\n"
                                      f"6. Выбранная должность: {data[piece][8]}\n"
                                      f"7. Уровень образования: {data[piece][9]}", reply_markup=inline_markup)
    else:
        update.message.reply_text("❗ Нет ОТКЛОНЁННЫХ заявок")


def button(update, context):
    query = update.callback_query
    query.answer()

    show = query["message"]["text"]
    id_list = show.split("\n")[0]
    ident = "".join(id_list)
    ident.split(":")
    target_id = ident[-1]

    if query.data.startswith("ACCEPT"):
        cursor.execute("UPDATE applications SET status = ? WHERE id = ?", ("Принята", target_id))
        connection.commit()

        data = cursor.execute("SELECT * FROM applications WHERE id = ?", (target_id,)).fetchall()
        query.edit_message_text(text=f"ID: {data[0][0]}\n"
                                     f"Статус заявки: {data[0][10]}\n"
                                     f"1. ФИО: {data[0][1]} {data[0][2]} {data[0][3]}\n"
                                     f"2. Дата рождения: {data[0][4]}\n"
                                     f"3. Номер телефона: {data[0][5]}\n"
                                     f"4. Email: {data[0][6]}\n"
                                     f"5. Дополнительная информация: {data[0][7]}\n"
                                     f"6. Выбранная должность: {data[0][8]}\n"
                                     f"7. Уровень образования: {data[0][9]}\n\n"
                                     f"✅ Заявка принята!")

    if query.data.startswith("CONFIRM"):
        cursor.execute("UPDATE applications SET status = ? WHERE id = ?", ("Подтверждена", target_id))
        connection.commit()

        data = cursor.execute("SELECT * FROM applications WHERE id = ?", (target_id,)).fetchall()
        query.edit_message_text(text=f"ID: {data[0][0]}\n"
                                     f"Статус заявки: {data[0][10]}\n"
                                     f"1. ФИО: {data[0][1]} {data[0][2]} {data[0][3]}\n"
                                     f"2. Дата рождения: {data[0][4]}\n"
                                     f"3. Номер телефона: {data[0][5]}\n"
                                     f"4. Email: {data[0][6]}\n"
                                     f"5. Дополнительная информация: {data[0][7]}\n"
                                     f"6. Выбранная должность: {data[0][8]}\n"
                                     f"7. Уровень образования: {data[0][9]}\n\n"
                                     f"✅ Заявка подтверждена!")

    if query.data.startswith("DECLINE"):
        cursor.execute("UPDATE applications SET status = ? WHERE id = ?", ("Отклонена", target_id))
        connection.commit()

        data = cursor.execute("SELECT * FROM applications WHERE id = ?", (target_id,)).fetchall()
        query.edit_message_text(text=f"ID: {data[0][0]}\n"
                                     f"Статус заявки: {data[0][10]}\n"
                                     f"1. ФИО: {data[0][1]} {data[0][2]} {data[0][3]}\n"
                                     f"2. Дата рождения: {data[0][4]}\n"
                                     f"3. Номер телефона: {data[0][5]}\n"
                                     f"4. Email: {data[0][6]}\n"
                                     f"5. Дополнительная информация: {data[0][7]}\n"
                                     f"6. Выбранная должность: {data[0][8]}\n"
                                     f"7. Уровень образования: {data[0][9]}\n\n"
                                     f"✅ Заявка отклонена!")


def handler(update, context):
    message = update.message.text
    if message == "✋ Все заявки":
        every(update, context)
    if message == "👌 Принятые заявки":
        accepted(update, context)
    if message == "✅ Подтверждённые заявки":
        confirmed(update, context)
    if message == "❌ Отклонённые заявки":
        declined(update, context)
    if message == "❓ Помощь":
        helper(update, context)


def main():
    updater = Updater(TOKEN_ADMIN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handler))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
