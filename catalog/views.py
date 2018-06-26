from django.contrib.auth.decorators import permission_required
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from . models import Book,BookInstance,Genre,Author,Language

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

#from django.views.generic import ListView,DetailView
from django.views import generic

from .forms import RenewBookForm
import datetime

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy


# Create your views here.

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.

    #通过session保存用户的浏览次数
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1


    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={
            'num_books':num_books,
            'num_instances':num_instances,
            'num_instances_available':num_instances_available,
            'num_authors':num_authors,
            'num_visits':num_visits,
            },
    )


class BookListView(generic.ListView):

    model = Book
    context_object_name = 'book_list'
    template_name = '/catalog/book_list' 

    #分页
    paginate_by = 3 

    #queryset = Book.objects.filter(title_icontains = 'war')[:5]
    #override
    def get_queryset(self):
        #return Book.objects.filter(title__icontains = 'war')[:5]
        return Book.objects.all();

    #override
    def get_context_data(self,**kwargs):
        context = super(BookListView,self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context



class BookDetailView(generic.DetailView):
    
    model = Book

    def book_detail_view(request,pk):
        try:
            book_id = Book.objects.get(pk = pk)
        except Book.DoesNotExist:
            raise Http404("Book does not exist")

        #book_id = Http404("Book does not exist")

        return render(
                request,
                'catalog/book_detail.html',
                context = {'book':book_id,},
        )
    pass

class AuthorListView(generic.ListView):

    model = Author
    context_object_name = 'author_list'
    template_name = '/catalog/author_list.html'

    paginate_by = 5;

    def get_queryset(self):
        return Author.objects.all()



class AuthorDetailView(generic.DetailView):

    model = Author 

    def author_detail_view(request,pk):

        author_id = get_object_or_404(Author,pk = pk)

        return render(
                request,
                '/catalog/author_detail.html',
                {'author':author_id,}
                )


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact='o').order_by('due_back')


class CanMarkReturnedListView(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_can_mark_returned.html'
    paginate_by = 5;
    permission_required = 'catalog.can_mark_returned' 

    def get_queryset(self):
        return BookInstance.objects.filter(borrower__isnull=False).filter(status__exact = 'o').order_by("due_back")



@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request,pk):
    book_inst = get_object_or_404(BookInstance,pk = pk)

    if request.method == 'POST':

        #创建表单实例
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            
            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today()+datetime.timedelta(weeks = 3)
        form = RenewBookForm(initial= {'renewal_date':proposed_renewal_date,})

    #如果不是post请求(第一次初始化表单的时候)或者没有通过表单验证，需要绘制表单，对于后者，是第二次绘制表单（添加了错误）
    return render(request,'catalog/book_renew_librarian.html',{'form':form,'bookinst':book_inst})




"""
通用视图的表单
"""

class AuthorCreate(CreateView):
    model = Author
    #指定列出的字段（这里是所有字段）
    fields = '__all__'
    #指定字段默认值
    initial = {'date_of_death':'05/01/2018'}

    #如果该字段不指定，则会默认定位到模型的详情界面
    #success_url = reverse_lazy('authors')

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')



