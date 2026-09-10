from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, MemberViewSet, LoanViewSet, CategoryViewSet
from rest_framework_simplejwt.views import ( 
    TokenObtainPairView,
    TokenRefreshView,)
from django.urls import path

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'members', MemberViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'categories', CategoryViewSet)


urlpatterns= [
path('token/',TokenObtainPairView.as_view(),name ='token_obtain_pair'),
path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),

] + router.urls