from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    
    name = models.CharField(max_length=25)
    budget = models.PositiveIntegerField()
    owner = models.ForeignKey(User,on_delete=models.CASCADE)


    class Meta:

        unique_together = ("name","owner")

    def __str__(self):
        return self.name


class Transactions(models.Model):

    title = models.CharField(max_length=50)
    amount = models.PositiveIntegerField()
    category_object = models.ForeignKey(Category,on_delete=models.CASCADE)

    payment_options = (
        ("cash","Cash"),
        ("upi","UPI"),
        ("card","Card")
    )

    payment_method = models.CharField(max_length=200,choices=payment_options,default="cash")

    created_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)



    def __str__(self):
        return self.title
    

# 'user' model is already is an inbuilt feature which is in the 'models.py' of the application 'django.contrib.auth' 
# go to forms to see the direct importing there