from axegaoshop.db.models.payment_settings import get_ozone_bank_data
from axegaoshop.services.payment.sbp.ozon_bank import OzoneBank


async def get_ozone_bank() -> OzoneBank | None:
    """получение объекта OzoneBank для работы с платегой"""
    data = await get_ozone_bank_data()

    if not data:
        yield None

    yield await OzoneBank(
        pin_code=data.pin_code,
        secure_refresh_token=data.token
    ).prepare()

