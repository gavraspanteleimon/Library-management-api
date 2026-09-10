from rest_framework import serializers
from .models import Author, Book, Member, Loan, Category
from django.contrib.auth.models import User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'birth_date']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'categories']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['user', 'phone', 'address']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['book', 'member', 'loan_date', 'return_date', 'is_returned']


class MemberRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(required=True)
    address = serializers.CharField(required=False, allow_blank=True)


    

    def create(self, validated_data):
        username = validated_data.pop['username']
        password = validated_data.pop['password']
        phone = validated_data['phone']
        address = validated_data.get('address', '')

        user = User.objects.create_user(username=username, password=password)
        member = Member.objects.create(user=user, **validated_data)
        return member