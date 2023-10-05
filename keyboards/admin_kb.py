from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_load2 = KeyboardButton('Список тренингов')
button_load3 = KeyboardButton('Проверить вопросы дилеров')
button_load4 = KeyboardButton('Тренинг расписание')
button_load5 = KeyboardButton('Сделать пост')
button_load6 = KeyboardButton('Изменить SABA ID')

schedule_add = KeyboardButton('Добавить тренинг в расписание')
schedule_delete = KeyboardButton('Удалить тренинг из расписания')
main_menu_button = KeyboardButton('Главное меню')

add_training_description = KeyboardButton('Добавить описание тренинга')
remove_training_description = KeyboardButton('Удалить описание тренинга')

button_reply_question = KeyboardButton('Ответить')
button_send_reply = KeyboardButton('Отправить ответ')
button_change_status = KeyboardButton('Изменить статус')
button_back_admin = KeyboardButton('В главное меню')

admin_cancel_button = KeyboardButton('Отменить ввод')

admin_cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(admin_cancel_button)
processing_buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(button_reply_question, button_send_reply).add(
    button_change_status, button_back_admin)
button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load2, button_load4) \
    .add(button_load3, button_load5).add(button_load6)
kb_training_description = ReplyKeyboardMarkup(resize_keyboard=True).add(add_training_description,
                                                                        remove_training_description).add(
    main_menu_button)
schedule_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(schedule_add, schedule_delete).add(main_menu_button)

# кнопка, чтобы делать посты в канале с синей кнопкой
start_button = InlineKeyboardButton('start', url='https://t.me/Toyota_academy_bot')
ikb_start = InlineKeyboardMarkup()
ikb_start.add(start_button)