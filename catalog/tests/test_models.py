from django.test import TestCase

class MyTestClass(TestCase):

    #全局设置
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("###setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)


from catalog.models import Author
class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Big',last_name='Bob')
        pass

    def test_first_name_label(self):
       author = Author.objects.get(pk = 1) 
       field_label = author._meta.get_field('first_name').verbose_name 
       self.assertEquals(field_label,'first name')
       pass

    def test_date_of_death_label(self):
       author = Author.objects.get(id = 1)
       field_label = author._meta.get_field('date_of_death').verbose_name 
       self.assertEquals(field_label,'died')
       pass

    def test_first_name_max_length(self):
       author = Author.objects.get(id = 1)
       max_length = author._meta.get_field('date_of_death').max_length
       self.assertEquals(max_length,100)
       pass

    def test_object_name_is_last_name_comma_first_name(self):
       author = Author.objects.get(id = 1)
       expected_object_name = '%s,%s'%(author.last_name,author.first_name)
       self.assertEquals(expected_object_name,str(author))
       pass

    def test_get_absulte_url(self):
       author = Author.objects.get(id = 1)
       self.assertEquals(author.test_get_absulte_url(),'/catalog/author/1')

      
from django.utils import timezone
import datetime
from catalog.forms import RenewBookForm 

class RenewBookFormTest(TestCase):

    def test_renew_form_date_field_label(self):
        form = RenewBookForm()        
        self.assertTrue(form.fields['renewal_date'].label == None or form.fields['renewal_date'].label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEqual(form.fields['renewal_date'].help_text,'Enter a date between now and 4 weeks (default 3).')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_renew_form_date_max(self):
        date = timezone.now() + datetime.timedelta(weeks=4)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertTrue(form.is_valid())
    

