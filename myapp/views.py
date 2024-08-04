from django.shortcuts import render,redirect

from django.views.generic import View

from myapp.forms import CategoryForm,TransactionForm

from myapp.models import Category,Transactions

from django.utils import timezone



class CategoryCreateView(View):

    def get(self,request,*args,**kwargs):

        
        form_instance = CategoryForm()
        
        qs = Category.objects.all()
        # categories to view in the same add page

        return render(request,"category_add.html",{"form":form_instance,"categories":qs})
    
    
    
    def post(self,request,*args,**kwargs):

        form_instance = CategoryForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()
            
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

        qs = Transactions.objects.filter(created_date__month = cur_month,created_date__year = cur_year)

        # created_date__month = to take only the month in the created_date

        return render(request,"transaction_add.html",{"form":form_instances,"transactions":qs})
    

    def post(self,request,*args,**kwargs):

        form_instance = TransactionForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("transaction-add")
        else:
            return render(request,"transaction_add.html",{"form":form_instances})
        



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