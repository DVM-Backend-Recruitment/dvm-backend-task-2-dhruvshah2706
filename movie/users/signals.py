from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.socialaccount.signals import social_account_added  # Import the social account signal
from .models import Profile

# Signal to create a Profile when a new User is created
@receiver(post_save,  sender=User)
def create_user_profile(sender,  instance,  created,  **kwargs):
    if created and not hasattr(instance,  'bypass_profile_creation'):
        Profile.objects.get_or_create(user=instance)
        

@receiver(post_save,  sender=User)
def save_user_profile(sender,  instance,  **kwargs):
   instance.profile.save()  # Save any updates to profile automatically

# # Signal to ensure Profile creation for Google/social logins
# @receiver(social_account_added)
# def ensure_profile_for_social_user(request,  sociallogin,  **kwargs):
#     print("I'm in ensure")
#     user = sociallogin.user
#     Profile.objects.get_or_create(user=user)  # Creates profile if it doesn't exist
