import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from apps.profiles.models import Profile, KYC
from niplan.settings.base import AUTH_USER_MODEL

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile when a new User is created.
    """
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"Profile created for {instance}")


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the Profile whenever the User is saved.
    """
    instance.profile.save()
    logger.info(f"Profile saved for {instance}")


@receiver(pre_save, sender=Profile)
def enforce_verification_for_seller_or_agent(sender, instance, **kwargs):
    """
    Signal to enforce phone number and KYC verification for sellers or agents.
    """
    if instance.is_seller or instance.is_agent:
        # Check if phone number is verified
        if not instance.is_verified:
            raise ValidationError(
                "Phone number must be verified to become a seller or agent."
            )

        # Check if KYC is verified
        if not hasattr(instance, "kyc") or not instance.kyc.kyc_verified:
            raise ValidationError("KYC must be verified to become a seller or agent.")


@receiver(post_save, sender=Profile)
def create_user_kyc(sender, instance, created, **kwargs):
    """
    Signal to create a KYC record when a new Profile is created.
    """
    if created:
        KYC.objects.create(profile=instance)
        logger.info(f"KYC created for {instance.user}'s profile")


@receiver(post_save, sender=KYC)
def save_user_kyc(sender, instance, **kwargs):
    """
    Signal to save the KYC record whenever it is updated.
    """
    logger.info(f"KYC saved for {instance.profile.user}'s profile")
