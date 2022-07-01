from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from habitation.users.managers import UserManager

class User(AbstractUser):
    """
    Default custom user model for habitation.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    #: First and last name do not cover name patterns around the globe
    username = None

    name = models.CharField(_("Name of User"), max_length=255)
    email = models.EmailField(
        _('email'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer.'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    image = models.ImageField(blank=True, null=True, upload_to='users_imgs')
    city = models.CharField(blank=True, null=True, max_length=25)
    phone_number = models.CharField(blank=True, null=True, max_length=11)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    objects = UserManager()


    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"email": self.email})
