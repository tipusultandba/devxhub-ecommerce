from django import forms
from .models import UserProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button

class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.TextInput(
        attrs={'type': 'date'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].disabled = True
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('user', css_class='form-group col-md-6 mb-0'),
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            Row(
                Column('date_of_birth', css_class='form-group col-md-6 mb-0'),
                Column('street', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            Row(
                Column('postal_code', css_class='form-group col-md-6 mb-0'),
                Column('country', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            Row(
                Column('billing_address', css_class='form-group col-md-6 mb-0'),
                Column('profile_picture', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            Row(
                Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                Column(Submit('submit', 'Update', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                css_class='row'
            ),
        )

    class Meta:
        model = UserProfile
        exclude = ("created_by", "updated_by")
