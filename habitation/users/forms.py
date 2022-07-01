from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)

        error_messages = {
            "email": {"unique": _("This email has already been taken.")}
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """
    


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
    
import re

from django import forms
from django.conf import settings
from django.forms import widgets
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .models import User


class SelectDateWidget(widgets.SelectDateWidget):
    none_value = ('', '----')


# class SignupForm(forms.ModelForm):

#     class Meta:
#         model = User

#         fields = ('email', 'password1', 'password2' )

#         widgets = {
#             'email': forms.EmailInput(),
#         }

#         labels = {
#             'email': _('E-mail address'),
#         }

#     def __init__(self, *args, **kwargs):

#         super(SignupForm, self).__init__(*args, **kwargs)
#         self.fields['email'].widget.attrs.update({'class': 'form-control', 'required': ''})


#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')

#         if password1 and password2:

#             if password1 != password2:
#                 raise forms.ValidationError(
#                     _("You must type the same password each time."))
#             elif re.match('^[a-z]*$', password2):
#                 raise forms.ValidationError(
#                     _('Password must contain at least one non-lower-case character.'))
#             elif re.match('^[A-Z]*$', password2):
#                 raise forms.ValidationError(
#                     _('Password must contain at least one non-upper-case character.'))

#         return self.cleaned_data['password2']

#     def signup(self, request, user):
#         # README: this is a simple hack for django-allauth to avoid
#         # saving the user twice
#         # https://github.com/pennersr/django-allauth/issues/607
#         pass
