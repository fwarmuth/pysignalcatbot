from signalbot import SignalBot
import os
from loguru import logger
import logging

from pysignalcatbot.commands import CatNowCommand

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
class Bot():
    config = None
    bot: SignalBot = None

    def __init__(self, args):
        self.config = {
            "signal_service": args['api_endpoint'].replace('http://', '').replace('https://', '').replace('/v2/send', ''),
            "phone_number": args['number'],
            "storage": None,
            }

        bot = SignalBot(self.config)
        bot.register(CatNowCommand(path='./images'), groups=args['recipients'])
        logger.info("Bot started")
        bot.start()

