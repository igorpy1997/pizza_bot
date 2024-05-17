from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

pizzas = [
    {"name": "Маргарита", "url": "https://lh3.googleusercontent.com/-F7-f2RyixFJ_0-MIGehlz7lp08CkWuy7Y64qDx8zcSrAyHA_uWVnJx1XOVAHg_qoFD7fW34aWScKlOz7tlHx8LeBxDoB64vaZ6LCKKMAPPnr8-QTpPpQVVK-xGPWFZomSVkVZXW"},
    {"name": "Пеппероні", "url": "https://aegpizza.ru/wp-content/uploads/2021/03/%D0%BF%D0%B5%D0%BF%D0%BF%D0%B5%D1%80%D0%BE%D0%BD%D0%B8-scaled.jpg"},
    {"name": "Гавайська", "url": "https://cdn.lifehacker.ru/wp-content/uploads/2021/01/1_1611130322-e1710884562989-1280x640.jpg"},
    {"name": "Чотири сири", "url": "https://adriano.com.ua/wp-content/uploads/2022/08/%D0%9F%D1%96%D1%86%D0%B0-4-%D1%81%D0%B8%D1%80%D1%83-%D1%8F%D0%BA-%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D1%8C%D0%BD%D0%BE-%D0%B7%D1%80%D0%BE%D0%B1%D0%B8%D1%82%D0%B8-%D1%81%D0%BC%D0%B0%D1%87%D0%BD%D1%83-%D1%81%D1%82%D1%80%D0%B0%D0%B2%D1%83.png"},
    {"name": "Вегетаріанська", "url": "https://papitospizza.ru/wa-data/public/shop/products/44/00/44/images/307/307.970.jpg"},
    {"name": "З морепродуктами", "url": "https://img.taste.com.au/JDi_goQG/taste/2016/11/seafood-dill-pizza-5236-1.jpeg"},
    {"name": "З беконом", "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGMfPFQNX0fKm4c7dkis0nnkRRr44JJXYF58gDk3JwZQ&s"},
    {"name": "Барбекю", "url": "https://www.thecandidcooks.com/wp-content/uploads/2023/04/bbq-chicken-pizza-feature.jpg"},
    {"name": "Карбонара", "url": "https://pizzeriavesuviana.pl/wp-content/uploads/2021/05/18.-Pizza-Carbonara-crop-e1621716523633.jpg"},
    {"name": "Спайсі", "url": "https://www.thecandidcooks.com/wp-content/uploads/2022/08/spicy-sausage-pepper-pizza-feature.jpg"}
]


prices = {"Маргарита": 23, "Пеппероні":25, "Гавайська":30,  "Чотири сири":45,
          "Вегетаріанська":26, "З морепродуктами":30, "З беконом":32, "Барбекю":34,
          "Карбонара":35, "Спайсі":30}


def get_pizza_menu(page=0):
    items_per_page = 3
    pages = len(pizzas) // items_per_page + (len(pizzas) % items_per_page > 0)

    first_item_index = page * items_per_page
    last_item_index = min(first_item_index + items_per_page, len(pizzas))

    buttons = []
    for pizza in pizzas[first_item_index:last_item_index]:
        buttons.append([InlineKeyboardButton(text=pizza["name"], callback_data=f"pizza_{pizza['name']}")])

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="<< Назад", callback_data=f"page_{page - 1}"))
    if page < pages - 1:
        navigation_buttons.append(InlineKeyboardButton(text="Вперед >>", callback_data=f"page_{page + 1}"))

    buttons.append([InlineKeyboardButton(text="Завершити замовлення", callback_data="finish_order")])

    if navigation_buttons:
        buttons.append(navigation_buttons)

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
