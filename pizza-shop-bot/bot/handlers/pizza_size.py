import json

import bot.telegram_client
import bot.database_client
from bot.handlers.handler import Handler, HandlerStatus

class PizzaSizeHandler(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        if "callback_query" not in update:
            return False
        
        if state != "WAIT_FOR_PIZZA_SIZE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("size_")

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        size_mapping = {
            "size_small": "Маленький(20cm)",
            "size_medium": "Срдений(25cm)",
            "size_large": "Большой(30cm)",
            "size_xl": "Огромный(40cm)",
        }
        pizza_size = size_mapping.get(callback_data)
        order_json["pizza_size"] = pizza_size
        bot.database_client.update_user_data(telegram_id, order_json)
        bot.database_client.update_user_state(telegram_id, "WAIT_FOR_DRINKS")
        bot.telegram_client.answerCallbackQuery(update["callback_query"]["id"],)
        bot.telegram_client.deleteMessage(
            chat_id = update["callback_query"]["message"]["chat"]["id"],
            message_id = update["callback_query"]["message"]["message_id"],
        ) 
        bot.telegram_client.sendMessage(
            chat_id = update["callback_query"]["message"]["chat"]["id"],
            text = "Выберите напиток:",
            reply_markup = json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Pepsi", "callback_data": "drink_pepsi"},
                            {"text": "Coca-cola", "callback_data": "drink_cola"},
                        ],
                        [
                            {"text": "Lipton", "callback_data": "drink_lipton"},
                            {"text": "Яблочный сок", "callback_data": "drink_apple_juice"},
                        ],
                        [
                            {"text": "Вода", "callback_data": "drink_still_water"},
                            {"text": "Газировка", "callback_data": "drink_carbonate_water"},
                        ]
                    ]
                }
            ),
        ) 
        return HandlerStatus.STOP