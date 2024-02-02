from datetime import datetime

from tortoise.models import Model
from tortoise import fields

from utils.images import create_user_photo


class Review(Model):
    id = fields.IntField(pk=True)

    accepted = fields.BooleanField(null=False, default=False)  # принят ли отзыв админом

    text = fields.TextField(null=False)  # текст отзыва

    rate = fields.IntField(null=False)  # максимум 5 звезд

    created_datetime = fields.DatetimeField(null=False, default=datetime.now)

    order = fields.OneToOneField("axegaoshop.Order", related_name="reviews")

    user = fields.ForeignKeyField("axegaoshop.User", related_name="reviews")

    parameter = fields.ForeignKeyField("axegaoshop.Parameter", related_name="reviews")

    photos: fields.ReverseRelation["ReviewPhoto"]

    class Meta:
        table = "reviews"


class ReviewPhoto(Model):
    id = fields.IntField(pk=True)

    photo = fields.TextField(null=False)
    review = fields.ForeignKeyField("axegaoshop.Review", related_name="review_photos")

    class Meta:
        table = "review_photos"
