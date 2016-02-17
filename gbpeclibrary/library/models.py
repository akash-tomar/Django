# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Student(AbstractUser):
	roll_number = models.CharField(max_length=30,unique=True)
	student_name = models.CharField(max_length=200)
	branch = models.CharField(max_length=20)
	sem = models.IntegerField(default=1)
	pic = models.ImageField(null=True,blank=True)
	due_fine = models.IntegerField(default=0)
	USERNAME_FIELD='roll_number'
	REQUIRED_FIELDS=['username','email']

	#additional fields
	phone = PhoneNumberField(null=True, blank=True, help_text=('Only Indian'))
	dob = models.DateField(blank=True,null=True)
	no_of_books_issued=models.IntegerField(default=0)
	no_of_books_book_bank=models.IntegerField(default=0)
	address=models.CharField(max_length=500,blank=True,null=True)
	claimed=models.BooleanField(default=False)
	def __str__(self):
		return self.student_name

class Author(models.Model):
	author_name = models.CharField(max_length=200,primary_key=True)
	def __str__(self):
		return self.author_name


class Quantity(models.Model):
	q_id=models.AutoField(primary_key=True)
	book_name=models.CharField(max_length=200)
	list_of_authors=models.ManyToManyField(Author)
	qty = models.IntegerField(default=1)
	class Meta:
		verbose_name_plural = 'Quantity'
#		unique_together=(('book_name','list_of_authors'),)
	def __str__(self):
		return self.book_name

class LastFiveIssues(models.Model):
	lfi_id=models.AutoField(primary_key=True)
	one_st=models.CharField(max_length=30,blank=True,null=True)
	two_st=models.CharField(max_length=30,blank=True,null=True)
	three_st=models.CharField(max_length=30,blank=True,null=True)
	four_st=models.CharField(max_length=30,blank=True,null=True)
	five_st=models.CharField(max_length=30,blank=True,null=True)
	issue_one_date=models.DateField(blank=True,null=True)
	issue_two_date=models.DateField(blank=True,null=True)
	issue_three_date=models.DateField(blank=True,null=True)
	issue_four_date=models.DateField(blank=True,null=True)
	issue_five_date=models.DateField(blank=True,null=True)
	return_one_date=models.DateField(blank=True,null=True)
	return_two_date=models.DateField(blank=True,null=True)
	return_three_date=models.DateField(blank=True,null=True)
	return_four_date=models.DateField(blank=True,null=True)
	return_five_date=models.DateField(blank=True,null=True)
	class Meta:
		verbose_name_plural='last five issues'
		
class Publisher(models.Model):
	publisher_name = models.CharField(max_length=200,primary_key=True)
	def __str__(self):
		return self.publisher_name



class Book(models.Model):
	
	last_five_issues=models.OneToOneField(LastFiveIssues)
	publisher_book=models.ForeignKey(Publisher)
	authors = models.ForeignKey(Quantity)
	student = models.ForeignKey(Student)
	
	book_id = models.CharField(primary_key=True,max_length=30)
	is_issued = models.BooleanField(default=False)
	dep_book = models.CharField(max_length=20)
	book_name = models.CharField(max_length=200)
	date_of_issue = models.DateField(default = '1900-1-1')
	return_date = models.DateField(default='1900-1-1')
	book_added_on = models.DateField(default='1900-1-1')
	placed_at_shelf=models.CharField(max_length=200,blank=True,null=True)
	edition_of_book = models.IntegerField()
	
	#new features
	rare_book = models.BooleanField(default=False)
	
	claim_one=models.CharField(max_length=30,blank=True,null=True)
	claim_two=models.CharField(max_length=30,blank=True,null=True)
	claim_three=models.CharField(max_length=30,blank=True,null=True)
	
	total_no_of_times_issued=models.IntegerField(default=0)
	times_issued=models.IntegerField(default=0) # no of times issued to a single child in a row.



	def __str__(self):
		return self.book_name


