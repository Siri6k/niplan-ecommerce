from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Gender(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")


class Profile(TimeStampedUUIDModel):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"),
        max_length=30,
        blank=True,
        null=True,
        unique=True,  # Ensure secondary phone number is unique (if provided)
        help_text=_("Primary phone number must be unique."),
    )
    second_phone_number = PhoneNumberField(
        verbose_name=_("Secondary Phone Number"),
        max_length=30,
        blank=True,
        null=True,
        help_text=_("Optional secondary phone number for additional contact."),
    )
    otp = models.CharField(max_length=6, blank=True, null=True)  # New field for OTP
    is_verified = models.BooleanField(
        default=False
    )  # New field for verification status
    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.choices,
        default=Gender.MALE,
        max_length=20,
    )
    about_me = models.TextField(
        verbose_name=_("About me"), default="Say something about yourself"
    )

    profile_photo = models.ImageField(
        verbose_name=_("Profile Photo"), default="profile_default.png"
    )
    country = CountryField(
        verbose_name=_("Country"), max_length=180, default="CD", blank=False, null=False
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=180,
        default="Lubumbashi",
        blank=False,
        null=False,
    )
    is_buyer = models.BooleanField(
        verbose_name=_("Buyer"),
        default=True,
        help_text=_("Are you looking to Buy a Product"),
    )
    is_seller = models.BooleanField(
        verbose_name=_("Seller"),
        default=False,
        help_text=_("Are you looking to Sell a Product"),
    )
    is_agent = models.BooleanField(
        verbose_name=_("Agent"), default=False, help_text=_("Are you an Agent?")
    )

    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    num_reviews = models.IntegerField(
        verbose_name=_("Number of Reviews"), default=0, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s profile"


class KYC(TimeStampedUUIDModel):
    profile = models.OneToOneField(
        Profile,
        related_name="kyc",
        on_delete=models.CASCADE,
        help_text=_("The profile associated with this KYC information."),
    )
    government_id = models.CharField(
        verbose_name=_("Government ID"),
        max_length=50,
        blank=True,
        null=True,
        help_text=_(
            "Government-issued identification number (e.g., passport, national ID)."
        ),
    )
    government_id_image = models.ImageField(
        verbose_name=_("Government ID Image"),
        upload_to="kyc/government_ids/",
        blank=True,
        null=True,
        help_text=_("Upload an image of your government-issued ID."),
    )
    proof_of_address = models.ImageField(
        verbose_name=_("Proof of Address"),
        upload_to="kyc/proof_of_address/",
        blank=True,
        null=True,
        help_text=_(
            "Upload a document that proves your address (e.g., utility bill, bank statement)."
        ),
    )
    kyc_verified = models.BooleanField(
        verbose_name=_("KYC Verified"),
        default=False,
        help_text=_("Indicates whether the user's KYC information has been verified."),
    )

    kyc_verified_at = models.DateTimeField(
        verbose_name=_("KYC Verified At"),
        blank=True,
        null=True,
        help_text=_("Timestamp when the user's KYC information was verified."),
    )

    def __str__(self):
        return f"KYC for {self.profile.user.username}"
