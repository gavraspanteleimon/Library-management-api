from django.shortcuts import render
from rest_framework import viewsets,generics
from .models import Author, Book, Member, Loan, Category
from .serializers import AuthorSerializer, BookSerializer, MemberSerializer, LoanSerializer, CategorySerializer,MemberRegistrationSerializer
from rest_framework.permissions import AllowAny


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MemberRegistrationViewSet(generics.CreateAPIView):
    serializer_class = MemberRegistrationSerializer
    permission_classes = [AllowAny]  # Allow anyone to register

# Create your views here.
