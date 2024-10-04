from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    watchlist = models.ManyToManyField(
        "Listing", blank=True, related_name="watchers"
    )


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Bid(models.Model):
    value = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        verbose_name="bidder",
        related_name="my_bids",
    )
    listing = models.ForeignKey(
        "Listing",
        on_delete=models.CASCADE,
        verbose_name="listing item",
        related_name="bids",
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"${self.value} by {self.user} on {self.listing}"

    def clean(self):
        initial_bid = self.listing.initial_bid
        if self.value < initial_bid:
            raise ValidationError(
                {"value": ("Bids must be higher than the initial bid.")}
            )


class Comment(models.Model):
    user = models.ForeignKey(
        "User", verbose_name="commenter", null=True, on_delete=models.SET_NULL
    )
    text_content = models.TextField(max_length=250)
    listing = models.ForeignKey(
        "Listing", related_name="comments", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.listing} | {self.user}: {self.text_content}"


class Listing(models.Model):
    created_by = models.ForeignKey("User", on_delete=models.CASCADE)
    is_active = models.BooleanField(
        "is open",
        default=True,
        help_text="Indicates if a Listing is open for new bids",
    )
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=240, blank=True)
    initial_bid = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(
        "Category", blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self) -> str:
        return self.title

    @property
    def current_bid(self) -> float:
        bids = self.bids.order_by("-value")
        return bids.first().value if bids.exists() else self.initial_bid

    @property
    def current_winner(self) -> User:
        bids = self.bids.order_by("-value")
        return bids.first().user if bids.exists() else None
