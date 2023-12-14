from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

b1 = KeyboardButton('📚 Описание тренингов')
b2 = KeyboardButton('☎ Контакты')
b3 = KeyboardButton('📆 Расписание тренингов')
b4 = KeyboardButton('📨 Задать вопрос Академии')
b5 = KeyboardButton('🇯🇵 Лучшие практики дилеров Японии')
b6 = KeyboardButton('✏ Записаться на платный тренинг')
reg_but = KeyboardButton('/Регистрация')

tech_tr_button = KeyboardButton('⚙ Технические тренинги')
non_tech_tr_button = KeyboardButton('📈 Нетехнические тренинги')
ucar_tr_button = KeyboardButton('🚘Тренинги авто с пробегом')
detailed_description_button = KeyboardButton('📒 Скачать описание всех тренингов')
back_button = KeyboardButton('Назад')

button_cancel = KeyboardButton('Назад')

b7 = KeyboardButton('Отправить запрос в Академию')

tech_schedule_button = KeyboardButton('⚙ Технические направление')
non_tech_schedule_button = KeyboardButton('📈 Нетехнические направление')
ucar_schedule_button = KeyboardButton('🚘Направление авто с пробегом')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b1, b6).add(b2).insert(b3).row(b4, b5)

registration_kb = ReplyKeyboardMarkup(resize_keyboard=True)
registration_kb.add(reg_but)

kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_cancel.add(button_cancel)

trainings_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(tech_tr_button, non_tech_tr_button) \
    .add(ucar_tr_button,detailed_description_button).add(back_button)

# tech_tr_button1 = InlineKeyboardButton('/Технические_тренинги', callback_data='/Технические_тренинги')
# non_tech_tr_button1 = InlineKeyboardButton('/Нетехнические_тренинги', callback_data='/Нетехнические_тренинги')
# ucar_tr_button1 = InlineKeyboardButton('/Тренинги_авто_с_пробегом', callback_data='/Тренинги_авто_с_пробегом')

kb_ask = ReplyKeyboardMarkup(resize_keyboard=True).add(b7)
kb_ask_remove = ReplyKeyboardRemove()

# ikb = InlineKeyboardMarkup()
# ikb.add(tech_tr_button1, non_tech_tr_button1).add(ucar_tr_button1)

schedule_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(tech_schedule_button, non_tech_schedule_button).add(
    ucar_schedule_button, back_button)


