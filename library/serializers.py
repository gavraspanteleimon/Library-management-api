from enum import member

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
    book_details = BookSerializer(source='book', read_only=True)           # ta balame gia na fainetai to onoma tou vivliou kai to onoma tou member sto loan  
    member_name = serializers.SerializerMethodField()    # ta balame gia na fainetai to onoma tou vivliou kai to onoma tou member sto loan  
    class Meta:
        model = Loan
        fields = ['id','book','book_details','member','member_name', 'loan_date', 'return_date', 'is_returned']

    def get_member_name(self, obj):
        return obj.member.user.username

class MemberRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField()
    address = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        user = User.objects.create_user(username=username, password=password)
        member = Member.objects.create(user=user, **validated_data)
        return member

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'username': instance.user.username,  # ρητά: πήγαινε ΜΕΣΑ στη σχέση
            'phone': instance.phone,
            'address': instance.address,
        }