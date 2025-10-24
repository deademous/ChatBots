import json

import bot.telegram_client
import bot.database_client
from bot.handlers.handler import Handler, HandlerStatus

class DrinksHandler(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        if "callback_query" not in update:
            return False
        
        if state != "WAIT_FOR_DRINKS":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("drink_")

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        drink_mapping = {
            "drink_pepsi": "Pepsi",
            "drink_cola": "Coca-Cola",
            "drink_lipton": "Lipton",
            "drink_apple_juice": "Сок яблочный",
            "drink_still_water": "Негазированная вода",
            "drink_carbonate_water": "Газированная вода",
        }
        order_drink = drink_mapping.get(callback_data)
        order_json["order_drink"] = order_drink
        bot.database_client.update_user_data(telegram_id, order_json)
        bot.database_client.update_user_state(telegram_id, "WAIT_FOR_ORDER_APPROVE")
        bot.telegram_client.answerCallbackQuery(update["callback_query"]["id"],)
        bot.telegram_client.deleteMessage(
            chat_id = update["callback_query"]["message"]["chat"]["id"],
            message_id = update["callback_query"]["message"]["message_id"],
        )
        order_text = "Ваш заказ:\n"
        if "pizza_name" in order_json:
            order_text += f"🍕 Пицца: {order_json['pizza_name']}\n"
        if "pizza_size" in order_json:
            order_text += f"📏 Размер: {order_json['pizza_size']}\n"
        if "order_drink" in order_json:
            order_text += f"🥤 Напиток: {order_json['order_drink']}\n"
        order_text += "\nВерно ли составлен заказ?"

        bot.telegram_client.sendMessage(
            chat_id = update["callback_query"]["message"]["chat"]["id"],
            text = order_text,
            reply_markup = json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Начать заново", "callback_data": "check_not_approve"},
                            {"text": "Подтвердить", "callback_data": "check_approve"},
                        ]
                    ]
                }
            ),
        ) 
        return HandlerStatus.STOP