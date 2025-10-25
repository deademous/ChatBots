import json

import bot.telegram_client
import bot.database_client
from bot.handlers.handler import Handler, HandlerStatus

class CheckOrderHandler(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        if "callback_query" not in update:
            return False
        
        if state != "WAIT_FOR_ORDER_APPROVE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("check_")

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]
        chat_id = update["callback_query"]["message"]["chat"]["id"]
        
        bot.telegram_client.answerCallbackQuery(update["callback_query"]["id"])
        bot.telegram_client.deleteMessage(
            chat_id=chat_id,
            message_id=update["callback_query"]["message"]["message_id"],
        )
        
        # ИСПРАВЛЕННО: правильные условия для обеих кнопок
        if callback_data == "check_approve":
            bot.database_client.update_user_state(telegram_id, "ORDER_FINISHED")
            bot.telegram_client.sendMessage(
                chat_id=chat_id,
                text="Заказ уже готовится и скоро будет доставлен. Ожидайте!",
            )
        elif callback_data == "check_not_approve":
            bot.database_client.clear_user_state_and_order(telegram_id)
            bot.database_client.update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")
            
            bot.telegram_client.sendMessage(
                chat_id=chat_id,
                text="Начнем заново! Выберите пиццу:",
                reply_markup=json.dumps({
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
                }),
            )
        return HandlerStatus.STOP