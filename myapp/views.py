from django.shortcuts import render,redirect

from django.views.generic import View

from myapp.forms import CategoryForm,TransactionForm,RegistrationForm,LoginForm

from myapp.models import Category,Transactions

from django.utils import timezone

from django.db.models import Sum,Avg

from django.contrib.auth import authenticate,login,logout

from django.contrib import messages

from myapp.decorators import signin_required

from django.utils.decorators import method_decorator




class CategoryCreateView(View):

    def get(self,request,*args,**kwargs):

        if not request.user.is_authenticated:

            messages.error(request,"Invalid session")
            
            return redirect("signin")

        form_instance = CategoryForm(user = request.user)
        
        qs = Category.objects.filter(owner = request.user)
        # categories to view in the same add page

        return render(request,"category_add.html",{"form":form_instance,"categories":qs})
    
    
    
    def post(self,request,*args,**kwargs):

        if not request.user.is_authenticated:

            messages.error(request,"Invalid session")
            
            return redirect("signin")

        form_instance = CategoryForm(request.POST,user = request.user,files=request.FILES)

        if form_instance.is_valid():

            form_instance.instance.owner = request.user
            # to take the logged in user to the owner details


            form_instance.save()

            # OR

            # data = form_instance.cleaned_data

            # Category.objects.create(**data)

            return redirect("category-add")
        
        else:
            
            return render(request,"category_add.html",{"form":form_instance})
        


# category/<int:pk>/change
@method_decorator(signin_required,name="dispatch")
class CategoryEditView(View):

    def get(self,request,*args,**kwargs):

        id = kwargs.get("pk")

        category_object = Category.objects.get(id=id)

        form_instances = CategoryForm(instance=category_object,user=request.user)

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

        form_instance = CategoryForm(request.POST,instance=cat_obj,user=request.user)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("category-add")
        
        else:
            return render(request,"category_edit.html",{"form":form_instance})




@method_decorator(signin_required,name="dispatch")
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

        form_instance = TransactionForm(request.POS)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            return redirect("transaction-add")
        else:
            return render(request,"transaction_add.html",{"form":form_instance})
        



# url:lh:8000/transaction/<int:pk>/change/
# method get,post

@method_decorator(signin_required,name="dispatch")
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



@method_decorator(signin_required,name="dispatch")
class TransactionDeleteView(View):

    def get(self,request,*args,**kwargs):

        id = kwargs.get("pk")

        Transactions.objects.get(id=id).delete()

        return redirect("transaction-add")
    


@method_decorator(signin_required,name="dispatch")
class ExpenseSummaryView(View):

    def get(self,request,*args,**kwargs):

        cur_year = timezone.now().year

        cur_month = timezone.now().month

        qs = Transactions.objects.filter(created_date__month = cur_month,
                                         created_date__year = cur_year,
                                         owner = request.user)

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

            messages.success(request,"Account created successfully")

            return redirect("signin")
        
        else:

            print("Failed to create account")

            messages.error(request,"Failed to create account")

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

                messages.success(request,"Signed in successfully")

                return redirect("category-add")
            
            messages.error(request,"Sign in failed")
        
        return render(request,"signin.html",{"form":form_instance})
    
@method_decorator(signin_required,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")