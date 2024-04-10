import aioyagmail
import yagmail

from axegaoshop.services.notifications.mailing.utils import render_template
from axegaoshop.settings import settings


class MessageTypes:
    RESET_PASSWORD = "reset.html"
    SHIPPING = "shipping.html"
    PURCHASE = "purchase.html"
    TICKET_MESSAGE = "message.html"


class Mailer:
    """модуль для работы с почтовыми сообщениями"""
    def __init__(self, recipient: str):
        self.mailer_ = yagmail.SMTP(
            user=settings.mail_user,
            password=settings.mail_password,
            host=settings.mail_host,
            port=settings.mail_port,
        )
        # получатель письма
        self.recipient = recipient

    async def send_reset(
            self,
            reset_url: str
    ):
        """письмо на сброс пароля"""
        self.mailer_.send(
            self.recipient,
            subject="LoftSoft Сброс Пароля",
            contents=render_template(MessageTypes.RESET_PASSWORD, reset_url=reset_url),
        )

    async def send_shipping(
            self,
            parameters: list[dict],
            total_sum: float,
            total_count: int,
            hand: bool = True
    ):
        """письмо на покупку товара"""
        print(parameters)
        print(total_count, total_sum)
        for p in parameters:
            p['photo'] = "http://fileshare.su:8000/api/uploads/L3ZKA1tU667CvcJn.png"
        if not hand:
            self.mailer_.send(
                self.recipient,
                subject="LoftSoft Покупка Товара",
                contents=render_template(
                    MessageTypes.PURCHASE,
                    parameters=parameters,
                    total_sum=total_sum,
                    total_count=total_count
                ),
            )
        else:
            self.mailer_.send(
                self.recipient,
                subject="LoftSoft Покупка Товара",
                contents=render_template(
                    MessageTypes.SHIPPING,
                    parameters=parameters,
                    total_sum=total_sum,
                    total_count=total_count
                ),
            )

    async def send_ticket_message(self, content: str):
        self.mailer_.send(
            self.recipient,
            subject="LoftSoft Сообщение от Поддержки",
            contents=render_template(
                MessageTypes.TICKET_MESSAGE,
                content=content
            ),
        )
#
# m = Mailer(recipient="homycoder@gmail.com")
#
# m.send_reset("https://google.com")
