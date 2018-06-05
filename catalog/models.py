from django.db import models
from django.urls import reverse
#from django.contrib.auth.decorators import permission_required
#from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your models here.

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import uuid # Required for unique book instances
import time
from datetime import date



def validate_isbn_check(isbn):
    """
    This function is used to validate the ISBN of the book according to the fratures given on the following website:  https://www.isbn-international.org/content/what-isbn
    """
    if len(str(abs(isbn))) != 13:
        raise ValidationError(
            _('%(isbn)s is not a valid ISBN'),
            params={'isbn': isbn},
        )


class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Language(models.Model):
    """
    Model representing a Language (e.g. English, French, Japanese, etc.)
    """
    name = models.CharField(max_length=200, help_text="Enter a the book's natural language (e.g. English, French, Japanese etc.")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET('get_author'))
    # Author as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(max_length=1000, null=True, blank="This book belongs to AD library. More information is not available right now. Please visit our library for details.", help_text='Enter a brief description of the book')
    isbn = models.BigIntegerField(unique=True, help_text="Enter 13 Character ISBN without space or dash. <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>", validators=[validate_isbn_check])
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    # Genre class has already been defined so we can specify the object above.
    languages = models.ManyToManyField(Language)
    #A book can be in many different language editions

    class Meta:
        ordering = ["title"]

    def get_author():
        return "Data Unavailable"

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this book.
        """
        return reverse('catalog:book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        #don't use join... you are fixing the layout part of the data
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
        display_genre.short_description = 'Genre'


from django.contrib.auth.models import User #Required to assign User as a borrower
class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library", verbose_name="Unique Identification Number")
    book = models.ForeignKey('Book', on_delete=models.SET('if_book_deleted'))
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    language = models.ForeignKey('Language', null=True,  on_delete=models.SET_NULL)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fine = models.PositiveSmallIntegerField(default=0)
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            self.fine = int((date.today() - self.due_back).days)*10
            return True
        return False

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=False, default='a', help_text='Book availability')


    class Meta:
        ordering = ["due_back"]
        permissions = (("can_list_all_borrowed", "List all borrowed books"), ("can_return", "Return issued books"), ("can_renew", "Renew issued books"), ("can_issue", "Issue Books"))


    def if_book_deleted():
        """
        It is a policy and security issue. We can't just prohibit deletion as well as shouldn't allow that anyone unauthorized deletes the book:
        1. If book discontinued, what happens to people who still have them issued?
        2. If someone hacks the DB and deletes the Book list, Shouldn't we save this transaction so that we get books from them at least
        """
        return "You are required to Immediately submit your book to library!"



    def __str__(self):
        """
        String for representing the Model object
        """
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField('Born', null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    #languages = models.ManyToManyField(Language)
    #genres = models.ManyToManyField(Genre)

    class Meta:
        ordering = ["first_name","last_name"]

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('catalog:author-detail', args=[str(self.id)])
