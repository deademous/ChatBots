import bot.telegram_client
from bot.handler import Handler

class EchoPhotoHandler(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and "photo" in update["message"]
    
    def handle(self, update: dict) -> bool:
        photo = update["message"]["photo"][-1]
        file_id = photo["file_id"]
        caption = ""

        if "caption" in update["message"]:
            caption = update["message"]["caption"]

        bot.telegram_client.sendPhoto(
            chat_id=update["message"]["chat"]["id"],
            photo=file_id,
            caption=caption
        )
        return False