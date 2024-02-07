from tortoise.models import Model
from tortoise import fields


class Review(Model):
    id = fields.IntField(pk=True)

    accepted = fields.BooleanField(null=False, default=False)  # принят ли отзыв админом

    text = fields.TextField(null=False)  # текст отзыва

    rate = fields.IntField(null=False)  # максимум 5 звезд

    created_datetime = fields.DatetimeField(null=False, auto_now_add=True)
    approved_datetime = fields.DatetimeField(null=False, auto_now=True)

    order = fields.OneToOneField("axegaoshop.Order", related_name="review")

    user = fields.ForeignKeyField("axegaoshop.User", related_name="reviews")

    photos: fields.ForeignKeyNullableRelation["ReviewPhoto"]

    class Meta:
        table = "reviews"
        ordering = ["-approved_datetime"]


class ReviewPhoto(Model):
    id = fields.IntField(pk=True)

    photo = fields.TextField(null=False)
    review = fields.ForeignKeyField("axegaoshop.Review", related_name="review_photos")

    class Meta:
        table = "review_photos"
