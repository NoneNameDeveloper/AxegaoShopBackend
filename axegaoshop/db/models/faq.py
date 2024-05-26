from tortoise import fields
from tortoise.models import Model


class Faq(Model):
    """пользовательское соглашение"""

    id = fields.BigIntField(pk=True)

    content = fields.TextField(null=False)
    title = fields.CharField(null=False, max_length=100)

    def slug(self) -> str:
        """
        slug для FAQ
        """
        return self.title.replace(" ", "-").lower() + "-" + str(self.id)

    class PydanticMeta:
        computed = ("slug",)

    class Meta:
        table = "faqs"
