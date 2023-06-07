from django import forms
from phonenumber_field.formfields import PhoneNumberField


def password_validation(form):
    if form['password'] == form['confirm_password']:
        return True


def sustainable_settings(msg):
    """To reduce code repetition. The widget parameter is placed in a separate function.
     To display a message in a field, fill in the msg=str argument"""
    widget_settings = forms.TextInput(attrs={'placeholder': msg, 'required': 'True'})
    return widget_settings


class RegistrationTryForm(forms.Form):
    email = forms.EmailField(max_length=254,
                             widget=forms.TextInput(attrs={'placeholder': 'Enter your Email', 'required': 'True'}),
                             required=False)


class RegisterConfirmForm(forms.Form):
    mobile_phone = PhoneNumberField(
        region='UA', max_length=13,
        error_messages={'unique': 'Not a valid mobile phone. Enter again and correctly.'},
        required=False,
        widget=sustainable_settings('Enter your Phone Number'),
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=sustainable_settings('Enter your First name'),
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=sustainable_settings('Enter your Last name'),
    )
    fathers_name = forms.CharField(
        max_length=20,
        required=False,
        widget=sustainable_settings('Enter your Fathers name'),
    )
    country = forms.CharField(
        max_length=30,
        required=False,
        widget=sustainable_settings('Enter Country where you live'),
    )
    city = forms.CharField(
        max_length=30,
        required=False,
        widget=sustainable_settings('Enter City where you live'),
    )
    street = forms.CharField(
        max_length=50,
        required=False,
        widget=sustainable_settings('Enter Street where you live'),
    )
    house_number = forms.CharField(
        max_length=10,
        required=False,
        widget=sustainable_settings('Enter your House number'),
    )
    flat_number = forms.CharField(
        max_length=10,
        required=False,
        widget=sustainable_settings('Enter your Flat number'),
    )
    passport_series = forms.CharField(
        max_length=2,
        required=False,
        widget=sustainable_settings('Enter your Passport series'),
    )
    passport_number = forms.CharField(
        max_length=6,
        required=False,
        widget=sustainable_settings('Enter your Passport number'),
    )
    passport_date_of_issue = forms.DateField(
        required=False,
        widget=sustainable_settings('2006-10-25'),
    )
    passport_issuing_authority = forms.CharField(
        max_length=100,
        required=False,
        widget=sustainable_settings('Enter your Passport issuing authority'),
    )
    password = forms.CharField(
        max_length=128,
        required=False,
        widget=sustainable_settings('Create your password'),
    )
    confirm_password = forms.CharField(
        max_length=128,
        required=False,
        widget=sustainable_settings('Confirm your password'),
    )
