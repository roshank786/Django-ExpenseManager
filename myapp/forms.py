from django import forms

from myapp.models import Category,Transactions

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

class CategoryForm(forms.ModelForm):
# if inherited from ModelForm then meta class is required


    def __init__(self,*args,**kwargs):
        
        self.user = kwargs.pop("user")
        # pop is used because we dont need to keep the user in the dictionary,so to store it to a variable user and the 
        # delete it from the dictionary

        return super().__init__(*args,**kwargs)


    class Meta:

        model = Category

        fields = ["name","budget"]

        # in this method we dont need to give the fields separately
        # like name = models.charfield()

        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "budget":forms.NumberInput(attrs={"class":"form-control"})
        }
        # widgets for styling the form
        

    def clean(self):

        self.cleaned_data = super().clean()

        print(self.user,"inside category form")
        # user in the view is displayed in the form

        budget_amount = int(self.cleaned_data.get("budget"))

        if budget_amount < 150:

            self.add_error("budget","Amount should be min of 150")

        category_name = self.cleaned_data.get("name")

        owner = self.user

        is_exist = Category.objects.filter(name__iexact = category_name,owner=owner).exists()

        if is_exist:

            self.add_error("name","Category already exists !!!")

        return self.cleaned_data



class TransactionForm(forms.ModelForm):

    class Meta:

        model = Transactions

        fields = ["title","amount","category_object","payment_method"]

        widgets = {
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "amount":forms.NumberInput(attrs={"class":"form-control"}),
            "category_object":forms.Select(attrs={"class":"form-control form-select"}),
            "payment_method":forms.Select(attrs={"class":"form-control form-select"})
        }




class RegistrationForm(UserCreationForm):

    class Meta:

        model = User

        fields = ["username","email","password1","password2"]

        widgets = {
        "username":forms.TextInput(attrs={"class":"form-control"}),
        "email":forms.TextInput(attrs={"class":"form-control"}),
        "password1":forms.TextInput(attrs={"class":"form-control"}),
        "password2":forms.TextInput(attrs={"class":"form-control"})
    }


class LoginForm(forms.Form):

    username = forms.CharField()

    password = forms.CharField()

    widgets = {
        "username":forms.TextInput(attrs={"class":"form-control"}),
        "password":forms.TextInput(attrs={"class":"form-control"})
    }