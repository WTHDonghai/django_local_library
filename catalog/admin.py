from django.contrib import admin

# Register your models here.
from . models import Author,Genre,Book,BookInstance,Language

admin.site.register([Genre,Language])

#admin.site.register(Author)
#admin.site.register(Book)
#admin.site.register(BookInstance)

#自定义某个模型的（Author）的管理页面
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','date_of_birth','date_of_death')

    #明细列表显示的样式，和字段。数组里每一个元素代表一行，还可以嵌套元祖
    fields = ['first_name','last_name',('date_of_birth','date_of_death')]

    date_hierarchy = 'date_of_birth'

#admin.site.register(Author,AuthorAdmin)


#内联
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    classes = ['collapse','wide','extraretty']

    #这里赋整型0表示，只展示一条与之相关联的数据
    extra = 0

    #只显示个别字段
    #fields = ['imprint','due_back','status']


#注册实体与管理页面（做关联），可以写成注解
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    '''
    由于author对应的字段是一个对象（书和作者1对1关系）
    这里将会获取对象的__str__方法返回的字符串。
    display_genre 参数对应的字段是一个方法，这里将会获取该方法返回的字符串
    '''
    list_display = ('title','author','display_genre')

    date_hierarchy = 'author__date_of_birth'

    inlines = [BookInstanceInline]
    pass

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):

    search_fields = ['imprint'] 

    list_filter = ('status','due_back')

    list_display = ('id','display_book','borrower','due_back','status')

    #明细列表显示，提供了更多的选项
    fieldsets = (
            (None,{
                'fields':('book','imprint','id'),
            }),
            ('Availability',{
                #wide ,extraretty 
                #'classes':('collapse',),
                'fields':('status','due_back','borrower',),
            })
    )

    pass



