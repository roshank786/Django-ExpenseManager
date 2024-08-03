from django import forms
from myapp.models import Category,Transactions

class CategoryForm(forms.ModelForm):

    class Meta:

        model = Category

        fields = ["name","budget","owner"]

        # in this method we dont need to give the fields separately
        # like name = models.charfield()

        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "budget":forms.NumberInput(attrs={"class":"form-control"}),
            "owner":forms.TextInput(attrs={"class":"form-control"})
        }

class TransactionForm(forms.ModelForm):

    class Meta:

        model = Transactions

        fields = ["title","amount","category_object","payment_method","user"]