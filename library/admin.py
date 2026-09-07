from django.contrib import admin
from .models import Author, Category , Book , Loan , Member

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','bio','birth_date')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author')
    search_fields = ('title','author__name')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book','member','loan_date','return_date')
    search_fields = ('book__title','member__user__username','loan_date')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user','phone','address')
    search_fields = ('user__username','phone')
