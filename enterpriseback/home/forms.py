from django import forms
from captcha.fields import ReCaptchaField

class MaintenanceForm(forms.Form):
    CHOICES_CONTACT = (('1', 'Phone',), ('2', 'Email',))
    CHOICES_PETS = (('1', 'Yes',), ('2', 'No',))
    CHOICES_MAINTENANCE = (
        ('1', 'I do not give permission to enter without my presence. I must be present during the repair appointment.',),
        ('2', 'Repair or damage caused by your negligence or misuse is your responsibility.',)
    )
    name = forms.CharField(required=True,max_length=100)
    email = forms.EmailField(required=True,max_length=100)
    adress = forms.CharField(required=True,max_length=100)
    phone_number = forms.CharField(required=True, max_length=20)
    unit_number = forms.CharField(required=True, max_length=50)
    file = forms.FileField(required=False)
    contact = forms.ChoiceField(required=True,choices=CHOICES_CONTACT, label="Preferred method of contact ")
    pets = forms.ChoiceField(required=False,choices=CHOICES_PETS)
    kind_pet = forms.CharField(required=False, max_length=50)
    option_maintenance = forms.ChoiceField(required=True,choices=CHOICES_MAINTENANCE)
    description = forms.CharField(required=False, max_length=350)
    captcha = ReCaptchaField()


class ContactForm(forms.Form):
    name = forms.CharField(required=True,max_length=100)
    email = forms.EmailField(required=True,max_length=100)
    phone_number = forms.CharField(required=True, max_length=20)
    subject = forms.CharField(required=True,max_length=100)
    description = forms.CharField(required=True, max_length=350)
    captcha = ReCaptchaField()

class MoveOutForm(forms.Form):
    CHOICES_STATE = (('1', 'California',), ('2', 'Texas',))

    name = forms.CharField(required=True,max_length=100)
    email = forms.EmailField(required=True,max_length=100)
    adress = forms.CharField(required=True,max_length=100)
    phone_number = forms.CharField(required=True, max_length=20)
    unit_number = forms.CharField(required=True, max_length=50)
    request_move_out_date= forms.CharField(required=True, max_length=50)
    city = forms.CharField(required=True, max_length=100)
    state = forms.ChoiceField(required=True,choices=CHOICES_STATE)
    zip_code = forms.CharField(required=True, max_length=10)
    captcha = ReCaptchaField()