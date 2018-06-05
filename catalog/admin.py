from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

#admin.site.register(BookInstance)
#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)

# Thses things below are changing the layout of data on the django-admin site.

class BookInline(admin.TabularInline):
    model = Book
    extra = 0

# Define a new admin class
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name',  'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death'),]

    inlines = [BookInline]

#admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra=0


@admin.register(Book)#Shortcut to admin.site.register(Book, BookAdmin), and needs to be written before the class, in contrary to after the class in case of the big one.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields':('status', 'due_back', 'borrower')
        }),
    )
