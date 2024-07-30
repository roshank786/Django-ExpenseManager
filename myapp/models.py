from django.db import models


# Create your models here.


class Category(models.Model):
    
    name = models.CharField(max_length=25)
    budget = models.PositiveIntegerField()
    owner = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Transactions(models.Model):

    title = models.CharField(max_length=50)
    amount = models.PositiveIntegerField()
    category_object = models.ForeignKey(Category,on_delete=models.CASCADE)

    payment_options = (
        ("Cash","cash"),
        ("UPI","upi"),
        ("Card","card")
    )

    payment_method = models.CharField(max_length=200,choices=payment_options,default="cash")

    created_date = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=200)



    def __str__(self):
        return self.title