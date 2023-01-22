import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import BookInstance


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="A date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        today = datetime.date.today()

        if data < today:
            raise ValidationError(_("Invalid date - renewal in past"))
        if data > today + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        return data


class RenewBookModelForm(ModelForm):
    """
    This approach is better for forms that align with a single model
    and have many fields
    """
    def clearn_due_back(self):
        data = self.cleaned_data['due_back']
        today = datetime.date.today()
        if data < today:
            raise ValidationError(_('Invalid date - renewal in past'))
        if data > today + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))
        return data

    class Meta:
        model = BookInstance
        fields = ['due_back']  # could do fields = '__all__' or use exclude
        labels = {'due_back': _('New renewal date')}
        help_texts = {
            'due_back': _('Enter a date between now and 4 weeks (default 3).')}

