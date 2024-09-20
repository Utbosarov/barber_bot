from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contact_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отправить контакт", request_contact=True)]
], resize_keyboard=True)

main_button_barber = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Открыть новый слот")]
], resize_keyboard=True)

main_button_client = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Забронировать место"), KeyboardButton(text="Получить локацию")]
], resize_keyboard=True)