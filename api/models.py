import math
from django.db import models
from django.db.models import Avg, Count
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from solo.models import SingletonModel

phone_validator = RegexValidator(
    ' ^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$ ', _('phone must be in format'))
min_rating = MinValueValidator(1, 'at least 1')
max_rating = MaxValueValidator(5, 'max 5')

ORDER_STATUS_CHOICES = [
    ("pending", "pending"),
    ("assigned", "assigned"),
    ("on the way", "on the way"),
    ("delivered", "delivered"),
    ("canceled", "canceled"),
]


class Configuration(SingletonModel):

    exchange_rate = models.FloatField(_("exchange rate"), default=0)
    distributor_gain = models.FloatField(_("distributor gain"), default=0)
    delivery_distance_price = models.IntegerField(_("delivery distance price"), default=0)
    delivery_fixed_price = models.IntegerField(_("delivery fixed price"), default=300)

    class Meta:
        verbose_name = _("configuration")
        verbose_name_plural = _("configurations")

    def __str__(self):
        return 'Configuration'

    def get_absolute_url(self):
        return reverse("configuration_detail", kwargs={"pk": self.pk})


class Metrics(SingletonModel):

    @property
    def super_clients(self):
        users = Order.objects.values('user').annotate(
            total=Count('user')).order_by('-total')[:5]
        super_clients = []
        for user in users:
            super_clients.append({
                'user': get_user_model().objects.get(pk=user['user']),
                'total': user['total'],
            })
        print(super_clients)
        return super_clients

    class Meta:
        verbose_name = _("Metrics")

    def __str__(self):
        return 'metrics'

    def get_absolute_url(self):
        return reverse("metrics_detail", kwargs={"pk": self.pk})


class ProductCategory(models.Model):

    name = models.CharField(_("name"), max_length=24)
    business = models.ForeignKey("api.Restaurant", verbose_name=_(
        "business"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("productcategory_detail", kwargs={"pk": self.pk})


class Restaurant(models.Model):

    name = models.CharField(_("name"), max_length=70)
    description = models.TextField(_("description"))
    address = models.CharField(_("address"), max_length=150)
    phone = models.CharField(_("phone"), max_length=20,)
    image = models.ImageField(
        _("image"), upload_to='restaurants', null=True, blank=True)
    user = models.ForeignKey(
        get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE)
    time = models.CharField(_("time"), max_length=10)
    bussiness_type = models.ManyToManyField(
        "api.Category", verbose_name=_("Business type"))
    is_active = models.BooleanField(_("is active"), default=True)
    tax = models.FloatField(_("tax"), default=10)
    latitude = models.CharField(_("latitude"), max_length=25, default='')
    longitude = models.CharField(_("longitude"), max_length=25, default='')
    recommended = models.BooleanField(_("recommended"), default=False)

    @property
    def categories_product(self):
        return self.productcategory_set.all()

    @property
    def total_gain(self):
        return sum([order.product.price * order.amount for order in OrderDetail.objects.filter(product__restaurant=self, order__status='delivered')])

    @property
    def total_gain_clean(self):
        total_debt = sum([order.product.price * order.amount for order in OrderDetail.objects.filter(
            product__restaurant=self, order__status='delivered')])
        return float(self.total_gain) - (float(total_debt) * self.tax / 100)

    @property
    def debt(self):
        without_paid = sum([order.product.price * order.amount for order in OrderDetail.objects.filter(
            product__restaurant=self, was_paid_by_business=False, order__status='delivered')])
        return float(without_paid) * self.tax / 100

    @property
    def rating(self):
        return self.restaurantrating_set.aggregate(Avg('rating'))['rating__avg'] or 0

    @property
    def products(self):
        return self.product_set.filter(is_active=True)

    def rate(self, user, rating):
        RestaurantRating.objects.update_or_create(
            user=user, restaurant=self, defaults={'rating': int(rating)})

    class Meta:
        verbose_name = _("restaurant")
        verbose_name_plural = _("restaurants")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("restaurant_detail", kwargs={"pk": self.pk})


class RestaurantRating(models.Model):

    user = models.ForeignKey(get_user_model(), verbose_name=_(
        "user"), on_delete=models.CASCADE)
    restaurant = models.ForeignKey("api.Restaurant", verbose_name=_(
        "restaurant"), on_delete=models.CASCADE)
    rating = models.IntegerField(_("rating"), validators=[
                                 min_rating, max_rating])

    class Meta:
        verbose_name = _("restaurant rating")
        verbose_name_plural = _("restaurant ratings")

    def __str__(self):
        return f'{self.user} -> {self.restaurant}'

    def get_absolute_url(self):
        return reverse("restaurant_rating_detail", kwargs={"pk": self.pk})


class Distributor(models.Model):

    user = models.ForeignKey(get_user_model(), verbose_name=_(
        "user"), on_delete=models.CASCADE)
    vehicle_image = models.ImageField(
        _("vehicle image"), upload_to='distributors/vehicles', null=True, blank=True)
    vehicle_id = models.CharField(_("vehicle registration id"), max_length=7)
    vehicle_type = models.CharField(_("vehicle type"), max_length=20)
    is_online = models.BooleanField(_("is online"))

    @property
    def rating(self):
        return self.distributorrating_set.aggregate(Avg('rating'))['rating__avg'] or 0

    @property
    def total_gain(self):
        delivered_orders = self.order_set.filter(status='delivered')
        return float(sum([order.delivery_price for order in delivered_orders])) * float(Configuration.get_solo().distributor_gain) / 100

    @property
    def debt(self):

        orders = Order.objects.filter(
            distributor=self, was_paid_by_distributor=False, status='delivered')
        without_paid = sum([order.delivery_price for order in orders])
        return float(without_paid) * 20 / 100

    def rate(self, user, rating):
        DistributorRating.objects.update_or_create(
            user=user, distributor=self, defaults={'rating': int(rating)})

    class Meta:
        verbose_name = _("distributor")
        verbose_name_plural = _("distributors")

    def __str__(self):
        return self.user.first_name or self.user.email

    def get_absolute_url(self):
        return reverse("distributor_detail", kwargs={"pk": self.pk})


class DistributorRating(models.Model):

    user = models.ForeignKey(get_user_model(), verbose_name=_(
        "user"), on_delete=models.CASCADE)
    distributor = models.ForeignKey("api.Distributor", verbose_name=_(
        "distributor"), on_delete=models.CASCADE)
    rating = models.IntegerField(_("rating"), validators=[
                                 min_rating, max_rating])

    class Meta:
        verbose_name = _("Distributor rating")
        verbose_name_plural = _("Distributor ratings")

    def __str__(self):
        return f'{self.user} -> {self.distributor}'

    def get_absolute_url(self):
        return reverse("distributor_rating_detail", kwargs={"pk": self.pk})


class Category(models.Model):

    name = models.CharField(_("name"), max_length=20)

    class Meta:
        verbose_name = _("Business Category")
        verbose_name_plural = _("Business Categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})


class Product(models.Model):

    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"))
    price = models.DecimalField(_("price"), max_digits=6, decimal_places=2)
    time = models.CharField(_("time of preparation"), max_length=10)
    image = models.ImageField(
        _("image"), upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(
        "api.ProductCategory",
        verbose_name=_("category"),
        on_delete=models.PROTECT
    )
    restaurant = models.ForeignKey(
        "api.Restaurant",
        verbose_name=_("restaurant"),
        on_delete=models.CASCADE
    )
    um = models.CharField(_("unit of measurement"), max_length=10)
    amount = models.IntegerField(_("amount"))
    is_active = models.BooleanField(_("is active"), default=True)

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    @property
    def rating(self):
        return self.productrating_set.aggregate(Avg('rating'))['rating__avg'] or 0

    def rate(self, user, rating):
        ProductRating.objects.update_or_create(
            user=user, product=self, defaults={'rating': int(rating)})

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})


class ProductRating(models.Model):

    user = models.ForeignKey(get_user_model(), verbose_name=_(
        "user"), on_delete=models.CASCADE)
    product = models.ForeignKey("api.Product", verbose_name=_(
        "product"), on_delete=models.CASCADE)
    rating = models.IntegerField(_("rating"), validators=[
                                 min_rating, max_rating])

    class Meta:
        verbose_name = _("product rating")
        verbose_name_plural = _("product ratings")

    def __str__(self):
        return f'{self.user} -> {self.product}'

    def get_absolute_url(self):
        return reverse("product_rating_detail", kwargs={"pk": self.pk})


class Order(models.Model):

    user = models.ForeignKey(get_user_model(), verbose_name=_(
        "user"), on_delete=models.DO_NOTHING)
    distributor = models.ForeignKey("api.Distributor", verbose_name=_(
        "distributor"), on_delete=models.DO_NOTHING, null=True, blank=True)
    date = models.DateField(_("date"), auto_now=True)
    time = models.TimeField(_("time"), auto_now=True)
    delivery_address = models.ForeignKey(
        "directorio.Address", verbose_name=_("delivery address"), on_delete=models.PROTECT)
    status = models.CharField(
        _("status"), max_length=15, choices=ORDER_STATUS_CHOICES)
    pay_type = models.CharField(_("pay_type"), max_length=25)
    was_paid_by_distributor = models.BooleanField(
        _("was paid by distributor"),  default=False)
    delivery_total_distance = models.IntegerField(_("delivery total distance"))

    @property
    def total_price(self):
        return self.sub_total + self.delivery_price

    @property
    def sub_total(self):
        return sum([float(order_detail.product.price) * order_detail.amount for order_detail in self.products.all()])

    @property
    def delivery_price(self):
        if self.delivery_total_distance > 5:
            return self.delivery_total_distance * Configuration.get_solo().delivery_distance_price
        else:
            return Configuration.get_solo().delivery_fixed_price

    @property
    def business_orders(self):
        products = [{
            'detail': detail.product,
            'amount': detail.amount
        } for detail in self.orderdetail_set.all()]

        return [{
            'latitude': order.product.restaurant.latitude,
            'longitude': order.product.restaurant.longitude,
            'products': products,
        }
            for order in self.products
        ]

    @property
    def products(self):
        return self.orderdetail_set.all()

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})


class OrderDetail(models.Model):

    order = models.ForeignKey("api.Order", verbose_name=_(
        "order"), on_delete=models.CASCADE)
    product = models.ForeignKey("api.Product", verbose_name=_(
        "product"), on_delete=models.DO_NOTHING)
    amount = models.IntegerField(_("amount"), validators=[min_rating])
    was_paid_by_business = models.BooleanField(
        _("was paid by business"), default=False)

    @property
    def business(self):
        return self.product.restaurant

    @property
    def price(self):
        return self.product.price * self.amount

    class Meta:
        verbose_name = _("order detail")
        verbose_name_plural = _("order details")

    def __str__(self):
        return f'{self.order.user or ""}'

    def get_absolute_url(self):
        return reverse("orderdetail_detail", kwargs={"pk": self.pk})
