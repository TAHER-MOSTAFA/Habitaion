from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django.core.validators import MinValueValidator
from django.contrib.postgres.fields import ArrayField
from decimal import Decimal
User = get_user_model()


class AD(TimeStampedModel):
    AD_TYPES = Choices(
        'Apartment',
        'Villa',
        'Studio',
        'Room',
        'Home',
        'Hotel',
        'Apartment',
        'Office',
        'Flat',
        'Palace',    
    )    

    lord = models.ForeignKey(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    available = models.BooleanField(default=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    cash_discount = models.DecimalField(decimal_places=2, max_digits=4)

    type = models.CharField(choices=AD_TYPES, max_length=10)
    diriction = models.CharField(max_length=10)
    location = models.PointField()

    area = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    baths_no = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    bed_rooms_no = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return self.name
    
    @property
    def cash_price(self):
        return Decimal(self.price * (1-(self.cash_discount/100))).quantize(Decimal('1.00'))
    
    # @property
    # def is_fav

class Spec(TimeStampedModel):
    label = models.CharField(max_length=15)
    value = models.CharField(max_length=15)
    ad = models.ForeignKey(AD, on_delete=models.CASCADE)


class Image(models.Model):
    image = models.ImageField(upload_to="imgs")
    ad = models.ForeignKey(AD, on_delete=models.CASCADE, related_name="images")
    
class Plan(models.Model):
    ad = models.ForeignKey(AD, on_delete=models.CASCADE)
    first_intallemnt = models.PositiveIntegerField()
    monthly_intallemnt = models.PositiveIntegerField()
    duration = models.PositiveIntegerField()
    interest_rate = models.PositiveIntegerField()


class Favourites(TimeStampedModel):
    ad = models.ForeignKey(AD, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    