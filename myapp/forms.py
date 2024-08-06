from django import forms

from myapp.models import Category,Transactions

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

class CategoryForm(forms.ModelForm):
# if inherited from ModelForm then meta class is required
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
        # widgets for styling the form
        
class TransactionForm(forms.ModelForm):

    class Meta:

        model = Transactions

        fields = ["title","amount","category_object","payment_method","user"]

        widgets = {
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "amount":forms.NumberInput(attrs={"class":"form-control"}),
            "category_object":forms.Select(attrs={"class":"form-control form-select"}),
            "payment_method":forms.Select(attrs={"class":"form-control form-select"}),
            "user":forms.TextInput(attrs={"class":"form-control"})
        }




class RegistrationForm(UserCreationForm):

    class Meta:

        model = User

        fields = ["username","email","password1","password2"]
