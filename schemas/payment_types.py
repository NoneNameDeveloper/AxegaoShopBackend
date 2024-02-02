from pydantic import BaseModel


class PaymentTypes(BaseModel):
    """модель с доступными способами оплаты"""
    SBP: str = "sbp"
    SITE_BALANCE: str = "site_balance"
