import random
import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import json
import os

TOKEN = ""
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

DATA_FILE = "players.json"

# --- ДАННЫЕ ПОЛЬЗОВАТЕЛЕЙ ---
user_inventory = {}
user_bestiary = {}
user_money = {}
user_cooldown = {}
user_rods = {}
user_selected_bait = {}
user_baits = {}
user_reels = {}
user_location = {}

# --- НАЖИВКИ ---
baits = {
    "Червь": 10,
    "Опарыш": 15,
    "Кукуруза": 20,
    "Икра": 35,
    "Мотыль": 25
}

# --- УДОЧКИ ---
rods = {
    "Супер-сильная": {"power": 18, "durability": 8, "cooldown": 12, "max_fish_weight": 35, "fish_size_bonus": 0.3, "price": 400},
    "Сильная": {"power": 15, "durability": 10, "cooldown": 12, "max_fish_weight": 30, "fish_size_bonus": 0.2, "price": 250},
    "Сбалансированная": {"power": 10, "durability": 15, "cooldown": 10, "max_fish_weight": 20, "fish_size_bonus": 0.1, "price": 150},
    "Надежная": {"power": 6, "durability": 25, "cooldown": 12, "max_fish_weight": 15, "fish_size_bonus": 0, "price": 120},
    "Легкая": {"power": 8, "durability": 12, "cooldown": 8, "max_fish_weight": 18, "fish_size_bonus": 0.05, "price": 130},
    "Эпическая": {"power": 20, "durability": 20, "cooldown": 8, "max_fish_weight": 40, "fish_size_bonus": 0.4, "price": 600},
}


# --- КАТУШКИ ---
reels = {
    "Быстрая": {"speed": 5, "durability": 10, "value_bonus": 0, "price": 180},
    "Прочная": {"speed": 2, "durability": 25, "value_bonus": 0, "price": 150},
    "Сбалансированная": {"speed": 3, "durability": 15, "value_bonus": 5, "price": 170},
    "Эпическая": {"speed": 6, "durability": 40, "value_bonus": 20, "price": 400},
    "Легкая": {"speed": 7, "durability": 8, "value_bonus": 0, "price": 200},
    "Тяжелая": {"speed": 2, "durability": 35, "value_bonus": 10, "price": 250},
    "Мастерская": {"speed": 5, "durability": 20, "value_bonus": 15, "price": 350},
}


# --- ЛОКАЦИИ ---
locations = {
    "Река": ["Сельдь", "Окунь", "Сом", "Щука", "Карп", "Лещ", "Форель", "Сиг"],
    "Озеро": ["Карась", "Лосось", "Ставрида", "Скумбрия", "Тунец", "Палтус", "Сардина", "Луфарь"],
    "Море": ["Акула", "Барракуда", "Морской окунь", "Рыба-клоун", "Морской конек", "Рыба-меч", "Акула-молот", "Манта"],
    "Тропический остров": ["Скат", "Горбуша", "Пиранья", "Тунец", "Скумбрия", "Карп", "Лещ", "Форель"]
}

rarity_levels = ["Обычная", "Редкая", "Эпическая", "Легендарная"]
rarity_multiplier = {"Обычная": 1, "Редкая": 1.5, "Эпическая": 2, "Легендарная": 5}

# --- РЫБА ---
import random

# Редкости
rarity_levels = ["Обычная", "Редкая", "Эпическая", "Легендарная"]

# Свойства всех рыб
fish_properties = {
    "Сельдь": {"rarity": "Обычная", "min_weight": 0.3, "max_weight": 1.5},
    "Окунь": {"rarity": "Обычная", "min_weight": 1, "max_weight": 5},
    "Сом": {"rarity": "Редкая", "min_weight": 5, "max_weight": 20},
    "Щука": {"rarity": "Редкая", "min_weight": 4, "max_weight": 15},
    "Карп": {"rarity": "Обычная", "min_weight": 2, "max_weight": 8},
    "Лещ": {"rarity": "Обычная", "min_weight": 1.5, "max_weight": 6},
    "Форель": {"rarity": "Редкая", "min_weight": 2, "max_weight": 10},
    "Сиг": {"rarity": "Редкая", "min_weight": 1, "max_weight": 4},
    "Карась": {"rarity": "Обычная", "min_weight": 1, "max_weight": 3},
    "Лосось": {"rarity": "Редкая", "min_weight": 3, "max_weight": 12},
    "Ставрида": {"rarity": "Обычная", "min_weight": 0.5, "max_weight": 2},
    "Скумбрия": {"rarity": "Редкая", "min_weight": 1, "max_weight": 5},
    "Тунец": {"rarity": "Эпическая", "min_weight": 10, "max_weight": 25},
    "Палтус": {"rarity": "Редкая", "min_weight": 5, "max_weight": 15},
    "Сардина": {"rarity": "Обычная", "min_weight": 0.2, "max_weight": 0.8},
    "Луфарь": {"rarity": "Редкая", "min_weight": 2, "max_weight": 6},
    "Акула": {"rarity": "Легендарная", "min_weight": 50, "max_weight": 150},
    "Барракуда": {"rarity": "Эпическая", "min_weight": 8, "max_weight": 18},
    "Морской окунь": {"rarity": "Редкая", "min_weight": 3, "max_weight": 10},
    "Рыба-клоун": {"rarity": "Обычная", "min_weight": 0.3, "max_weight": 1},
    "Морской конек": {"rarity": "Эпическая", "min_weight": 1, "max_weight": 3},
    "Рыба-меч": {"rarity": "Легендарная", "min_weight": 15, "max_weight": 35},
    "Акула-молот": {"rarity": "Легендарная", "min_weight": 30, "max_weight": 70},
    "Манта": {"rarity": "Легендарная", "min_weight": 40, "max_weight": 100},
    "Скат": {"rarity": "Редкая", "min_weight": 5, "max_weight": 20},
    "Горбуша": {"rarity": "Обычная", "min_weight": 1, "max_weight": 4},
    "Пиранья": {"rarity": "Эпическая", "min_weight": 0.5, "max_weight": 2}
}

# Функция стоимости по редкости
def get_value_by_rarity(rarity):
    if rarity == "Обычная":
        return random.randint(5, 20)
    elif rarity == "Редкая":
        return random.randint(21, 50)
    elif rarity == "Эпическая":
        return random.randint(51, 100)
    elif rarity == "Легендарная":
        return random.randint(101, 200)
    else:
        return 10

# Генерация fish_data для каждой локации
fish_data = {}
for loc, fish_list in locations.items():
    fish_data[loc] = []
    for name in fish_list:
        prop = fish_properties.get(name, {"rarity": "Обычная", "min_weight": 1, "max_weight": 5})
        bait = random.choice(list(baits.keys()))
        fish = {
            "name": name,
            "min_weight": prop["min_weight"],
            "max_weight": prop["max_weight"],
            "base_value": get_value_by_rarity(prop["rarity"]),
            "rarity": prop["rarity"],
            "bait": bait
        }
        fish_data[loc].append(fish)

# --- Сохранение и загрузка данных ---
def save_data():
    data = {
        "user_inventory": user_inventory,
        "user_bestiary": user_bestiary,
        "user_money": user_money,
        "user_baits": user_baits,
        "user_rods": user_rods,
        "user_reels": user_reels,
        "user_selected_bait": user_selected_bait,
        "user_location": user_location
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            global user_inventory, user_bestiary, user_money, user_baits
            global user_rods, user_reels, user_selected_bait, user_location
            user_inventory = data.get("user_inventory", {})
            user_bestiary = data.get("user_bestiary", {})
            user_money = data.get("user_money", {})
            user_baits = data.get("user_baits", {})
            user_rods = data.get("user_rods", {})
            user_reels = data.get("user_reels", {})
            user_selected_bait = data.get("user_selected_bait", {})
            user_location = data.get("user_location", {})

# --- МЕНЮ ---
def main_menu():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎣 Рыбалка", callback_data="fish"),
                InlineKeyboardButton(text="🎒 Инвентарь", callback_data="inventory"),
                InlineKeyboardButton(text="💰 Продать", callback_data="sell")
            ],
            [
                InlineKeyboardButton(text="📖 Бестиарий", callback_data="bestiary"),
                InlineKeyboardButton(text="🛒 Удочки", callback_data="rods"),
                InlineKeyboardButton(text="🪝 Наживки", callback_data="baits")
            ],
            [
                InlineKeyboardButton(text="⚙ Сборка", callback_data="gear"),
                InlineKeyboardButton(text="Катушки", callback_data="reels"),
                InlineKeyboardButton(text="⬅ Главное меню", callback_data="back")
            ]
        ]
    )
    return kb

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def locations_menu():
    buttons = []
    loc_list = list(locations.keys())
    # делим на строки по 3 кнопки
    for i in range(0, len(loc_list), 3):
        row = [InlineKeyboardButton(text=loc, callback_data=f"loc_{loc}") for loc in loc_list[i:i+3]]
        buttons.append(row)
    # кнопка назад
    buttons.append([InlineKeyboardButton(text="⬅ Главное меню", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def rods_menu():
    buttons = []
    for name, data in rods.items():
        buttons.append([InlineKeyboardButton(
            text=f"{name} | Сила:{data['power']} Прочность:{data['durability']} Кулдаун:{data['cooldown']} Цена:{data['price']}",
            callback_data=f"buyrod_{name}"
        )])
    buttons.append([InlineKeyboardButton(text="⬅ Главное меню", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def reels_menu():
    buttons = []
    for name, data in reels.items():
        buttons.append([InlineKeyboardButton(
            text=f"{name} | Скорость:{data['speed']} Прочность:{data['durability']} Цена:{data['price']}",
            callback_data=f"buyreel_{name}"
        )])
    buttons.append([InlineKeyboardButton(text="⬅ Главное меню", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def baits_menu():
    buttons = []
    for name, price in baits.items():
        buttons.append([InlineKeyboardButton(
            text=f"{name} | Цена: {price*3} монет",  # увеличенная цена
            callback_data=f"buybait_{name}"
        )])
    buttons.append([InlineKeyboardButton(text="⬅ Главное меню", callback_data="back")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

def gear_menu(uid):
    rod_name = user_rods.get(uid, "Нет")
    reel_name = user_reels.get(uid, "Нет")
    rod = rods.get(rod_name, {"power":0, "durability":0, "cooldown":0})
    reel = reels.get(reel_name, {"speed":0, "durability":0})
    msg = (
        f"Сборка:\n"
        f"Удочка: {rod_name} (Сила:{rod['power']}, Прочность:{rod['durability']}, Кулдаун:{rod['cooldown']})\n"
        f"Катушка: {reel_name} (Скорость:{reel['speed']}, Прочность:{reel['durability']})"
    )
    return msg

# --- СЛУЧАЙНАЯ РЫБА ---
def get_random_fish(loc, user_bait=None, rod_name=None, reel_name=None):
    loc_fish = fish_data.get(loc, [])
    possible = [f for f in loc_fish if user_bait is None or f["bait"] == user_bait]
    if not possible:
        possible = loc_fish
    fish = random.choice(possible)
    weight = round(random.uniform(fish["min_weight"], fish["max_weight"]), 2)

    # бонусы от удочки и катушки
    rod = rods.get(rod_name, {})
    reel = reels.get(reel_name, {})
    size_bonus = rod.get("fish_size_bonus", 0)
    value_bonus = reel.get("value_bonus", 0)
    weight = round(weight * (1 + size_bonus), 2)
    value = int(fish["base_value"] * rarity_multiplier[fish["rarity"]] + value_bonus)
    
    f = fish.copy()
    f["weight"] = weight
    f["value"] = value
    return f

# --- ЛОВЛЯ ---
# --- ЛОВЛЯ ---
async def catch_fish(user_id, loc, bait=None):
    rod_name = user_rods.get(user_id)
    reel_name = user_reels.get(user_id)
    rod = rods.get(rod_name, {})  # если удочки нет, пустой словарь

    # минимальная сила удочки для каждой локации
    min_power_for_location = {
        "Река": 0,
        "Озеро": 0,
        "Море": 15,  # например, для моря нужна мощная удочка
        "Тропический остров": 10
    }

    required_power = min_power_for_location.get(loc, 0)
    if rod.get("power", 0) < required_power:
        return {
            "name": "Нужна более мощная удочка для входа сюда!",
            "weight": 0,
            "rarity": "-",
            "value": 0,
            "bait": "-"
        }

    fish = get_random_fish(loc, bait, rod_name, reel_name)

    # шанс слома удочки
    max_weight = rod.get("max_fish_weight", 12)
    if fish["weight"] > max_weight:
        if random.random() < 0.1:  # 10% шанс слома
            user_rods[user_id] = None

    # добавляем в инвентарь
    inv = user_inventory.get(user_id, {})
    key = fish["name"]
    if key not in inv:
        inv[key] = []
    inv[key].append({
        "weight": fish["weight"],
        "value": fish["value"],
        "rarity": fish["rarity"],
        "bait": fish["bait"]
    })
    user_inventory[user_id] = inv

    # обновляем бестиарий
    bestiary = user_bestiary.get(user_id, {})
    if key not in bestiary or fish["weight"] > bestiary[key]["max_weight"]:
        bestiary[key] = {"max_weight": fish["weight"], "bait": fish["bait"], "rarity": fish["rarity"]}
    user_bestiary[user_id] = bestiary

    save_data()
    return fish

# --- START ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    load_data()
    uid = message.from_user.id

    if uid not in user_money:
        user_money[uid] = 100

    # Инициализация приманок
    if uid not in user_baits:
        user_baits[uid] = {}
        for bait in baits:
            user_baits[uid][bait] = 0

    if uid not in user_selected_bait:
        user_selected_bait[uid] = None

    if uid not in user_rods:
        user_rods[uid] = None
    if uid not in user_reels:
        user_reels[uid] = None

    await message.answer("Привет! Добро пожаловать в Рыбалку!", reply_markup=main_menu())
# --- CALLBACK ---
@dp.callback_query()
async def cb_handler(callback: types.CallbackQuery):
    uid = callback.from_user.id
    data = callback.data
    await callback.answer()

    # --- Инициализация нового игрока с бесплатной нейтральной наживкой ---
    if uid not in user_baits:
        user_baits[uid] = {}

    # если нет нейтральной – выдаём
    if "Нейтральная" not in user_baits[uid]:
        user_baits[uid]["Нейтральная"] = 5

    # если нет выбранной наживки — выставляем нейтральную
    if uid not in user_selected_bait or user_selected_bait[uid] is None:
        user_selected_bait[uid] = "Нейтральная"

    save_data()

    # ----------- ЛОКАЦИИ / ЛОВЛЯ -----------
    if data == "fish":
        await callback.message.edit_text(
            "Выберите локацию:",
            reply_markup=locations_menu()
        )

    elif data.startswith("loc_"):
        loc = data[4:]
        user_location[uid] = loc
        save_data()

        now = datetime.now()

        rod_name = user_rods.get(uid)
        reel_name = user_reels.get(uid)

        rod = rods.get(rod_name, {"cooldown": 12})
        reel = reels.get(reel_name, {"speed": 0})

        effective_cd = max(1, rod["cooldown"] - reel["speed"])

        # --- Таймер ожидания перед ловлей ---
        if uid in user_cooldown and now < user_cooldown[uid]:
            remaining = int((user_cooldown[uid] - now).total_seconds())
            msg_text = f"Подождите {remaining} секунд перед новой ловлей."

            bar_length = 10
            timer_msg = await callback.message.answer(
                f"{msg_text}\n{'⬜' * bar_length} {remaining}s"
            )

            last_text = None

            for i in range(remaining, 0, -1):
                filled = int(bar_length * (1 - i / remaining))
                empty = bar_length - filled
                bar = "⬛" * filled + "⬜" * empty
                new_text = f"{msg_text}\n{bar} {i}s"

                if new_text != last_text:
                    try:
                        await timer_msg.edit_text(new_text)
                    except:
                        pass
                    last_text = new_text

                await asyncio.sleep(1)

            await timer_msg.edit_text(
                "Вы можете снова ловить рыбу!",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="🎣 Продолжить рыбалку", callback_data=f"loc_{loc}")],
                        [InlineKeyboardButton(text="🌍 Сменить локацию", callback_data="fish")],
                        [InlineKeyboardButton(text="⬅ Главное меню", callback_data="back")]
                    ]
                )
            )
            return

        # --- Списание наживки ---
        bait = user_selected_bait.get(uid)

        if user_baits[uid].get(bait, 0) <= 0:
            await callback.message.answer(f"У вас нет наживки {bait}. Выберите другую.")
            return
        else:
            user_baits[uid][bait] -= 1
            save_data()

        # --- Пойманная рыба ---
        fish = await catch_fish(uid, loc, bait)

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🎣 Продолжить рыбалку", callback_data=f"loc_{loc}")],
                [InlineKeyboardButton(text="🌍 Сменить локацию", callback_data="fish")],
                [InlineKeyboardButton(text="⬅ Главное меню", callback_data="back")]
            ]
        )

        await callback.message.edit_text(
            f"Вы поймали {fish['name']}!\nВес: {fish['weight']} кг\nРедкость: {fish['rarity']}\nЦена: {fish['value']} монет\nИспользована наживка: {fish['bait']}",
            reply_markup=kb
        )

        user_cooldown[uid] = now + timedelta(seconds=effective_cd)

    # ----------- ИНВЕНТАРЬ / НАЖИВКИ -----------
    elif data == "inventory":
        inv = user_inventory.get(uid, {})
        bait_inv = user_baits.get(uid, {})

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"{bait_name} ({count})", callback_data=f"select_bait_{bait_name}")]
                for bait_name, count in bait_inv.items() if count > 0
            ] + [[InlineKeyboardButton(text="⬅ Главное меню", callback_data="back")]]
        )

        if not inv:
            msg = "Ваш инвентарь пуст.\n"
        else:
            msg = "Ваш инвентарь:\n"
            for name, fishes_list in inv.items():
                for f in fishes_list:
                    msg += f"{name} ({f['rarity']}) - {f['weight']} кг, стоимость {f['value']} монет\n"

        await callback.message.edit_text(msg, reply_markup=kb)

    elif data.startswith("select_bait_"):
        bait_name = data[12:]
        user_selected_bait[uid] = bait_name
        save_data()
        await callback.message.answer(f"Вы выбрали наживку {bait_name} для следующей ловли.")

    # ----------- БЕСТИАРИЙ -----------
    elif data == "bestiary":
        bestiary = user_bestiary.get(uid, {})
        if not bestiary:
            await callback.message.edit_text("Бестиарий пуст.", reply_markup=main_menu())
            return

        msg = "Бестиарий:\n"
        for name, info in bestiary.items():
            msg += f"{name} ({info['rarity']}) – max вес: {info['max_weight']} кг, наживка: {info['bait']}\n"

        await callback.message.edit_text(msg, reply_markup=main_menu())

    # ----------- МЕНЮ ТАБОВ -----------
    elif data in ["rods", "reels", "baits", "gear", "back", "sell"]:
        if data == "rods":
            await callback.message.edit_text("Выберите удочку:", reply_markup=rods_menu())
        elif data == "reels":
            await callback.message.edit_text("Выберите катушку:", reply_markup=reels_menu())
        elif data == "baits":
            await callback.message.edit_text("Магазин наживок:", reply_markup=baits_menu())
        elif data == "gear":
            await callback.message.edit_text(gear_menu(uid), reply_markup=main_menu())
        elif data == "back":
            await callback.message.edit_text("Главное меню:", reply_markup=main_menu())
        elif data == "sell":
            inv = user_inventory.get(uid, {})
            total = sum(f['value'] for fishes in inv.values() for f in fishes)
            user_money[uid] = user_money.get(uid, 0) + total
            user_inventory[uid] = {}
            save_data()
            await callback.message.edit_text(
                f"Вы продали всю рыбу за {total} монет. У вас теперь {user_money[uid]} монет.",
                reply_markup=main_menu()
            )

    # ----------- ПОКУПКИ СНАРЯЖЕНИЯ -----------
    elif data.startswith("buyrod_"):
        rod_name = data[7:]
        rod = rods.get(rod_name)
        if not rod:
            await callback.message.edit_text("Удочка не найдена.", reply_markup=main_menu())
            return

        money = user_money.get(uid, 0)
        if money >= rod["price"]:
            user_money[uid] -= rod["price"]
            user_rods[uid] = rod_name
            save_data()
            await callback.message.edit_text(
                f"Вы купили удочку {rod_name}. Сила {rod['power']}, Прочность {rod['durability']}, Кулдаун {rod['cooldown']}. Остаток: {user_money[uid]}",
                reply_markup=main_menu()
            )
        else:
            await callback.message.edit_text("Недостаточно денег.", reply_markup=main_menu())

    elif data.startswith("buyreel_"):
        reel_name = data[8:]
        reel = reels.get(reel_name)
        money = user_money.get(uid, 0)

        if money >= reel["price"]:
            user_money[uid] -= reel["price"]
            user_reels[uid] = reel_name
            save_data()
            await callback.message.edit_text(
                f"Вы купили катушку {reel_name}. Скорость {reel['speed']}, Прочность {reel['durability']}. Остаток: {user_money[uid]}",
                reply_markup=main_menu()
            )
        else:
            await callback.message.edit_text("Недостаточно денег.", reply_markup=main_menu())

    # ----------- ПОКУПКА НАЖИВОК -----------
    elif data.startswith("buybait_"):
        bait_name = data[8:]
        price = baits.get(bait_name)

        if price is None:
            await callback.message.edit_text("Наживка не найдена.", reply_markup=main_menu())
            return

        money = user_money.get(uid, 0)

        if money >= price:
            user_money[uid] -= price
            user_baits[uid][bait_name] = user_baits[uid].get(bait_name, 0) + 1
            user_selected_bait[uid] = bait_name
            save_data()

            await callback.message.edit_text(
                f"Вы купили {bait_name}! Теперь у вас {user_baits[uid][bait_name]} шт.\nВыбрана как текущая наживка.\nОстаток: {user_money[uid]}",
                reply_markup=main_menu()
            )
        else:
            await callback.message.edit_text("Недостаточно денег.", reply_markup=main_menu())

# --- ЗАПУСК ---
if __name__ == "__main__":
    load_data()
    asyncio.run(dp.start_polling(bot))

