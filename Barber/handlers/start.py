from aiogram import filters, types, Router, Dispatcher
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from buttons.reply_buttons import contact_button
from aiogram.types import ReplyKeyboardRemove


db1 = Router()



class Registration(StatesGroup):
    full_name = State()
    phone_number = State()

import sqlite3


class Database:
    def init(self):
        self.db = sqlite3.connect("database.db")
        self.cursor = self.db.cursor()

    def create_table_users(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INT,
                full_name VARCHAR(221),
                phone_number VARCHAR(221)
            )
        """)
        self.db.commit()


    def create_table_time(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS time(
                start_time VARCHAR(221),
                end_time VARCHAR(221),
                is_booked BOOLEAN
            )
        """)


    def add_time(self, start_time, end_time):
        self.cursor.execute("""
            INSERT INTO time(start_time, end_time, is_booked)
            VALUES (?, ?, ?)
        """, (start_time, end_time, False))

        self.db.commit()

    def add_user(self, id, full_name, phone_number):
        self.cursor.execute("""
            INSERT INTO users(id, full_name, phone_number)
            VALUES (?, ?, ?)
        """, (id, full_name, phone_number))

    def check_user(self, id):
        result = self.cursor.execute("""
            SELECT * FROM users 
            WHERE id = ?
        """, (id, )).fetchone()

        return result

    def get_all_available_time(self):
        result = self.cursor.execute("""
            SELECT * FROM time
            WHRERE is_booked = 0
        """)
        return result.fetchall()

    def book_slot(self, start_time, end_time):
        self.cursor.execute("""
        UPDATE time
        SET is_booked = 1
        WHERE start_time = ? AND end_time = ?
        """, start_time, end_time)
        self.db.commit()


    def close_database(self):
        self.db.close()







@db1.message(filters.Command("start"))
async def start_function(message: types.Message,
                         state: FSMContext):
    user_check = db1.check_user(message.from_user.id)
    if user_check is None:

        await db1.create_table_users()
        await state.set_state(Registration.full_name)
        await message.answer(f"Botga xush kelibsiz, "
                             f"Familiyangizni kiriting")
    else:
        await message.answer("Qaytganingiz blan")


@db1.message(Registration.full_name)
async def full_name_function(message: types.Message,
                             state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    await state.set_state(Registration.phone_number)
    await message.answer("Yaxshi endi nomer telefoninggizni kiritng! ",reply_markup=contact_button)


@db1.message(Registration.phone_number)
async def phone_number_function(message: types.Message,
                                state: FSMContext):
    phone_number = message.contact.phone_number
    data = await state.get_data()
    db1.add_user(id=message.from_user.id, full_name=data['full_name'],
                phone_number=data['phone_number'])


    await state.update_data(phone_number=phone_number)
    await message.answer("Yaxshi biz nomeringizni va ismingizni saqlab oldik!",
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()