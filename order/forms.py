from django import forms
from django.utils.translation import ugettext_lazy as _

from account.models import Address


class AddressForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Address
        fields = "__all__"
        exclude = ['created_at', 'updated_at', 'user']
        widgets = {'city': forms.TextInput(attrs={'placeholder': 'نام شهر'}),
                   'street': forms.TextInput(attrs={'placeholder': 'نام خیابان'}),
                   'allay': forms.TextInput(attrs={'placeholder': 'نام کوچه'}), }

