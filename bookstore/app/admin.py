from django.contrib import admin
from . models import books
# Register your models here.

@admin.register(books)
class BooksAdmin(admin.ModelAdmin):
    list_display=('title','author','description','published_date','price','created_at','updated_at')
    #search_fields = ('title', 'author')

   
   
  