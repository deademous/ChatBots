from bot.dispatcher import Dispatcher
from bot.handlers.database_logger import DatabaseLogger
from bot.handlers.echo_handler import EchoHandler
from bot.long_polling import start_long_polling

if __name__ == "__main__":
    try:
        dispatcher = Dispatcher()
        dispatcher.add_handlers(EchoHandler())
        start_long_polling(dispatcher)
    except KeyboardInterrupt:
        print("\nBye!")