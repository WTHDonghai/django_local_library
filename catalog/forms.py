from django import forms


from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime 
from . models import BookInstance

class RenewBookForm(forms.Form):

    """
    自定义表单数据
    """
    renewal_date = forms.DateField(help_text = "Enter a date between now and 4 weeks (default 3).")
    

    """
        表单和实体相关联
    """
    class Meta:
        model = BookInstance
        fields = ['due_back',]
        labels = {'due_back':_('Renewal date'),}
        #help_text = {'due_back':_('Enter a date between now and 4 weeks (default 3).')}

    #校验表单
    def clean_renewal_date(self):

        #将表单数据正确转化成期望的类型
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks = 4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data
