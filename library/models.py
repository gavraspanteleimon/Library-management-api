from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField(blank = True)
    birth_date = models.DateField(null=True , blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author , on_delete = models.CASCADE)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=200 , blank=True)

    def __str__(self):
        return self.user.username


class Loan(models.Model):
    book = models.ForeignKey(Book , on_delete=models.CASCADE)
    member =models.ForeignKey(Member,on_delete=models.CASCADE)
    loan_date = models.DateField(null=True , blank=True)
    return_date = models.DateField(null=True , blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book} loaned by {self.member}"