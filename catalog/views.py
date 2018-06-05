from django.views import generic
from django.shortcuts import get_object_or_404, render
from datetime import date
#from django.urls import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RenewBookForm, ReturnBookForm, IssueBookModelForm
from .models import Book, Author, BookInstance, Genre
from uauth.models import Uauth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
#from django.contrib.auth.models import User
# Create your views here.
#from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# to create Author
class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}
    #success_url = reverse_lazy('catalog:authors')

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    #success_url = reverse_lazy('catalog:authors')

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('catalog:authors')

# to create Book
class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    initial={'title':'Title', 'summary':'Summary', }
    #success_url = reverse_lazy('catalog:books')

class BookUpdate(UpdateView):
    model = Book
    fields = ['__all__']
    #success_url = reverse_lazy('catalog:books')

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('catalog:books')

#to create BookInstance
class BookInstanceCreate(CreateView):
    model = BookInstance
    fields = ['book', 'imprint', 'language', 'status']
    initial={'imprint':'Penguin', 'due_back':None, 'fine':0, 'status':'a',}
    #success_url = reverse_lazy('catalog:books')

class BookInstanceUpdate(UpdateView):
    model = BookInstance
    fields = ['book', 'imprint', 'language', 'status']
    #success_url = reverse_lazy('catalog:books')

class BookInstanceDelete(DeleteView):
    model = BookInstance
    success_url = reverse_lazy('catalog:books')




def index(request):
    """
    View function for home page of site.
    """

    #Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    #Available books
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.
    #logged_in = request.user.is_authenticated ---no need as better way is found
    return render(
        request,
        'catalog/index.html',
        context={
            'num_books':num_books,
            'num_instances':num_instances,
            'num_instances_available':num_instances_available,
            'num_authors':num_authors,
            'num_visits':num_visits,
        })
    #render() function creates and returns an HTML page as a response


class BookListView(LoginRequiredMixin, generic.ListView):
    login_url = '/uauth/login/'
    model = Book
    paginate_by = 3


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/uauth/login/'
    model = Book
    paginate_by = 1

    def book_detail_view(request, pk):
        book_id = get_object_or_404(pk=pk)
        return render(
            request,
            'catalog/book_detail.html',
            context={'book':book_id, }
        )


class AuthorListView(LoginRequiredMixin, generic.ListView):
    login_url = '/uauth/login/'
    model = Author
    paginate_by = 1


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    paginate_by = 1
    login_url = '/uauth/login/'
    def author_detail_view(self, request, pk):
        author_id = get_object_or_404(pk=pk)
        is_dead = False
        age = date.today() - author_id.date_of_birth
        if author_id.date_of_death < date.today():
            is_dead = True
            age = author_id.date_of_death - author_id.date_of_birth
        return render(
            request,
            'catalog/author_detail.html',
            context={'author':author_id, 'is_dead':is_dead, 'age':age, },
            #context={'author':author_id,},
        )


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    login_url = '/uauth/login/'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllLoanedBooksListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing all books on loan to currently logged in library staff.
    """
    login_url = '/uauth/login'
    model = BookInstance
    permission_required = 'catalog.can_list_all_borrowed'
    template_name = 'catalog/all_borrowed_books.html'
    paginate_by = 10

    def get_queryset(self):
        #users = User.objects.all()
        #bookinstance_list = []
        #for user in users:
            #bookinstance_list += BookInstance.objects.filter(borrower=user).filter(status__exact='o').order_by('due_back')
        #return bookinstance_list
        return BookInstance.objects.all().filter(status__exact='o').order_by('due_back')

@login_required
@permission_required('catalog.can_renew')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk=pk)

    #If this is a POST request then process the form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request(binding)
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            # redirect to a new url
            return HttpResponseRedirect(reverse('catalog:all-borrowed'))
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

@login_required
@permission_required('catalog.can_return')
def return_book_librarian(request, pk):
    pass
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk=pk)

    #If this is a POST request then process the form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request(binding)
        form = ReturnBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.status = form.cleaned_data['condition']
            book_inst.borrower = None #User.objects.all().filter(username__exact='lib')
            book_inst.due_back = None
            book_inst.save()
            # redirect to a new url
            return HttpResponseRedirect(reverse('catalog:all-borrowed'))
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_status = "a"
        form = ReturnBookForm(initial={'condition': proposed_status,})

    return render(request, 'catalog/book_return_librarian.html', {'form': form, 'bookinst':book_inst})


@login_required
@permission_required('catalog.can_issue')
def issue_book_librarian(request, pk):
    """
    View function to issue a specific BookInstance by librarian
    """
    book_instance=get_object_or_404(BookInstance, pk=pk)

    #If this is a POST request then process the form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request(binding)
        form1 = IssueBookModelForm(request.POST)

        # Check if the form is valid:
        if form1.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.status = "o"
            book_instance.fine = 0
            book_instance.borrower = form1.cleaned_data['borrower'] #User.objects.all().filter(username__exact='lib')
            book_instance.due_back = datetime.date.today() + datetime.timedelta(60)
            book_instance.save()
            # redirect to a new url
            return HttpResponseRedirect(reverse('catalog:all-borrowed'))
    # If this is a GET (or any other method) create the default form.
    else:
        due_back_default = datetime.date.today() + datetime.timedelta(60)
        form1 = ReturnBookForm(initial={'due_back':due_back_default , 'fine':0, 'status':"o",})

    return render(request, 'catalog/book_issue_librarian.html', {'form1': form1, 'bookinstance':book_instance})



"""
def search(request, query):
    book=get_object_or_404(Book, pk=query)

    #If this is a POST request then process the form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request(binding)
        form = SearchString(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            book.save()
            # redirect to a new url
            return HttpResponseRedirect(reverse('catalog:search'))
    return render(
        request,
        'catalog/search.html',
        context={'form': form, 'result':book,}
    )
"""

"""
def books(request):
    book_list=['Hello zindagi', 'Koolie', 'Kya cool hain hum']
    return render(
        request,
        'catalog/books.html',
        context={
            'book_list':book_list,
            },)
"""
# regex to encode a date from a url
# r'^book/(?P<int:year>\d+)[/](?P<int:month>\d+)[/](?P<int:day>\d+)$'
