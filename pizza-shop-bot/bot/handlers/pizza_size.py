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
            "size_small": "Small(25cm)",
            "size_medium": "Medium(30cm)",
            "size_large": "Large(35cm)",
            "size_xl": "xl(40cm)",
        }
        pizza_size = size_mapping.get(callback_data)
        order_json["pizza_size"] = pizza_size
        print(order_json)
        bot.database_client.update_user_data(telegram_id, order_json)
        bot.database_client.update_user_state(telegram_id, "WAIT_FOR_DRINK")
        bot.telegram_client.answerCallbackQuery(update["callback_query"]["id"],)
        bot.telegram_client.deleteMessage(
            chat_id = update["callback_query"]["message"]["chat"]["id"],
            message_id = update["callback_query"]["message"]["message_id"],
        ) 
        bot.telegram_client.sendMessage(
            chat_id = update["callback_query"]["message"]["chat"]["id"],
            text = "Брат, какой диаметр?",
            reply_markup = json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Pepsa", "callback_data": "pizza"},
                            {"text": "Cool Coola", "callback_data": "pizza_pepperoni"},
                        ],
                        [
                            {"text": "Lipton", "callback_data": "pizza_parma"},
                            {"text": "Apple Juice", "callback_data": "pizza_quattro_stagioni"},
                        ]
                    ]
                }
            ),
        ) 
        return HandlerStatus.STOP