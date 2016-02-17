from django import forms
from .models import Author,Book,Student,Quantity,LastFiveIssues,Publisher
from django.contrib.auth.models import User
import django.contrib.auth
from phonenumber_field.modelfields import PhoneNumberField

class AuthorForm(forms.ModelForm):
	class Meta:
		model = Author
		fields = ['author_name',]
	def __init__(self,*args,**kwargs):
		super(AuthorForm,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
			'class':'form-control'})
		self.fields['author_name'].widget.attrs.update({'placeholder':'Name of the Author','autofocus':'autofocus'})

class ProfileForm(forms.ModelForm):
	phone=PhoneNumberField(null=True,blank=True,help_text=('OnlyIndian'))
	address=forms.CharField(max_length=500)
	class Meta:
		model=Student
		fields=['roll_number','student_name','branch','sem','email']
	def __init__(self,*args,**kwargs):
		super(ProfileForm,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
			'class':'form-control'})
		self.fields['roll_number'].widget.attrs.update({'placeholder':'Roll Number','autofocus':'autofocus'})
		self.fields['student_name'].widget.attrs.update({'placeholder':'Name of the student'})
		self.fields['branch'].widget.attrs.update({'placeholder':'Branch'})
		self.fields['sem'].widget.attrs.update({'placeholder':'Semester'})
		self.fields['email'].widget.attrs.update({'placeholder':'Email'})
		self.fields['phone'].widget.attrs.update({'placeholder':'Phone Number'})
		self.fields['address'].widget.attrs.update({'placeholder':'Address'})
		






class StudentForm(forms.ModelForm):
#	password=forms.CharField(widget=forms.PasswordInput())
#	cpassword=forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model=Student
		fields=['roll_number','student_name','branch','sem','email','username']
	def __init__(self,*args,**kwargs):
		super(StudentForm,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
			'class':'form-control'})
		self.fields['roll_number'].widget.attrs.update({'placeholder':'Roll Number','autofocus':'autofocus'})
		self.fields['student_name'].widget.attrs.update({'placeholder':'Name of the student'})
		self.fields['branch'].widget.attrs.update({'placeholder':'Branch'})
		self.fields['sem'].widget.attrs.update({'placeholder':'Semester'})
		self.fields['email'].widget.attrs.update({'placeholder':'Email'})
		self.fields['username'].widget.attrs.update({'placeholder':'Username'})







class BookForm(forms.ModelForm):
	#studentRollNumber = forms.CharField(max_length=100)
	authorName = forms.CharField(max_length=100)
	publisherbook=forms.CharField(max_length=100)
	class Meta:
		model = Book
		fields = ['book_id','book_name','dep_book','placed_at_shelf','edition_of_book']
	def __init__(self,*args,**kwargs):
		super(BookForm,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
			})
#self.fields['authorName'].widget.attrs.update({'placeholder':'Name Of the Author'})
		self.fields['book_id'].widget.attrs.update({'placeholder':'Scan Bar Code'})
		self.fields['book_name'].widget.attrs.update({'placeholder':'Name of the Book','autofocus':'autofocus'})
		self.fields['dep_book'].widget.attrs.update({'placeholder':'Department Name'})
		self.fields['publisherbook'].widget.attrs.update({'placeholder':'Publisher Name'})
		self.fields['placed_at_shelf'].widget.attrs.update({'placeholder':'Shelf Address'})
		self.fields['edition_of_book'].widget.attrs.update({'placeholder':'Edition Of The Book'})
		self.fields['authorName'].widget.attrs.update({'placeholder':'List of authors Eg. Peter Linz, Gabreich'})


class ReturnForm(forms.Form):
	idi = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
	def __init__(self,*args,**kwargs):
		super(ReturnForm,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
			})
		self.fields['idi'].widget.attrs.update({'placeholder':'Scan Bar Code'})



class IssueForm(forms.Form):
	r_no = forms.CharField(max_length = 20 )
	def __init__(self,*args,**kwargs):
		super(IssueForm,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
			})
		self.fields['r_no'].widget.attrs.update({'placeholder':'Roll Number','autofocus':'autofocus'})

class BookNameForm(forms.ModelForm):
	class Meta:
		model=Book
		fields=['book_name']
	def __init__(self,*args,**kwargs):
		super(BookNameForm,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
			})
		self.fields['book_name'].widget.attrs.update({'placeholder':'Book Name','autofocus':'autofocus'})


class BookDepForm(forms.ModelForm):
	class Meta:
		model=Book
		fields=['dep_book']
	def __init__(self,*args,**kwargs):
		super(BookDepForm,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
			})
		self.fields['dep_book'].widget.attrs.update({'placeholder':'Department Eg. CSE,MAE or ECE','autofocus':'autofocus'})


class StudentDepForm(forms.ModelForm):
	sem=forms.IntegerField()
	class Meta:
		model=Book
		fields=['dep_book']
	def __init__(self,*args,**kwargs):
		super(StudentDepForm,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
			})
		self.fields['dep_book'].widget.attrs.update({'placeholder':'Department Eg. CSE,MAE or ECE','autofocus':'autofocus'})
		self.fields['sem'].widget.attrs.update({'placeholder':'Semester'})


class StudentNameForm(forms.ModelForm):
	class Meta:
		model=Student
		fields=['student_name']
	def __init__(self,*args,**kwargs):
		super(StudentNameForm,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
			})
		self.fields['student_name'].widget.attrs.update({'placeholder':'Student Name'})


class FineForm(forms.Form):
	fine=forms.IntegerField()
	def __init__(self,*args,**kwargs):
		super(FineForm,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
			})
		self.fields['fine'].widget.attrs.update({'placeholder':'Fine Paid'})


class BookBankForm(forms.Form):
	code=forms.CharField(max_length=30)
	rno=forms.CharField(max_length=30)
	def __init__(self,*args,**kwargs):
		super(BookBankForm,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
			})
		self.fields['code'].widget.attrs.update({'placeholder':'Scan Bar Code'})
		self.fields['rno'].widget.attrs.update({'placeholder':'Roll Number','autofocus':'autofocus'})


class LoginForm(forms.Form):
	username=forms.CharField(max_length=30)
	password=forms.CharField(max_length=30,widget=forms.PasswordInput())
	def __init__(self,*args,**kwargs):
		super(LoginForm,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
			})
		self.fields['username'].widget.attrs.update({'placeholder':'Username'})
		self.fields['password'].widget.attrs.update({'placeholder':'Password'})


class ReissueForm(forms.Form):
	code = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
	def __init__(self,*args,**kwargs):
		super(ReissueForm,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
			})
		self.fields['code'].widget.attrs.update({'placeholder':'Bar Code'})


