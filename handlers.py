import sqlite3
from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import admin_ids
from database import save_order, get_all_orders, update_order_status, get_order_status
from keyboards import get_pizza_menu, pizzas, prices

router = Router()
user_data = {}

class OrderState(StatesGroup):
    awaiting_menu_interaction = State()
    awaiting_address = State()
    awaiting_name = State()

async def show_pizza_menu(message: types.Message, page=0):
    text_lines = []
    for pizza in pizzas[page * 3:(page + 1) * 3]:
        text_lines.append(f"{pizza['name']}\n[Картинка]({pizza['url']})")
    text = "\n\n".join(text_lines)
    await message.answer_photo(photo=pizzas[page * 3]['url'], caption=text, reply_markup=get_pizza_menu(page), parse_mode='Markdown')

@router.message(Command("order"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(OrderState.awaiting_menu_interaction)
    user_data[message.from_user.id] = {'order': []}
    await show_pizza_menu(message)

@router.callback_query(OrderState.awaiting_menu_interaction)
async def on_callback_query(callback_query: types.CallbackQuery, state: FSMContext):
    user_order = user_data[callback_query.from_user.id]['order']
    data = callback_query.data

    if data.startswith("pizza"):
        pizza_name = data.split("_")[1]
        pizza_price = prices[pizza_name]
        user_order.append([pizza_name, pizza_price])
        await callback_query.message.answer(f"Вы додали {pizza_name} в ваш замовлення.")
    elif data.startswith("page"):
        page = int(data.split("_")[1])
        await callback_query.message.delete()
        await show_pizza_menu(callback_query.message, page)
    elif data == "finish_order":
        order_details_list = []
        final_price = 0
        for order in user_order:
            order_details_list.append(order[0])
            final_price += order[1]
        order_details = ",".join(order_details_list)

        await callback_query.message.answer(f"Ваше замовлення: {order_details}.Вартість замовлення {final_price} грн. Дякуємо за покупку!")
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.message.delete()
        await state.set_state(OrderState.awaiting_address)
        await callback_query.message.answer("Введіть адресу достави:")
    await callback_query.answer()

@router.message(OrderState.awaiting_address)
async def process_address(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)
    await state.set_state(OrderState.awaiting_name)
    await message.answer("Введіть ім'я")

@router.message(OrderState.awaiting_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    data = await state.get_data()
    address = data.get("address")
    user_id = message.from_user.id
    order_details_list = [order[0] for order in user_data[user_id]['order']]
    final_price = sum(order[1] for order in user_data[user_id]['order'])
    save_order(user_id, ','.join(order_details_list), final_price, address, name)
    await message.answer(f"Ваше замовлення збережене. Адреса достави: {address}.")
    await state.clear()

@router.message(Command("showorders"))
async def show_orders(message: types.Message):
    if str(message.from_user.id) in admin_ids:
        orders = get_all_orders()
        if orders:
            for order in orders:
                order_id, user_id, order_details, total_price, address, user_name = order
                response = (f"Замовлення {order_id} від користувача {user_name}: {order_details}, на суму {total_price} грн. "
                            f"Адреса: {address}")
                buttons = [
                    InlineKeyboardButton(text="Взяти замовлення", callback_data=f"takeorder_{order_id}")
                ]
                keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
                await message.answer(response, reply_markup=keyboard)
        else:
            await message.answer("У базі даних немає замовлень.")
    else:
        await message.answer("У вас немає прав доступу до цієї команди.")

@router.callback_query()
async def handle_callback(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    action, order_id = data.split('_')
    order_id = int(order_id)

    if action == "takeorder":
        current_status = get_order_status(order_id)
        if current_status == "Замовлення оформлено":
            update_order_status(order_id, callback_query.from_user.id, "Взято кур'єром")
            await callback_query.message.edit_text(f"Замовлення №{order_id} взято до доставки.")
            buttons = [
                InlineKeyboardButton(text="✅ Завершити замовлення", callback_data=f"complete_{order_id}"),
                InlineKeyboardButton(text="❌ Скасувати замовлення", callback_data=f"cancel_{order_id}")
            ]
            keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
            await callback_query.message.answer("Виберіть опцію:", reply_markup=keyboard)
        else:
            await callback_query.message.answer(f"Замовлення №{order_id} вже взято до доставки іншим кур'єром.")
    elif action == "complete":
        update_order_status(order_id, callback_query.from_user.id, "Успішно завершено")
        await callback_query.message.edit_text(f"Замовлення №{order_id} успішно завершено.")
    elif action == "cancel":
        update_order_status(order_id, callback_query.from_user.id, "Відмінено")
        await callback_query.message.edit_text(f"Замовлення №{order_id} відмінено.")
    await callback_query.answer()
