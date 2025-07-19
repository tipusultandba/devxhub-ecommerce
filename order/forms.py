from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150)
    city = forms.CharField(max_length=50)
    street = forms.CharField(max_length=150)
    phone_no = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()    
        self.helper.form_method = 'post'
        self.helper.form_id = 'id_checkout_form'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                
                css_class='row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('street', css_class='form-group col-md-6 mb-0'),

                css_class='row'
            ),
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('phone_no', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            Row(
                Column('address', css_class='form-group col-md-12 mb-0'),
                css_class='row'
            ),
            Row(
                Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                Column(Submit('submit', 'Continue', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                css_class='row'
            ),
        )