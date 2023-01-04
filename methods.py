from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

import globals
from database import Database
db = Database("db-evos.db")


def send_main_menu(context, chat_id, lang_id, message_id=None):
    buttons = [
        [KeyboardButton(text=globals.BTN_TEXT_ORDER[lang_id])],
        [KeyboardButton(text=globals.BTN_MY_ORDERS[lang_id])]

    ]

    if message_id:
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=globals.TEXT_MAIN_MENU[lang_id],
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons, resize_keyboard=True
            )
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=globals.TEXT_MAIN_MENU[lang_id],
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons, resize_keyboard=True
            )
        )


def send_category_buttons(categories, lang_id):   ##### 78 holatimz   bu biz faqat knopkalarni shakillantirib beradi

    buttons = []  ### 79 holatimz
    row = []
    for i in range(len(categories)):
        row.append(InlineKeyboardButton(text=categories[i][f'name_{globals.LANGUAGE_CODE[lang_id]}'],     #### 80 holatimz
                                        callback_data=f"category_{categories[i]['id']}"))

        if len(row) == 2 or (len(categories) % 2 == 1 and i == len(categories) - 1):
            buttons.append(row)
            row = []

    return buttons

def send_product_buttons(products, lang_id):     ##### 90 holatimz
    buttons = []  ### 91 holatimz
    row = []
    for i in range(len(products)):
        row.append(InlineKeyboardButton(text=products[i][f'name_{globals.LANGUAGE_CODE[lang_id]}'],  #### 92 holatimz
                                        callback_data=f"category_product_{products[i]['id']}"))  ##### 93 holatimz

        if len(row) == 2 or (len(products) % 2 == 1 and i == len(products) - 1):   #### 94 holatimz
            buttons.append(row)
            row = []

    return buttons


