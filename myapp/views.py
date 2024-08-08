from django.shortcuts import render,redirect

from django.views.generic import View

from myapp.forms import CategoryForm,TransactionForm,RegistrationForm,LoginForm

from myapp.models import Category,Transactions

from django.utils import timezone

from django.db.models import Sum,Avg

from django.contrib.auth import authenticate,login,logout



class CategoryCreateView(View):

    def get(self,request,*args,**kwargs):

        
        form_instance = CategoryForm()
        
        qs = Category.objects.filter(owner = request.user)
        # categories to view in the same add page

        return render(request,"category_add.html",{"form":form_instance,"categories":qs})
    
    
    
    def post(self,request,*args,**kwargs):

        form_instance = CategoryForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.owner = request.user
            # to take the logged in user to the owner details

            cat_name = form_instance.cleaned_data.get("name")

            user_obj = request.user

            is_exist = Category.objects.filter(name__iexact = cat_name , owner = user_obj).exists()

            if is_exist:

                print("already exists !!!!!")

                return render(request,"category_add.html",{"form":form_instance,"message":"Category already exists !!!"})
            
            else:


                form_instance.save()

                # OR

                # data = form_instance.cleaned_data

                # Category.objects.create(**data)

                return redirect("category-add")
        
        else:
            
            return render(request,"category_add.html",{"form":form_instance})
        


# category/<int:pk>/change
class CategoryEditView(View):

    def get(self,request,*args,**kwargs):

        id = kwargs.get("pk")

        category_object = Category.objects.get(id=id)

        form_instances = CategoryForm(instance=category_object)

        return render(request,"category_edit.html",{"form":form_instances})
    


    def post(self,request,*args,**kwargs):

        # id = kwargs.get("pk")

        # form_instances = CategoryForm(request.POST)

        # if form_instances.is_valid():
            
        #     data = form_instances.cleaned_data

        #     Category.objects.filter(id=id).update(**data)

        #     return redirect("category-add")
        # else:
        #     return render(request,"category_edit.html",{"form":form_instances})
        # old method for the same

        id = kwargs.get("pk")

        cat_obj = Category.objects.get(id=id)

        form_instance = CategoryForm(request.POST,instance=cat_obj)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("category-add")
        
        else:
            return render(request,"category_edit.html",{"form":form_instances})




class TransactionCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instances = TransactionForm()

        cur_year = timezone.now().year
        # .year to take the current year

        cur_month = timezone.now().month

        qs = Transactions.objects.filter(created_date__month = cur_month,created_date__year = cur_year,owner=request.user)

        # created_date__month = to take only the month in the created_date

        categories = Category.objects.filter(owner=request.user)
        # taking all data in the category of the logged in user

        return render(request,"transaction_add.html",{"form":form_instances,"transactions":qs,"categories":categories})
    

    def post(self,request,*args,**kwargs):

        form_instance = TransactionForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            return redirect("transaction-add")
        else:
            return render(request,"transaction_add.html",{"form":form_instance})
        



# url:lh:8000/transaction/<int:pk>/change/
# method get,post

class TransactionUpdateView(View):

    def get(self,request,*args,**kwargs):

        id = kwargs.get("pk")

        transaction_obj = Transactions.objects.get(id=id)

        form_instance = TransactionForm(instance=transaction_obj)

        return render(request,"transaction_edit.html",{"form":form_instance})
        

    def post(self,request,*args,**kwargs):

        id = kwargs.get("pk")

        transaction_obj = Transactions.objects.get(id=id)

        form_instance = TransactionForm(request.POST,instance=transaction_obj)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("transaction-add")
        
        else:
            return render(request,"transaction_edit.html",{"form":form_instance})



class TransactionDeleteView(View):

    def get(self,request,*args,**kwargs):

        id = kwargs.get("pk")

        Transactions.objects.get(id=id).delete()

        return redirect("transaction-add")
    



class ExpenseSummaryView(View):

    def get(self,request,*args,**kwargs):

        cur_year = timezone.now().year

        cur_month = timezone.now().month

        qs = Transactions.objects.filter(created_date__month = cur_month,
                                         created_date__year = cur_year)

        total_expense = qs.values("amount").aggregate(total = Sum("amount"))

        print(total_expense) # {'total': 320}

        data = {
            "total_expense":total_expense.get("total")
        }

        return render(request,"expense_summary.html",data)
    


        

        

class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance = RegistrationForm()

        return render(request,"register.html",{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        form_instance = RegistrationForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            print("Account created succesfully")

            return redirect("signin")
        
        else:

            print("Failed to create account")

            return render(request,"register.html",{"form":form_instance})


        
     

class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance = LoginForm()

        return render(request,"signin.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance = LoginForm(request.POST)

        if form_instance.is_valid():

            data = form_instance.cleaned_data #("username":"django","password":"Password@123")

            user_obj = authenticate(request,**data)

            if user_obj:

                login(request,user_obj)

                return redirect("category-add")
        
        return render(request,"signin.html",{"form":form_instance})
    

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")