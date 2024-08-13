from django.contrib import messages
from django.shortcuts import redirect


def signin_required(fn):

    def wrapper(request,*args,**kwargs):

        if not request.user.is_authenticated:
            
            messages.error(request,"Invalid session")

            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
        
    return wrapper

# this is a function decorator 
# we need to convert this into method decorator using in built django method_decorator
# @method_decorator(signin_decorator,name="dispatch")