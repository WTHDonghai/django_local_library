from django.db import models

#倒入用户类
from django.contrib.auth.models import User

# Create your models here.
from django.urls.base import reverse
import uuid
from datetime import date

class Genre(models.Model):

    name = models.CharField(max_length = 200,help_text = "Entry a book genre(e.g. Science Fiction, French Poetry etc.)");

    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(max_length = 200)

    #书和作者1:*关系，所以在书的模型中建立外键链接作者
    author = models.ForeignKey('Author',on_delete = models.SET_NULL,null = True)

    summary = models.TextField(max_length = 1000,help_text = "Enter a brief description of the book")

    isbn = models.CharField('ISBN',max_length = 13,help_text = '13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre,help_text = "Select a genre for this book")
    
    language = models.ForeignKey('Language',max_length = 100,null = True,on_delete = models.SET_NULL)

    def display_genre(self):
        return ', '.join( genre.name for genre in self.genre.all()[:3] )

    #这我他妈就懵圈了，这个是怎么被调用的？方法名怎么又可以访问方法
    display_genre.short_description = 'Genre'
    #display_genre.long_descrption= 'Genre'
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail',args = [str(self.id),]) 

class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True,default = uuid.uuid4,help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book',on_delete=models.SET_NULL,null = True)
    imprint = models.CharField(max_length = 200)
    due_back = models.DateField(null = True,blank = True)

    LOAN_STATUS = (
        ('m','Maintenance'),
        ('o','On loan'),
        ('a','Available'),
        ('r','Reserved'),
    )

    status = models.CharField(max_length = 1,choices = LOAN_STATUS,blank = True,default = 'm',help_text = "Book availability")

    #借阅的用户
    borrower = models.ForeignKey(User,on_delete = models.SET_NULL,null = True,blank = True) 

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned","Set book as returned"),)

    def display_book(self):
        return self.book.title
    display_book.short_description = "Book"

    '''
    是否过期
    '''
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    
    def __str__(self):
        return '{0} {1}'.format(self.id,self.book.title)


class Author(models.Model):

    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    date_of_birth = models.DateField(null = True,blank = True)
    date_of_death = models.DateField('Died',null = True,blank = True)

    def get_absolute_url(self):
        return reverse('author-detail',args = [str(self.id)]) 

    def __str__(self):
        return '{0}, {1}'.format(self.last_name,self.first_name) 


    class Meta:
        ordering = ['last_name'] 

class Language(models.Model):

    name = models.CharField(max_length = 200,help_text = "Enter a the book's natural language(e.g. English,French,Japanese etc.)")

    def __str__(self):
        return self.name 







