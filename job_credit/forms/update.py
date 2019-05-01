# job_credit/forms/update.py

from django import forms

from ..models import Record


class CreditRecordCreationForm(forms.ModelForm):

    class Meta:
        model = Record
        fields = ['site_user', 'action', 'amount', 'description']

    def save(self, commit=True):
        """
        Hook into save method to update credits

        :param commit:
        :return:
        """
        user = self.instance.site_user
        act = self.instance.action
        amount = self.instance.amount

        if act == Record.ACTION_CONSUME:
            user.credit_bank.balance -= amount
        else:
            user.credit_bank.balance += amount

        user.credit_bank.save()
        self.instance.balance = user.credits

        return super(CreditRecordCreationForm, self).save(commit=commit)
