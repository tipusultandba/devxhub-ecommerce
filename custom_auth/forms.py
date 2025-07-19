from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils.text import capfirst
from django.contrib.auth import get_user_model
User = get_user_model()


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()    
        self.helper.form_id = 'id-signupForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
    
    # if need to de active user after registration.

    # def save(self, commit=True):
    #     obj = super(UserCreationForm, self).save(commit=False)
    #     obj.active = False
    #     if commit:
    #         obj.save()
    #     return obj

class LoginForm(AuthenticationForm):    
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = User._meta.get_field(User.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length
        if self.fields["username"].label is None:
            self.fields["username"].label = capfirst(self.username_field.verbose_name)
        # Form Helper Start from here.
        self.helper = FormHelper()    
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login'))


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()    
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Update'))