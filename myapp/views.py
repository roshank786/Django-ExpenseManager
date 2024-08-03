from django.shortcuts import render,redirect

from django.views.generic import View

from myapp.forms import CategoryForm

from myapp.models import Category



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