from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
from telegram import (
InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatAction, Message
)


import methods
from database import Database
import globals

db = Database("db-evos.db")

def check(update, context):
    user = update.message.from_user
    db_user = db.get_user_by_chat_id(user.id)
    if not db_user:
        db.create_user(user.id)
        buttons = [
            [KeyboardButton(text=globals.BTN_LANG_UZ), KeyboardButton(text=globals.BTN_LANG_RU), KeyboardButton(text=globals.BTN_LANG_EN)]
        ]
        update.message.reply_text(text=globals.WELCOME_TEXT)
        update.message.reply_text(
            text=globals.CHOOSE_LANG,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True
            )
        )
        context.user_data["state"] = globals.STATES["reg"]

    elif not db_user["lang_id"]:
        buttons = [
            [KeyboardButton(text=globals.BTN_LANG_UZ), KeyboardButton(text=globals.BTN_LANG_RU), KeyboardButton(text=globals.BTN_LANG_EN)]
        ]
        update.message.reply_text(
            text=globals.CHOOSE_LANG,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True
            )
        )
        context.user_data["state"] = globals.STATES["reg"]

    elif not db_user["first_name"]:
        update.message.reply_text(
            text=globals.TEXT_ENTER_FIRST_NAME[db_user["lang_id"]],
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data["state"] = globals.STATES["reg"]

    elif not db_user["last_name"]:
        update.message.reply_text(
            text=globals.TEXT_ENTER_LAST_NAME[db_user["lang_id"]],
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data["state"] = globals.STATES["reg"]

    elif not db_user["phone_number"]:
        buttons = [
            [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['lang_id']], request_contact=True)]

        ]
        update.message.reply_text(
            text=globals.TEXT_ENTER_CONTACT[db_user['lang_id']],
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True
            )
        )
        context.user_data["state"] = globals.STATES["reg"]

    else:
        context.user_data["state"] = globals.STATES["menu"]
        methods.send_main_menu(context,user.id, db_user['lang_id'])
        context.user_data['states'] = globals.STATES["menu"]

def check_data_decorator(func):
    def inner(update, context):
        user = update.message.from_user
        db_user = db.get_user_by_chat_id(user.id)
        state = context.user_data.get("state", 0)

        if state !=globals.STATES['reg']:

            if not db_user:
                db.create_user(user.id)
                buttons = [
                    [KeyboardButton(text=globals.BTN_LANG_UZ), KeyboardButton(text=globals.BTN_LANG_RU), KeyboardButton(text=globals.BTN_LANG_EN)]
                ]
                update.message.reply_text(text=globals.WELCOME_TEXT)
                update.message.reply_text(
                    text=globals.CHOOSE_LANG,
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=buttons,
                        resize_keyboard=True

                    )
                )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["lang_id"]:
                buttons = [
                    [KeyboardButton(text=globals.BTN_LANG_UZ), KeyboardButton(text=globals.BTN_LANG_RU), KeyboardButton(text=globals.BTN_LANG_EN)]

                ]
                update.message.reply_text(
                    text=globals.CHOOSE_LANG,
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=buttons,
                        resize_keyboard=True
                    )
                )
                context.user_data["states"] = globals.STATES["reg"]

            elif not db_user["first_name"]:
                update.message.reply_text(
                    text=globals.TEXT_ENTER_FIRST_NAME[db_user['lang_id']],
                    reply_markup=ReplyKeyboardRemove()
                )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["last_name"]:
                update.message.reply_text(
                    text=globals.TEXT_ENTER_LAST_NAME[db_user['lang_id']],
                    reply_markup=ReplyKeyboardRemove()
                )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["phone_number"]:
                buttons = [
                    [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['lang_id']],request_contact=True)]
                ]
                update.message.reply_text(
                    text=globals.TEXT_ENTER_CONTACT[db_user['lang_id']],
                    reply_markup=ReplyKeyboardMarkup(
                         keyboard=buttons,
                         resize_keyboard=True
                    )
                )
                context.user_data["state"] = globals.STATES["reg"]

            else:
                return func(update, context)
            return False
        else:
            return func(update, context)
    return inner


def start_handler(update, context):
    check(update, context)


@check_data_decorator
def message_handler(update, context):
    message = update.message.text
    user = update.message.from_user
    state = context.user_data.get("state", 0)
    db_user = db.get_user_by_chat_id(user.id)
    if state ==0:
        check(update, context)

    elif state == 1:
        db_user =db.get_user_by_chat_id(user.id)

        if not db_user["lang_id"]:

            if message ==globals.BTN_LANG_UZ:
                db.update_user_data(user.id, "lang_id", 1)
                check(update, context)

            elif message == globals.BTN_LANG_RU:
                db.update_user_data(user.id, "lang_id", 2)
                check(update, context)

            elif message == globals.BTN_LANG_EN:
                db.update_user_data(user.id, "lang_id", 3)
                check(update, context)


            else:
                update.message.reply_text(
                    text=globals.TEXT_LANG_WARNING
                )

        elif not db_user["first_name"]:
            db.update_user_data(user.id, "first_name", message)
            check(update, context)

        elif not db_user["last_name"]:
            db.update_user_data(user.id, "last_name", message)
            buttons = [
                [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['lang_id']], request_contact=True)]
            ]
            update.message.reply_text(
                text=globals.TEXT_ENTER_CONTACT[db_user['lang_id']],
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=buttons,
                    resize_keyboard=True
                )
            )
            check(update, context)

        elif not db_user["phone_number"]:
            db.update_user_data(user.id, "phone_number", message)
            check(update, context)

        else:
            check(update, context)

    elif state == 2:
        if message == globals.BTN_TEXT_ORDER[db_user['lang_id']]:
            categories = db.get_categories_by_parent()
            buttons = methods.send_category_buttons(categories=categories, lang_id=db_user["lang_id"])   ##### 83 holatimz

            if context.user_data.get("carts", {}):  #### 126 holatimz
                carts=context.user_data.get("carts")   #### 130 holatimz
                #text = ""  #### 127 holatimz text ni shakillantiramz
                text ="O'ylik haqi:\n\n"  ####  138 holatimz
                lang_code=globals.LANGUAGE_CODE[db_user['lang_id']]    #### 137 holatimz
                #for cart in carts.keys(): ### 131 holatimz
                total_price=0  #### 140 holatimz
                for cart, val in carts.items():     ### 135 holatimz
                    print(cart)
                    product=db.get_product_for_cart(int(cart))   #### 132 holatimz cart ni berib
                    text += f"{val} x {product[f'cat_name_{lang_code}']} {product[f'name_{lang_code}']}\n"      #### 136 holatimz
                    total_price += product['price'] * val #### 141 holatimz
                text += f"\n Jami: {total_price}"   #### 139 holatimz
                buttons.append([InlineKeyboardButton(text="O'ylik haqqi", callback_data="cart")])  #### 142 holatimz

            else:    #### 128 holatimz
                text = globals.TEXT_ORDER[db_user['lang_id']]
            update.message.reply_text(
                text=text,     #### 129 holatimz
                #text=globals.TEXT_ORDER[db_user['lang_id']],
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )

            ######  Buyurmtmasini korish knopkasini shakillantirish

        elif message == globals.BTN_MY_ORDERS[db_user['lang_id']]:    ##### 213 holatimz buyurmalarni shakillantish
            # orders = db.get_user_orders(db_user['id'])  #### 214  holatimz
            # lang_code=globals.LANGUAGE_CODE[db_user['lang_id']]     ##### 231 holatimz
            #
            # for order in orders:  ### 221 holatimz skilni sababi ishlatishimz uchun
            #     # text=""     #### 222 holatimz
            #     text = f"Buyurtma : # {order['id']}\n\n"  #### 226  holatimz
            #     total_price = 0  #### 227 holat
            #     products = db.get_order_products(order['id'])  #### 223 holatimz  id berib qo'ysak order ga tegishli productlar chiqadi
            #     for product in products:  ### 224 holatimz
            #         total_price += product['product_price'] * product['amount']  #### 228 holatimz
            #         text += f"{product['amount']} x {product[f'product_name_{lang_code}']} ({product[f'product_price']}) so'm \n"  #### 225 holatimz
            #
            #     # text += f"Umumiy narx :{order['total_price']}"    ##### 226 holatimz
            #     text += f"\n Umumiy narx :{total_price}"  ##### 229 holatimz
            #     update.message.reply_text(text=text)  #### 230 holatimz          !!!!! tugadi hush kelibsz !!!!!

            orders=db.get_user_orders(db_user['id'])     #### 214  holatimz
            lang_code=globals.LANGUAGE_CODE[db_user['lang_id']]     ##### 231 holatimz
            for order in orders:    ### 221 holatimz skilni sababi ishlatishimz uchun
                #text=""     #### 222 holatimz
                text=f"O'ylik : # {order['id']}\n\n"     #### 226  holatimz
                total_price=0   #### 227 holat
                products=db.get_order_products(order['id'])    #### 223 holatimz  id berib qo'ysak order ga tegishli productlar chiqadi
                for product in products:      ### 224 holatimz
                    total_price += product['product_price'] * product['amount']   #### 228 holatimz
                    text += f"{product['amount']} x {product[f'product_name_{lang_code}']} = ({product['product_price']}) so'm \n"    #### 225 holatimz

                #text += f"Umumiy narx :{order['total_price']}"    ##### 226 holatimz
                text += f"\n Umumiy narx :{total_price}"  ##### 229 holatimz
                update.message.reply_text(text=text)     #### 230 holatimz          !!!!! tugadi hush kelibsz !!!!!


        # elif message == globals.BTN_COMMENTS[db_user['lang_id']]:
        #     suggestions=db.get_suggestion(user['id'])
        #     lang_code = globals.LANGUAGE_CODE[db_user['lang_id']]


    else:
        update.message.reply_text("Hello")


def inline_handler(update, context):

    query = update.callback_query
    data_sp = str(query.data).split("_")
    db_user = db.get_user_by_chat_id(query.message.chat_id)

    if data_sp[0]=="category":
        if data_sp[1]=="product":  #### 95 holat
            if data_sp[2]=="back":   #### 109 holat
                query.message.delete()    ##### 112 holatimz
                products = db.get_products_by_category(category_id=int(data_sp[3]))  ##### 110 holatimz
                buttons = methods.send_product_buttons(products=products, lang_id=db_user["lang_id"])  #### 111  holatimz

                clicked_btn = db.get_category_parent(int(data_sp[3]))  ##### 114 holatimz   category ga qaytishimz
                if clicked_btn and clicked_btn['parent_id']:  ##### 115 holatimz
                    buttons.append([InlineKeyboardButton(  #### 116  holatimz
                        text="Back", callback_data=f"category_back_{clicked_btn['parent_id']}"  ###### 117 holatimz
                    )])

                else:  #### 118 holatimz
                    buttons.append([InlineKeyboardButton(  ##### 119 holatimz
                        text="back", callback_data=f"category_back"  #####  120 holatimz    category ga qaytishimz
                    )])
                query.message.reply_text(     ##### 113 holatimz
                    text=globals.TEXT_ORDER[db_user['lang_id']],
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
                )

            else:  ##### 110 holat
                if len(data_sp) == 4:  #### 121 holatimz
                    query.message.delete()    ####### 181 holatimz
                    carts=context.user_data.get("carts", {})    #### 123 holatimz
                    carts[f"{data_sp[2]}"] = carts.get(f"{data_sp[2]}", 0)+ int(data_sp[3])  ### 124 holatimz  cart qoshamz bu bilan
                    context.user_data["carts"] = carts  ### 125 holat
#############################################
                    categories = db.get_categories_by_parent()     ##### 168 holatimz
                    buttons = methods.send_category_buttons(categories=categories, lang_id=db_user["lang_id"])  ##### 169  holatimz


                    text = "💵 Oylik haqqi :\n\n"  ####  170  holatimz
                    lang_code = globals.LANGUAGE_CODE[db_user['lang_id']]  #### 171  holatimz
                    # for cart in carts.keys(): ### 131 holatimz
                    total_price = 0  #### 172 holatimz
                    for cart, val in carts.items():  ### 173 holatimz
                        print(cart)
                        product = db.get_product_for_cart(int(cart))  #### 174  holatimz cart ni berib
                        text += f"{val} x {product[f'cat_name_{lang_code}']} {product[f'name_{lang_code}']}\n"  #### 175  holatimz
                        total_price += product['price'] * val  #### 176  holatimz
                    text += f"\n Jami: {total_price}"  #### 177  holatimz
                    buttons.append([InlineKeyboardButton(text=" 💵 Ish haqqi", callback_data="cart")])  #### 178  holatimz

                    # else:  #### 128 holatimz
                    #     text = globals.TEXT_ORDER[db_user['lang_id']]
                    query.message.reply_text(
                        text=text,  #### 179 holatimz
                        # text=globals.TEXT_ORDER[db_user['lang_id']],
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)    #### 180 holatimz
                    )


              ################################################3
                else:    #### 122 holatimz
                    product=db.get_product_by_id(int(data_sp[2]))  #### 100 holat
                    query.message.delete()  ### 101 holat

                    caption=f"{globals.TEXT_PRODUCT_PRICE[db_user['lang_id']]}" + str(product["price"]) + \
                        f"\n {globals.TEXT_PRODUCT_DESC[db_user['lang_id']]}" + \
                        product[f"description_{globals.LANGUAGE_CODE[db_user['lang_id']]}"]   ###### 106 holatimz

                    buttons=[      #### 107 holatimz
                        [
                            InlineKeyboardButton(text="1", callback_data=f"category_product_{data_sp[2]}_{1}"),
                            InlineKeyboardButton(text="2", callback_data=f"category_product_{data_sp[2]}_{2}"),
                            InlineKeyboardButton(text="3", callback_data=f"category_product_{data_sp[2]}_{3}"),

                        ],
                        [
                            InlineKeyboardButton(text="4",callback_data=f"category_product_{data_sp[2]}_{4}"),
                            InlineKeyboardButton(text="5", callback_data=f"category_product_{data_sp[2]}_{5}"),
                            InlineKeyboardButton(text="6", callback_data=f"category_product_{data_sp[2]}_{6}"),

                        ],
                        [
                            InlineKeyboardButton(text="7",callback_data=f"category_product_{data_sp[2]}_{7}"),
                            InlineKeyboardButton(text="8", callback_data=f"category_product_{data_sp[2]}_{8}"),
                            InlineKeyboardButton(text="9", callback_data=f"category_product_{data_sp[2]}_{9}"),

                        ],
                        [
                            InlineKeyboardButton(text="10", callback_data=f"category_product_{data_sp[2]}_{10}"),
                            InlineKeyboardButton(text="11", callback_data=f"category_product_{data_sp[2]}_{11}"),
                            InlineKeyboardButton(text="12", callback_data=f"category_product_{data_sp[2]}_{12}"),

                        ],
                        [
                            InlineKeyboardButton(text="13", callback_data=f"category_product_{data_sp[2]}_{13}"),
                            InlineKeyboardButton(text="14", callback_data=f"category_product_{data_sp[2]}_{14}"),
                            InlineKeyboardButton(text="15", callback_data=f"category_product_{data_sp[2]}_{15}"),

                        ],
                        [
                            InlineKeyboardButton(text="16", callback_data=f"category_product_{data_sp[2]}_{16}"),
                            InlineKeyboardButton(text="17", callback_data=f"category_product_{data_sp[2]}_{17}"),
                            InlineKeyboardButton(text="18", callback_data=f"category_product_{data_sp[2]}_{18}"),

                        ],
                        [
                            InlineKeyboardButton(text="19", callback_data=f"category_product_{data_sp[2]}_{19}"),
                            InlineKeyboardButton(text="20", callback_data=f"category_product_{data_sp[2]}_{20}"),
                            InlineKeyboardButton(text="21", callback_data=f"category_product_{data_sp[2]}_{21}"),

                        ],
                        [
                            InlineKeyboardButton(text="22", callback_data=f"category_product_{data_sp[2]}_{22}"),
                            InlineKeyboardButton(text="23", callback_data=f"category_product_{data_sp[2]}_{23}"),
                            InlineKeyboardButton(text="24", callback_data=f"category_product_{data_sp[2]}_{24}"),

                        ],
                        [
                            InlineKeyboardButton(text="25", callback_data=f"category_product_{data_sp[2]}_{25}"),
                            InlineKeyboardButton(text="26", callback_data=f"category_product_{data_sp[2]}_{26}"),
                            InlineKeyboardButton(text="27", callback_data=f"category_product_{data_sp[2]}_{27}"),

                        ],
                        [
                            InlineKeyboardButton(text="28", callback_data=f"category_product_{data_sp[2]}_{28}"),
                            InlineKeyboardButton(text="29", callback_data=f"category_product_{data_sp[2]}_{29}"),
                            InlineKeyboardButton(text="30", callback_data=f"category_product_{data_sp[2]}_{30}"),
                            InlineKeyboardButton(text="31", callback_data=f"category_product_{data_sp[2]}_{31}"),

                        ],
                        [
                            InlineKeyboardButton(text="Back", callback_data=f"category_product_back_{product['category_id']}")   #### 108 holat ortga qaytish
                        ]
                    ]

                    query.message.reply_photo(       #### 102 holat
                        photo=open(product['image'], "rb"),     #### 103 holat
                        caption=caption,  #### 104 holat
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
                    )

        elif data_sp[1]=="back": ##### 49 holatimz
            if len(data_sp)==3:   ### 50 holatimz

                print("has Parent")    #### 60 holatimz tekshirib koryapmz parent bor yoki yoq
                parent_id = int(data_sp[2])   #### 53 holatimz

            else:    #### 51 holatimz
                print("No parent")  #### 61 holatimz
                parent_id = None      #### 54 holatimz
            categories = db.get_categories_by_parent(parent_id=parent_id)     ##### 52 holatimz    tepadagi asossiy qismini qaytaramz    ,,,, 55 holatimz
            buttons = methods.send_category_buttons(categories=categories, lang_id=db_user["lang_id"])  ##### 81 holatimz method dan funsiyani chaqirib olamz


            if parent_id:   #### 56 holatimz       #######
                clicked_btn = db.get_category_parent(parent_id)     ##### 72 holatimz

                if clicked_btn and clicked_btn['parent_id']:  #### 73 holatimz   bu holatimz orqaga qaytishga agar parent bolsa bitta oldinga qaytish kerak
                    buttons.append([InlineKeyboardButton(
                        text="Back", callback_data=f"category_back_{clicked_btn['parent_id']}"  ###### 74  holatimz
                    )])

                else:  #### 75 holatimz
                    buttons.append([InlineKeyboardButton(  ## 76 holatimz
                        text="back", callback_data=f"category_back"  #####   77 holatimz
                    )])
                # buttons.append([InlineKeyboardButton(  #### 57 holatimz
                #     text="Back", callback_data="category_back"
                # )])
            query.message.edit_reply_markup(  ##### 58 holatimz
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=buttons
                )
            )

        else:    ###### 59 holatimz

            categories=db.get_categories_by_parent(parent_id=int(data_sp[1]))
            if categories:   ##### 84 holatimz
                buttons = methods.send_category_buttons(categories=categories, lang_id=db_user["lang_id"])   #### 82 holatimz,,,

            else:        ####### 85 holatimz
                products=db.get_products_by_category(category_id=int(data_sp[1]))   ##### 87 holatimz
                buttons = methods.send_product_buttons(products=products, lang_id=db_user["lang_id"])  #### 86  holatimz


            clicked_btn = db.get_category_parent(int(data_sp[1]))     ##### 64 holatimz

            if clicked_btn and clicked_btn['parent_id']:   ##### 65 holatimz ,,,,, 71 holatimz  clicked_btn['parent_id']
                buttons.append([InlineKeyboardButton(   #### 66  holatimz
                    text="Back", callback_data=f"category_back_{clicked_btn['parent_id']}"      ###### 67 holatimz
                )])

            else:   #### 68 holatimz
                buttons.append([InlineKeyboardButton( ##### 69 holatimz
                    text="back", callback_data=f"category_back"      ##### 70 holatimz
                )])

            query.message.edit_reply_markup(    ##### 48 holatimz
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=buttons
                )
            )

    elif data_sp[0]=="cart":    ####143 holatimz
        #if data_sp[1]=="clear":    #### 147 holatimz     lekin uzunligi raqam bolishi kerak
        if len(data_sp)==2 and  data_sp[1]=="clear":   #### 147 holatimz
            context.user_data.pop("carts")  ##### 150 holatimz savatchani boshatish uchun
            categories = db.get_categories_by_parent()   ##### 151 holatimz
            buttons = methods.send_category_buttons(categories=categories,lang_id=db_user["lang_id"])  ##### 152  holatimz
            text = globals.TEXT_ORDER[db_user['lang_id']]   #### 155 holatimz
            query.message.reply_text(    ##### 153 holatimz
                text=text,  #### 154  holatimz
                # text=globals.TEXT_ORDER[db_user['lang_id']],
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )
        #elif data_sp[1] == "back"     #### 148 holatimz
        elif len(data_sp)==2 and  data_sp[1]=="back":   #### 148 holatimz
            categories = db.get_categories_by_parent()     ########  156  tepadagi funksiyani qaytaramz
            buttons = methods.send_category_buttons(categories=categories,lang_id=db_user["lang_id"])    #####   157  holatimz

            if context.user_data.get("carts", {}):  ####     158   holatimz
                carts = context.user_data.get("carts")  ####   159    holatimz
                # text = ""  ####     holatimz text ni shakillantiramz
                text = " 💵 Umumiy o'ylik:\n\n"  ####    160    holatimz
                lang_code = globals.LANGUAGE_CODE[db_user['lang_id']]  ####   161    holatimz
                # for cart in carts.keys(): ###  162   holatimz
                total_price = 0  ####   163  holatimz
                for cart, val in carts.items():  ###  164  holatimz
                    product = db.get_product_for_cart(int(cart))  ####     holatimz cart ni berib
                    text += f"{val} x {product[f'cat_name_{lang_code}']} {product[f'name_{lang_code}']}\n"  ####    holatimz
                    total_price += product['price'] * val  ####   holatimz
                text += f"\n Jami: {total_price}"        #### 165 holat
                buttons.append([InlineKeyboardButton(text="💵 Ish haqi", callback_data="cart")])  ### 166 holatimz

            else:  ### 167 holatimz    oxiri
                text = globals.TEXT_ORDER[db_user['lang_id']]
            #update.message.reply_text()
            query.message.edit_text(   #### 182 holatimz
                #text=text,  ####   holatimz
                text=text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )

        else:     #### 149 holatimz
            buttons=[         ##### 145 holatimz
                [
                    InlineKeyboardButton(text="O'ylikni ko'rish", callback_data="order"),
                    InlineKeyboardButton(text="🗑 O'ylikni o'chirish", callback_data="cart_clear")
                ],
                [InlineKeyboardButton(text="⬅️Orqaga", callback_data="cart_back")],
            ]
            query.message.edit_reply_markup(       #### 144 holatimz
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=buttons     ##### 146 holatimz

                )
            )

    elif data_sp[0]=="order":     ###### 183 holatimz

        if len(data_sp)>1 and data_sp[1] == "payment":   #### 197 holatimz
            context.user_data['payment_type'] = int(data_sp[2])    ##### 201 holatimz
            query.message.delete()     ##### 202 holatimz
            query.message.reply_text(  ##### 198 holatimz
                text="Locatsiyani jo'nating!",
                reply_markup=ReplyKeyboardMarkup([[KeyboardButton(text="Send location", request_location=True)]],resize_keyboard=True))  ##### 199 holatimz
        else:   #### 200 holatimz
            query.message.edit_reply_markup(       #### 196 holatimz
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(text="Naqd pul", callback_data="order_payment_1"),
                        InlineKeyboardButton(text="Karta", callback_data="order_payment_2")
                    ]]
                )
            )

        # query.message.reply_text(         ##### 193 holatimz
        #     text="Locatsiyani jo'nating!",
        #     reply_markup=ReplyKeyboardMarkup([[KeyboardButton(text="Send location", request_location=True)]], resize_keyboard=True)    ##### 194 holatimz


        # print(context.user_data.get("carts", {}))    ##### 189 holatimz sinash bu id sini bilish uchun
        # db.create_order(db_user['id'], [])    ####  188 holatimz
        # db.create_order(db_user['id'], context.user_data.get("carts", {}))     #### 190 holatimz

def location_handler(update, context):    #### 195 holatimz
    db_user = db.get_user_by_chat_id(update.message.from_user.id)     #### 204 holatimz
    #print(update.message.location)
    location=update.message.location    ##### 205 holatimz
    payment_type=context.user_data.get("payment_type", None)     ###### 207 holatimz
    db.create_order(db_user['id'], context.user_data.get("carts", {}), payment_type, location)    ##### 203 holatimz  ,,, 208 holatimz

    context.user_data['payment_type'] = None    ##### 209 holatimz   qaytgan malumot bosh bolsa
    context.user_data['carts'] = {}       ##### 210 holatimz
    #update.message.delete()     ####
    update.message.reply_text(      ##### 212 holatimz
        text="Sizning murojatingiz  qabul qilindi! ishlarizga omad "
    )
    methods.send_main_menu(context, update.message.from_user.id, db_user['lang_id'], )   #### 211 holatimz   bu bosh menu ga qaytarib beradi

def main():
    updater = Updater("5227671163:AAFgosBe6bMKbJs75eW4q77I5umBKIHn-5s")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(MessageHandler(Filters.location, location_handler))
    dispatcher.add_handler(CallbackQueryHandler(inline_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

