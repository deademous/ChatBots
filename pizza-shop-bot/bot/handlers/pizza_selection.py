import json

import bot.telegram_client
import bot.database_client
from bot.handlers.handler import Handler, HandlerStatus

class PizzaSelectionHandler(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        if "callback_query" not in update:
            return False
        
        if state != "WAIT_FOR_PIZZA_NAME":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("pizza_")

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        pizza_mapping = {
            "pizza_margherita": "Маргарита",
            "pizza_pepperoni": "Пепперони", 
            "pizza_parma": "Пармская",
            "pizza_quattro_stagioni": "Четыре сезона"
        }
        pizza_name = pizza_mapping.get(callback_data)
        bot.database_client.update_user_data(telegram_id, {"pizza_name": pizza_name})
        bot.database_client.update_user_state(telegram_id, "WAIT_FOR_PIZZA_SIZE")
        bot.telegram_client.answerCallbackQuery(update["callback_query"]["id"],)
        bot.telegram_client.deleteMessage(
            chat_id = update["callback_query"]["message"]["chat"]["id"],
            message_id = update["callback_query"]["message"]["message_id"],
        ) 
        bot.telegram_client.sendMessage(
            chat_id = update["callback_query"]["message"]["chat"]["id"],
            text = "Выберите размер пиццы:",
            reply_markup = json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "20 см", "callback_data": "size_small"},
                            {"text": "25 см", "callback_data": "size_medium"},
                        ],
                        [
                            {"text": "30 см", "callback_data": "size_large"},
                            {"text": "40 см", "callback_data": "size_xl"},
                        ]
                    ]
                }
            ),
        ) 
        return HandlerStatus.STOP