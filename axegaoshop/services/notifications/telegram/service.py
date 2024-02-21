import asyncio
import typing

from aiogram import Bot
from aiogram.utils.token import TokenValidationError

from axegaoshop.services.notifications.telegram.templates import SELL_NOTIFY_TEMPLATE


class TelegramService:
    def __init__(self, token: str, recievers: list[int]):
        self.bot_token = token
        self.bot: Bot = self.connect_bot()
        self.recievers = recievers
        self.error = None
        self.s = self.bot.session
        if not self.bot:
            self.error = "INVALID_TOKEN"
                
    def connect_bot(self):
        try:
            return Bot(self.bot_token)
        except TokenValidationError:
            return None

    def available(self) -> bool:
        """если доступно исползование рассылки тг - True
        если что-то не то - False"""
        return True if not self.error else False

    async def notify(self, type_: typing.Literal['sell', 'ticket'], data: dict):
        """отправка уведомлений о покупке либо о новых сообщениях в тикете"""
        if type_ == 'sell':
            for reciever in self.recievers:
                try:
                    await self.bot.send_message(
                        chat_id=reciever,
                        text=SELL_NOTIFY_TEMPLATE.format(
                            ITEM=data['item'],
                            TITLE=data['title'],
                            PROMOCODE=data['promocode'],
                            COUNT=data['count']
                        )
                    )
                except:
                    pass

        elif type == "ticket":
            for reciever in self.recievers:
                try:
                    await self.bot.send_message(
                        chat_id=reciever,
                        text=SELL_NOTIFY_TEMPLATE.format(
                            NUMBER=data['number'],
                            SENDER=data['sender'],
                            CONTENT=data['content'],
                        )
                    )
                except:
                    pass

    async def test_notify(self):
        """отправка тестового уведомления"""
        for reciever in self.recievers:
            try:
                await self.bot.send_message(reciever, "Тест")
            except:
                pass