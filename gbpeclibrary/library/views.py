from django.shortcuts import render
from .forms import AuthorForm, StudentForm, BookForm, IssueForm , ReturnForm,BookNameForm,BookDepForm,StudentNameForm,StudentDepForm,FineForm,BookBankForm,ReissueForm
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Student, Author, Book, Quantity, LastFiveIssues,Publisher
import datetime
from datetime import timedelta
from django.shortcuts import get_object_or_404,Http404
from django.db.models import Count
from django.core.mail import send_mail
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth import authenticate
from django.contrib.auth import login as log
from django.contrib.auth import logout as loggedout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def main(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	else:
	
		#No of books issued today
		issuedtoday=len(Book.objects.filter(date_of_issue = datetime.date.today()))
	
		#No of books returned today
		list_of_books=Book.objects.all()
		returnedtoday=0
		for book in list_of_books:
			lfi=book.last_five_issues
			if lfi.return_one_date == datetime.date.today():
				returnedtoday=returnedtoday+1
		
		#Total fine pending.
		all_students=Student.objects.all()
		fine=0
		for student in all_students:
			if student.due_fine > 0:
				fine=fine+student.due_fine

		#New books added in past 30 days.

		since=datetime.date.today()-timedelta(days=30)
		books=Book.objects.filter(book_added_on__gte= since).values_list('book_name').distinct()

		#for pagination of new books
		paginator=Paginator(books,10)
		page=request.GET.get('page')
		try:
			books=paginator.page(page)
		except PageNotAnInteger:
			books=paginator.page(1)
		except EmptyPage:
			books=paginator.page(paginator.num_pages)


		return render(request,'base.html',{'returned':returnedtoday,'issued':issuedtoday,'fine':fine,'newbooks':books})
	
def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				log(request,user)
				return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/login')

	return render(request,'login.html',{})

@login_required
def logout(request):
	loggedout(request)
	return HttpResponseRedirect('/')

@login_required
def addBook(request):
    if not request.user.is_staff:
    	raise Http404

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
	#print(request.POST)
	form = BookForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
        	bookname = form.cleaned_data.get('book_name')
		bookid = form.cleaned_data.get('book_id')
		depbook= form.cleaned_data.get('dep_book')
		placedatshelf= form.cleaned_data.get('placed_at_shelf')
		edition=form.cleaned_data.get('edition_of_book')
        	studentrollnumber = '03720902713'	#form.cleaned_data.get('studentRollNumber')
        	pubbook=form.cleaned_data.get('publisherbook')
		if not Publisher.objects.filter(pk=pubbook).exists():
			pubbook=Publisher.objects.create(publisher_name=pubbook)
			pubbook.save()
		pubbook=Publisher.objects.get(pk=pubbook)

		authorname = form.cleaned_data.get('authorName')
        	authorname=str(authorname)
		authorname=(authorname.split(","))
		auth=[]
		for author in authorname:
			if author[0]==' ':
				author=author[1:]
			if not Author.objects.filter(pk=author).exists():
				z=(Author(author_name=author))
				auth.append(z)
				z.save()
			else:
				auth.append(Author.objects.get(pk=author))
# here we have a list of Author objects in auth[]	
		candidate_authors=Quantity.objects.annotate(c=Count('list_of_authors')).filter(c=len(auth))
		for author in auth:
			candidate_authors = candidate_authors.filter(list_of_authors=author,book_name=bookname)
		final_authors = candidate_authors
		if(len(final_authors)==0):
			f_authors=Quantity.objects.create()
			f_authors.book_name=bookname
			for ak in auth:
				f_authors.list_of_authors.add(ak)
				f_authors.save()
		else:
			f_authors=final_authors[0]
			f_authors.qty+=1
			f_authors.save()

		lfi=LastFiveIssues.objects.create()
		lfi.save()

        	s = get_object_or_404(Student,roll_number = studentrollnumber)
	#	print(a)
		bao=datetime.date.today()	
		b = Book(book_id=bookid,dep_book=depbook, book_name=bookname, placed_at_shelf=placedatshelf,edition_of_book=edition,student=s,authors=f_authors,last_five_issues=lfi,publisher_book=pubbook,book_added_on=bao)
		b.save()
		qtt=b.authors
		auths_b=qtt.list_of_authors.all()
		pub_b=b.publisher_book
        	return render(request,'addBook.html',{'book_added':True,'b':b,'auths':auths_b,'pub':pub_b})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = BookForm()
   	return render(request, 'addBook.html', {'form': form})


@login_required	
def addAuthor(request):
	if not request.user.is_staff:
		raise Http404

	if request.method=='POST':
		form = AuthorForm(request.POST)
		if form.is_valid():
			authname=form.cleaned_data.get('author_name')
			a = Author(author_name=authname)
			a.save()
			messages.success(request,'Author added successfully!')
			return HttpResponseRedirect('/addAuthor')
		else:
			messages.success(request,'Author addition failed!')
			return HttpResponseRedirect('/addAuthor')
	else:
		form = AuthorForm()
		return render(request,'addAuthor.html',{'form':form})



def addStudent(request):

	if request.method=='POST':
		form = StudentForm(request.POST,request.FILES) 
		print('here')
		if form.is_valid():
			rno=form.cleaned_data.get('roll_number')
			stname=form.cleaned_data.get('student_name')
			br=form.cleaned_data.get('branch')
			sem=form.cleaned_data.get('sem')
			dp=form.cleaned_data.get('pic')
			email=form.cleaned_data.get('email')
			passw=request.POST.get('password')
			cpassw=request.POST.get('cpassword')
			username=form.cleaned_data.get('username')
			if passw!=cpassw:
				cform=StudentForm()
				return render(request,'addStudent.html',{'form':cform})
			s=Student(roll_number=rno,student_name=stname,branch=br,sem=sem,pic=dp,email=email,username=username)
			s.set_password(passw)
			s.save()
			return render(request,'addStudent.html',{'s':s})
		else:
			return render(request,'addStudent.html',{'failed':True})
	else:
		form=StudentForm()
		return render(request,'addStudent.html',{'form':form})


@login_required
def deleteBook(request):
	if not request.user.is_staff:
		raise Http404
	if request.method=='POST':
		form = ReturnForm(request.POST)
		print('delete')
		if form.is_valid():
			code = form.cleaned_data.get('idi')
			b = get_object_or_404(Book,pk=code)
			print(b)
			qty=b.authors
			qty.qty-=1
			qty.save()
			b.delete()
			return render(request,'deleteBook.html',{'deleted':True})
	else:
		form = ReturnForm()
		return render(request,'deleteBook.html',{'form':form})


@login_required
def deleteAuthor(request):
	if not request.user.is_staff:
		raise Http404

	if request.method=='POST':
		f=request.POST.get('author_name')
		a=get_object_or_404(Author,pk=f)
		a.delete()
		return render(request,'deleteAuthor.html',{'deleted':True})
	else:
		form=AuthorForm()
		return render(request,'deleteAuthor.html',{'form':form})


@login_required
def deleteStudent(request):
	if not request.user.is_staff:
		raise Http404

	if request.method=='POST':
		form=IssueForm(request.POST)
		if form.is_valid():
			rno = form.cleaned_data.get('r_no')
			print(rno)
			s=get_object_or_404(Student,roll_number=rno)
			s.delete()
			return render(request,'deleteStudent.html',{'deleted':True})
	else:
		form=IssueForm()
		return render(request,'deleteStudent.html',{'form':form})




@login_required
def issue(request):
	if not request.user.is_staff:
		raise Http404

#gets called for issuing the book.
	if request.method=='POST':
		form = IssueForm(request.POST)
		if form.is_valid():
			bar_code = request.POST.get('bar_code')
			roll_number = form.cleaned_data.get('r_no')
			print bar_code,roll_number
			b = get_object_or_404(Book,pk=bar_code)
			s = get_object_or_404(Student,roll_number=roll_number)
		
			#check max books issuing limit
			if s.no_of_books_issued==4:
				return render(request,'Issue.html',{'limit':True}) #modify html

			#check if book is claimed by someone.
			if b.claim_one!='':
				print "i am claimed"
				if roll_number!=b.claim_one:
					d1=datetime.date.today()
					d2=b.last_five_issues.return_one_date
					delta=d1-d2
					if delta.days >=2:
						b.claim_one=''
						b.save()
					else:
						return render(request,'Issue.html',{'claim':True}) #handle this in html.
				else:
					b.claim_one=''
					b.save()
			
			if not b.is_issued:
				b.is_issued=True
				b.student=s
				b.date_of_issue= datetime.date.today()
				b.return_date= datetime.date.today()+timedelta(days=30)
				b.save()
				s.no_of_books_issued+=1;
				s.save()
				return render(request,'Issue.html',{'issued':True,'b':b,'s':s})
	return render(request,'Issue.html',{'cannot_be_issued':True})





@login_required
def bookSearch(request):
	if request.method=='POST':
#	print('hulla')
		idform=ReturnForm(request.POST)
		nameform = BookNameForm(request.POST)
		depform=BookDepForm(request.POST)
		if idform.is_valid():
			code=idform.cleaned_data.get('idi')
			b=get_object_or_404(Book,pk=code)
			qty=b.authors
			auths=qty.list_of_authors.all()
			pub=b.publisher_book
			lfi=b.last_five_issues
			return render(request,'bookSearch.html',{'book':b,'qty':qty,'auths':auths,'pub':pub,'lfi':lfi})
		#print(nameform)
		if nameform.is_valid():
			name=nameform.cleaned_data.get('book_name')
			qb=Quantity.objects.filter(book_name__icontains=name)
			listoftuple=[]
			for q in qb:
				x=q.book_name
				y=q.qty
				z=q.list_of_authors.all()
				list_books=q.book_set.all()
				count=0
				for bks in list_books:
					if not bks.is_issued:
						count=count+1
				tup=(x,y,z,count,q.q_id)
				listoftuple.append(tup)
			
				
			return render(request,'bookSearch.html',{'list':listoftuple})
		if depform.is_valid():
			code=depform.cleaned_data.get('dep_book')
			b=Book.objects.filter(dep_book__iexact=code).values_list('book_name').distinct()
			listofbooks=[]
			for foo in b:
				listofbooks.append(foo[0])
			return render(request,'bookSearch.html',{'listb':listofbooks})
		else:
			return render(request,'bookSearch.html',{'no_book':True})

	else:
		idform = ReturnForm()
		nameform = BookNameForm()
		depform = BookDepForm() 
		return render(request,'bookSearch.html',{'idform':idform,'nameform':nameform,'depform':depform})



@login_required
def authorSearch(request):
	if request.method=='POST':
		f=request.POST.get('author_name')
		a=Author.objects.filter(author_name__icontains=f)
		list_auth=[]
		for foo in a:
			books=foo.quantity_set.all()	
			list_auth.append((foo,books))
		return render(request,'authorSearch.html',{'list_auth':list_auth})
	else:
		form = AuthorForm()
		return render(request,'authorSearch.html',{'form':form})



@login_required
def studentSearch(request):
	if request.method=='POST':
		idform = IssueForm(request.POST)
		depform=StudentDepForm(request.POST)
		nameform=StudentNameForm(request.POST)
		if idform.is_valid():
			code=idform.cleaned_data.get('r_no')
			s=get_object_or_404(Student,roll_number=code)
			books=s.book_set.all()
			return render(request,'studentSearch.html',{'s':s,'books':books})
		if depform.is_valid():
			sem=depform.cleaned_data.get('sem')
			dep=depform.cleaned_data.get('dep_book')
			s=Student.objects.filter(branch__iexact=dep,sem=sem).order_by('roll_number')
			s_list=[]
			for st in s:
				bk=st.book_set.all()
				s_list.append((st,bk))
			return render(request,'studentSearch.html',{'s_dep':s_list})	
		if nameform.is_valid():
			name=nameform.cleaned_data.get('student_name')
			students=Student.objects.filter(student_name__icontains=name).order_by('roll_number')
			list_st=[]
			for s in students:
				books=s.book_set.all()
				list_st.append((s,books))
			return render(request,'studentSearch.html',{'list_st':list_st})
		else:
			return HttpResponse('<h1>Please fill atleast one field.</h1>')
	else:
		idform = IssueForm()
		depform=StudentDepForm()
		nameform=StudentNameForm()
		return render(request,'studentSearch.html',{'idform':idform,'depform':depform,'nameform':nameform})
		


@login_required
def issueReturn(request):
	if not request.user.is_staff:
		raise Http404

	if request.method=='POST':
		form = ReturnForm(request.POST)
		if form.is_valid():
			code = form.cleaned_data.get('idi')
			b = get_object_or_404(Book,pk=code)
			print type(b)
			if b.is_issued:
				print 'blah'
				d1= datetime.date.today()
				d2= b.return_date
				delta = d1 - d2
				s=b.student
				if delta.days>0 :
					x=s.due_fine+long(delta.days)
					s.due_fine=x
					s.save()
				#setting up last five issues
				lfi=b.last_five_issues
			
				lfi.five_st=lfi.four_st
				lfi.four_st=lfi.three_st
				lfi.three_st=lfi.two_st
				lfi.two_st=lfi.one_st
				lfi.one_st=b.student.roll_number

				lfi.issue_five_date=lfi.issue_four_date
				lfi.issue_four_date=lfi.issue_three_date
				lfi.issue_three_date=lfi.issue_two_date
				lfi.issue_two_date=lfi.issue_one_date
				lfi.issue_one_date=b.date_of_issue

				lfi.return_five_date=lfi.return_four_date
				lfi.return_four_date=lfi.return_three_date
				lfi.return_three_date=lfi.return_two_date
				lfi.return_two_date=lfi.return_one_date
				lfi.return_one_date=datetime.date.today()

				lfi.save()
				b.is_issued=False
				b.student=get_object_or_404(Student,roll_number='03720902713')
				doi=b.date_of_issue
				rd=b.return_date
				b.date_of_issue=datetime.date(1900,1,1)
				b.return_date=datetime.date(1900,1,1)
				b.times_issued=0
				b.save()
				s.no_of_books_issued-=1
				s.save()
				delta=delta.days
				if delta<0:
					delta=0
				if b.claim_one!='':
					claim=get_object_or_404(Student,roll_number=b.claim_one)
					message='Book with id :'+str(b.book_id)+' is now available in the library. Please Issue it by '+str(datetime.date.today()+timedelta(days=1))+' or else it will be made available for anyone to issue.'
					send_mail('GBPEC LIBRARY', message, 'akash.tomar217@yahoo.com',[claim.email,], fail_silently=False)

	
				return render(request,'Issue.html',{'returned':True,'doi':doi,'rd':rd,'b':b,'fine':delta,'s':s})
			else:
				f = IssueForm()
				return render(request,'Issue.html',{'bar_code':code,'issueForm':f})
	else:
		form = ReturnForm()
		return render(request,'issuereturn.html',{'form':form})




@login_required
def fine(request):
	if not request.user.is_staff:
		raise Http404

	if request.method=='POST':
		form=IssueForm(request.POST)
		fineform=FineForm(request.POST)
		if form.is_valid():
			rno=form.cleaned_data.get('r_no')
			s=get_object_or_404(Student,roll_number=rno)
			f=FineForm()
			return render(request,'fine.html',{'s':s,'fineform':f})
		if fineform.is_valid():
			fine=fineform.cleaned_data.get('fine')
			s=request.POST.get('student')
			st=get_object_or_404(Student,pk=s)
			st.due_fine-=fine
			st.save()
			return render(request,'fine.html',{'st':st})
	else:
		form=IssueForm()
		return render(request,'fine.html',{'form':form})




@login_required
def bookbank(request):
	if not request.user.is_staff:
		raise Http404

	if request.method=='POST':
		form=BookBankForm(request.POST)
		if form.is_valid():
			code=form.cleaned_data.get('code')
			rno=form.cleaned_data.get('rno')
			b=Book.objects.get(pk=code)
			s=Student.objects.get(roll_number=rno)
			if b.is_issued:
				return render(request,'bookbank.html',{'is_issued':True,'name':s.student_name})
			b.student=s
			b.date_of_issue= datetime.date.today()
			b.return_date= datetime.date.today()+timedelta(days=30*6)
			b.is_issued=True
			b.save()
			
			#setting up last five issues
			lfi=b.last_five_issues
			
			lfi.five_st=lfi.four_st
			lfi.four_st=lfi.three_st
			lfi.three_st=lfi.two_st
			lfi.two_st=lfi.one_st
			lfi.one_st=s.roll_number

			lfi.issue_five_date=lfi.issue_four_date
			lfi.issue_four_date=lfi.issue_three_date
			lfi.issue_three_date=lfi.issue_two_date
			lfi.issue_two_date=lfi.issue_one_date
			lfi.issue_one_date=b.date_of_issue

			lfi.return_five_date=lfi.return_four_date
			lfi.return_four_date=lfi.return_three_date
			lfi.return_three_date=lfi.return_two_date
			lfi.return_two_date=lfi.return_one_date
			lfi.return_one_date=b.return_date

			lfi.save()
			s.save()
			return render(request,'bookbank.html',{'bookbank':True,'b':b,'s':s})
			
			
	else:
		form=BookBankForm()
		return render(request,'bookbank.html',{'form':form})


@login_required
def email(request):
	if not request.user.is_staff:
		raise Http404

	s=Student.objects.all()
	count=0
	for stud in s:
		books=stud.book_set.all()
		for b in books:
			if b.is_issued:
				d1=datetime.date.today()
				d2=b.return_date
				delta=d1-d2
				message='Your book '+str(b.book_name)+' is due to be returned on '+str(b.return_date)+'. Please return on time to avoid additional fines.'
				if delta.days>=-2 :
					send_mail('GBPEC LIBRARY', message, 'akash.tomar217@yahoo.com',[stud.email,], fail_silently=False)
					count=count+1
				if delta.days==-2:
					message1='The book with id :'+str(b.book_id)+' will be returned in the library on '+str(b.return_date)+'. Contact librarian for further assistance.'
					claim=get_object_or_404(Student,roll_number=b.claim_one)
					print message,claim.email
					send_mail('GBPEC LIBRARY',message1,'akash.tomar217@yahoo.com',[claim.email,],fail_silently=False)
					count+=1
	return render(request,'email.html',{'count':count})



@login_required
def allbooks(request):
	books=Quantity.objects.all()
	paginator=Paginator(books,10)
	page=request.GET.get('page')

	try:
		book=paginator.page(page)
	except PageNotAnInteger:
		book=paginator.page(1)
	except EmptyPage:
		book=paginator.page(paginator.num_pages)
	
	listoftuple=[]
	for q in book:
		x=q.book_name
		y=q.qty
		z=q.list_of_authors.all()
		list_books=q.book_set.all()
		count=0
		for bks in list_books:
			if not bks.is_issued:
				count=count+1
		tup=(x,y,z,count)
		listoftuple.append(tup)

	return render(request,'allbooks.html',{'books':listoftuple,'b':book})





@login_required
def reissue(request):
	if request.method=='POST':
		form = ReissueForm(request.POST)
		if form.is_valid():
			bar_code = form.cleaned_data.get('code')
			roll_number=request.user.roll_number
			b = get_object_or_404(Book,pk=bar_code)
			if  b.is_issued:
				s=get_object_or_404(Student,roll_number=roll_number)
				if s == b.student and b.times_issued<2:
					d1= datetime.date.today()
					d2= b.return_date
					delta = d1 - d2
					if delta.days>0 :
						x=s.due_fine+long(delta.days)
						s.due_fine=x
						s.save()
				#setting up last five issues
					lfi=b.last_five_issues
			
					lfi.five_st=lfi.four_st
					lfi.four_st=lfi.three_st
					lfi.three_st=lfi.two_st
					lfi.two_st=lfi.one_st
					lfi.one_st=b.student.roll_number

					lfi.issue_five_date=lfi.issue_four_date
					lfi.issue_four_date=lfi.issue_three_date
					lfi.issue_three_date=lfi.issue_two_date
					lfi.issue_two_date=lfi.issue_one_date
					lfi.issue_one_date=b.date_of_issue
		
					lfi.return_five_date=lfi.return_four_date
					lfi.return_four_date=lfi.return_three_date
					lfi.return_three_date=lfi.return_two_date
					lfi.return_two_date=lfi.return_one_date
					lfi.return_one_date=datetime.date.today()

					lfi.save()
					doi=b.date_of_issue
					rd=b.return_date
				
					b.date_of_issue= datetime.date.today()
					b.return_date= datetime.date.today()+timedelta(days=30)
					b.times_issued+=1
					b.save()
					
					delta=delta.days
					if delta<0:
						delta=0

					return render(request,'reissue.html',{'reissued':True,'b':b,'fine':delta})
				else:
					return render(request,'reissue.html',{'reissued':False})

			else:
				return render(request,'reissue.html',{'reissued':False})
	else:
		form = ReissueForm()
		return render(request,'reissue.html',{'form':form})



def claim(request):
	if request.method=='POST':
		q_id=request.POST.get('q_id')
		book_id=request.POST.get('book_id')	
		if q_id:
			book=get_object_or_404(Quantity,pk=q_id)
			books=book.book_set.all()
			
			#if book is available no need to claim it.
			for book in books:
				if not book.is_issued:
					return render(request,'claim.html',{'available':True})

			#since all books are issued.
			lists=[]
			for book in books:
				lists.append((book,book.return_date))
				#if book.return_date < ret_date:
#					ret_date=book.return_date
#					z=book
			lists=sorted(lists,key=lambda z:z[1])
			while len(lists)!=0:
				z=lists.pop(0)
				z=z[0]
				if z.claim_one == '':
					z.claim_one=request.user.roll_number
					z.save()
					message='Book with id :'+str(z.book_id)+' has been claimed by you. We will notify you again before 2 days of book return date.'
					send_mail('GBPEC LIBRARY', message, 'akash.tomar217@yahoo.com',[request.user.email,], fail_silently=False)

					return render(request,'claim.html',{'claim':True})
				
				#Only one claim being allowed.
				'''elif z.claim_two == '':
					z.claim_two = request.user.roll_number
					z.save()					
					return render(request,'claim.html',{'no_claim':False})
	
				elif z.claim_three=='':
					z.claim_three=request.user.roll_number
					z.save()
					return render(request,'claim.html',{'no_claim':False})'''

			return render(request,'claim.html',{'no_claim':True})	

		if book_id:
			b=get_object_or_404(Book,pk=book_id)
			print b.claim_one,b.claim_two,b.claim_three
			if b.claim_one == '':
				b.claim_one=request.user.roll_number
				b.save()
				return render(request,'claim.html',{'claim':True})
			
			#only one claim being allowed.
			'''elif b.claim_two == '':
				b.claim_two = request.user.roll_number
				b.save()
			elif b.claim_three=='':
				print "here"
				b.claim_three=request.user.roll_number
				print request.user.roll_number
				b.save()'''
		
			return render(request,'claim.html',{'no_claim':True})

def profile(request):
	if request.user.is_authenticated():
		rno=request.user.roll_number
		s=get_object_or_404(Student,roll_number=rno)
		books=s.book_set.all()
		return render(request,'profile.html',{'s':s,'books':books})

def signup(request):
	if request.method=='POST':
		form = StudentForm(request.POST,request.FILES) 
		print('here')
		if form.is_valid():
			rno=form.cleaned_data.get('roll_number')
			stname=form.cleaned_data.get('student_name')
			br=form.cleaned_data.get('branch')
			sem=form.cleaned_data.get('sem')
			dp=form.cleaned_data.get('pic')
			email=form.cleaned_data.get('email')
			passw=request.POST.get('password')
			cpassw=request.POST.get('cpassword')
			username=form.cleaned_data.get('username')
			if passw!=cpassw:
				cform=StudentForm()
				return render(request,'addStudent.html',{'form':cform})
			s=Student(roll_number=rno,student_name=stname,branch=br,sem=sem,pic=dp,email=email,username=username)
			s.set_password(passw)
			s.is_active=True
			s.save()
			return HttpResponseRedirect('/')	
		else:
			return render(request,'signup.html',{'failed':True})
	else:
		form=StudentForm()
		return render(request,'signup.html',{'form':form})

