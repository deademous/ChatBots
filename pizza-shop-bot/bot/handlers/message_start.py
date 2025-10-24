import json
import bot.telegram_client
import bot.database_client
from bot.handlers.handler import Handler, HandlerStatus

class MessageStart(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        return (
            "message" in update
            and "text" in update["message"]
            and update["message"]["text"] == "/start"
        )


    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["message"]["from"]["id"]
        bot.database_client.clear_user_state_and_order(telegram_id)
        bot.database_client.update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")
        bot.telegram_client.sendMessage(
            chat_id = update["message"]["chat"]["id"],
            text = "Добро пожаловать в нашу пиццерию! Приступим к заказу!",
            reply_markup = json.dumps({"remove_keyboard": True}),
        )

        bot.telegram_client.sendMessage(
            chat_id = update["message"]["chat"]["id"],
            text = "Выберите пиццу!",
            reply_markup = json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Маргарита", "callback_data": "pizza_margherita"},
                            {"text": "Пепперони", "callback_data": "pizza_pepperoni"},
                        ],
                        [
                            {"text": "Пармская", "callback_data": "pizza_parma"},
                            {"text": "4 сезона", "callback_data": "pizza_quattro_stagioni"},
                        ]
                    ]
                }
            ),
        )
        return HandlerStatus.STOP