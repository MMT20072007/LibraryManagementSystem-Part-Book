# MongoDB
INSTALLED_APPS = [
    'rest_framework',
    'django_mongodb_engine',
    'django_mongodb_engine.contrib',
    'djongo',
]

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'mydatabase',
        'HOST': 'mongodb://localhost:27017/',
    }
}

# models.py

from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title

# Serializer و Viewset

from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price', 'genre', 'author_city__id']
    search_fields = ['title', 'description']
    ordering_fields = ['price']

# models.py

from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255)
    birth_city = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# somesetting

python manage.py makemigrations
python manage.py migrate

# urls.py

from django.urls import include, path
from rest_framework import routers
from library.views import BookViewSet

router = routers.DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    ...
]