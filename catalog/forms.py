# Create your models here.
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import uuid # Required for unique book instances
import datetime
#from django.forms import ModelForm
from .models import BookInstance

class IssueBookModelForm(forms.ModelForm):
    """
        def clean_fine(self):
            data = self.cleaned_data['fine']
            data = 0
            return data

        def clean_status(self):
            data = self.cleaned_data['status']
            data = 'o'
            return data

        def clean_due_back(self):
            data = self.cleaned_data['due_back']
            data = datetime.date.today() + 60
            return data

        def clean_borrower(self):
            data = self.cleaned_data['borrower']
            if data not in User.objects.all():
                raise ValidationError(_('Invalid user!'))
            return data
    """

    class Meta:
        model = BookInstance
        fields = [ 'borrower', ]
        labels = { 'borrower': _('Borrower'), }
        help_texts = { }

        #fields = ['borrower', 'fine', 'status','id']
        #labels = { 'due_back': _('Renewal date'), 'borrower': _('Borrower'), 'fine': _('Fine'), 'status': _('Status'),}
        #help_texts = { 'due_back': _('Enter a date between now and 4 weeks (default 3).'), }


#class SearchString(forms.Form):
#    query = forms.CharField(max_length=50)


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text=f"Enter a date between now and {datetime.date.today() + datetime.timedelta(weeks=4)} (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data


class ReturnBookForm(forms.Form):
    condition = forms.CharField(max_length=1)
    #condition = forms.ChoiceField(kwargs=(('a', 'Available'), ('m', 'Mainetnance'), ('r', 'Reserved')), required=True, invalid_choice="You can't do this bruh")

    def clean_condition(self):
        data = self.cleaned_data['condition']
        if data not in ["m", "a", "r"]:
            raise ValidationError(_('Invalid condition - choose one of m, a or r'))
        return data
