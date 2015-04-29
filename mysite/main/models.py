from django.db import models
from django import forms
from pymodbus.client.sync import ModbusTcpClient
import datetime
from django.utils.timezone import utc
import ldap
import ldap.filter
from django.forms.models import modelform_factory
# Create your models here.

class Group(models.Model):
	titel = models.CharField(max_length = 20)
	def __unicode__(self):
		return '%s ' %(self.titel) 
class Function(models.Model):
	titel		= models.CharField(max_length = 20)
	bos_function = models.BooleanField( blank = True)
	id_group	= models.ForeignKey(Group, blank = True, null =True)
	def __unicode__(self):
		return '%s  %s' %(self.titel, self.id_group) 

class User(models.Model):
	login		= models.CharField(max_length = 10, primary_key=True)
	first_name	= models.CharField(max_length = 20, null = True, blank = True)
	second_name	= models.CharField(max_length = 20, null = True, blank = True)
	patronymic	= models.CharField(max_length = 20, null = True, blank = True)
	id_function = models.ForeignKey(Function, blank = True, null =True)	
	email 		= models.EmailField( max_length=254,  null = True, blank = True)
	phone_work 	= models.IntegerField(null = True, blank = True)
	phone_mob 	= models.BigIntegerField(null = True, blank = True)
	admin_prava = models.BooleanField( blank = True)
	avatar 		= models.ImageField(verbose_name='put', upload_to = 'users/' , null = True, blank = True)
	
	def __unicode__(self):
		return '%s' %(self.login) 
	def save(self, force_insert=False, force_update=False, using=None):
		try:
			obj =  User.objects.get(login=self.login)
			if obj.avatar.path != self.avatar.path:
				obj.avatar.delete()
		except:
			pass
		super(User, self).save()
	def delete(self, using=None):
		try:
			obj = User.objects.get(login=self.login)
			obj.avatar.delete()
		except (User.DoesNotExist, ValueError):
			pass
		super(User, self).delete()

class Documents(models.Model):
	titel 		 = models.CharField(max_length = 200)
	user_id 	 = models.ForeignKey(User, related_name='+')
	status 		 = models.IntegerField()
	versia 		 = models.CharField(max_length = 20)
	id_versia 	 = models.BigIntegerField()
	date 		 = models.DateTimeField()
	update 		 = models.ForeignKey(User, related_name='+', null = True, blank = True)
	versia_final = models.BooleanField()
	file 		 = models.FileField(upload_to='documents/')
	def __unicode__(self):
		return '%s' %(self.titel) 

	

	
class DocumentUser(models.Model):
	user 	 = models.ForeignKey(User)
	document = models.ForeignKey(Documents)
	status 	 = models.IntegerField()

class DocumentGroup(models.Model):
	group = models.ForeignKey(Group)
	document = models.ForeignKey(Documents)
	status	 = models.IntegerField()



class Matching(models.Model):
	titel 			= models.CharField(max_length = 20, null = True, blank = True)
	id_creator		= models.ForeignKey(User, related_name='+')
	id_signatory	= models.ForeignKey(User, related_name='+', null = True, blank = True)
	specification	= models.TextField( null = True, blank = True)
	date 			= models.DateTimeField()
	date_end		= models.DateTimeField(null = True, blank = True)
	date_real_end	= models.DateTimeField(null = True, blank = True)
	status 			= models.IntegerField() 
class Matching_Document(models.Model):
	matching 	= models.ForeignKey(Matching)
	document	= models.ForeignKey(Documents)
class Matching_User(models.Model):
	matching 	= models.ForeignKey(Matching)
	user 		= models.ForeignKey(User)
	number 		= models.IntegerField() 
	status 		= models.IntegerField() 
class Comment_Matching(models.Model):
	matching 	= models.ForeignKey(Matching)
	user 		= models.ForeignKey(User)
	comemnt		= models.TextField()
	date 		= models.DateTimeField()

class FormProfile(forms.Form):
	def __init__(self, *args, **kwargs):
		if 'login' in kwargs:
			self.login = kwargs.pop('login')
			self.user  = User.objects.get(login = self.login)
			
		else:
			self.user = None
		
		super(FormProfile, self).__init__(*args, **kwargs)
		if self.user:
			try:
				self.fields['first_name'] 		= forms.CharField(initial = self.user.first_name, max_length = 20)
				self.fields['second_name'] 		= forms.CharField(initial = self.user.second_name, max_length = 20)
				self.fields['patronymic'] 		= forms.CharField(initial = self.user.patronymic, max_length = 20)
				self.fields['id_function'] 		= forms.ModelChoiceField(queryset= Function.objects.all() ,initial = self.user.id_function)
				self.fields['email'] 			= forms.EmailField(initial = self.user.email, max_length = 254)
				self.fields['phone_work_form'] 	= forms.IntegerField(initial = self.user.phone_work, min_value = 100 , max_value =999)
				self.fields['phone_mob_form'] 	= forms.IntegerField(initial = self.user.phone_mob, min_value = 89000000000, max_value = 89999999999)
				self.fields['admin_prava_form'] = forms.BooleanField(initial = self.user.admin_prava)
				self.fields['avatar'] 			= forms.ImageField()
				
			except:
				self.fields['first_name'] 		= forms.CharField( max_length = 20)
				self.fields['second_name'] 		= forms.CharField( max_length = 20)
				self.fields['patronymic'] 		= forms.CharField( max_length = 20)
				self.fields['id_function'] 		= forms.ModelChoiceField(queryset = Function.objects.all())
				self.fields['email'] 			= forms.EmailField( max_length = 254)
				self.fields['phone_work_form'] 	= forms.IntegerField( min_value = 100 , max_value =999)
				self.fields['phone_mob_form'] 	= forms.IntegerField( min_value = 89000000000, max_value = 89999999999)
				self.fields['admin_prava_form'] = forms.BooleanField()
				self.fields['avatar'] 			= forms.ImageField()
				
		else:
			self.fields['first_name'] 		= forms.CharField( max_length = 20)
			self.fields['second_name'] 		= forms.CharField( max_length = 20)
			self.fields['patronymic'] 		= forms.CharField( max_length = 20)
			self.fields['id_function'] 		= forms.ModelChoiceField(queryset = Function.objects.all())
			self.fields['email'] 			= forms.EmailField( max_length = 254)
			self.fields['phone_work_form'] 	= forms.IntegerField( min_value = 100 , max_value =999)
			self.fields['phone_mob_form'] 	= forms.IntegerField( min_value = 89000000000, max_value = 89999999999)
			self.fields['admin_prava_form'] = forms.BooleanField()
			self.fields['avatar'] 			= forms.ImageField()

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 254)
	password = forms.CharField( widget = forms.PasswordInput)

class UserForm(forms.Form):
	user 		= forms.ModelChoiceField(queryset = User.objects.all())
	status_user = forms.BooleanField()

class GroupForm(forms.Form):
	group = forms.ModelChoiceField(queryset = Group.objects.all())
	status_group = forms.BooleanField()

class DocumentForm(forms.Form):
	file = forms.FileField()	

class MatchingForm(forms.Form):
	def __init__(self, *args, **kwargs):
		if 'id' in kwargs:
			self.id = kwargs.pop('id')
			self.matching  = Matching.objects.get(id = self.id)

			
		else:
			self.matching = None
		
		super(MatchingForm, self).__init__(*args, **kwargs)
		if self.matching:
			try:
				self.fields['date']					= forms.DateTimeField(initial = self.matching.date, widget = forms.DateInput())
				self.fields['titel'] 				= forms.CharField(initial = self.matching.titel)
				self.fields['user_performer'] 		= forms.ModelChoiceField(queryset = User.objects.all(), initial =	Matching_User.objects.get(matching = self.matching, number = 1).user)
				self.fields['specification'] 		= forms.CharField(widget=forms.Textarea, initial = self.matching.specification)
				self.fields['user_signatory'] 		= forms.ModelChoiceField(queryset = User.objects.all(), initial = self.matching.id_signatory)
				
				
			except:
				self.fields['date']					= forms.DateTimeField(widget = forms.DateInput())
				self.fields['titel'] 				= forms.CharField()
				self.fields['user_performer'] 		= forms.ModelChoiceField(queryset = User.objects.all())
				self.fields['specification'] 		= forms.CharField(widget=forms.Textarea)
				self.fields['user_signatory'] 		= forms.ModelChoiceField(queryset = User.objects.all())
				
				
		else:
			self.fields['date']					= forms.DateTimeField(widget = forms.DateInput())
			self.fields['titel'] 				= forms.CharField()
			self.fields['user_performer'] 		= forms.ModelChoiceField(queryset = User.objects.all())
			self.fields['specification'] 		= forms.CharField(widget=forms.Textarea)
			self.fields['user_signatory'] 		= forms.ModelChoiceField(queryset = User.objects.all())
	
class MatchingUserForm(forms.Form):
	user = forms.ModelChoiceField(queryset = User.objects.all())


class Comment(forms.Form):		
	comment_user = forms.CharField(widget=forms.Textarea)



class MadelMain(models.Model):
	def save_user(self, login, first_name = None, second_name = None, patronymic = None, id_function = None, email = None, phone_mob = None, phone_work = None, avatar = None, admin_prava = True):
		user = User(login = login, first_name = first_name, second_name = second_name, patronymic = patronymic, id_function =  id_function, email = email, phone_work = phone_work, phone_mob = phone_mob, admin_prava = admin_prava)
		if avatar:
			user.avatar.save(avatar)
		user.save()
	def user_profile(self, login):

		user = User.objects.get(login = login)

		return user# [user.login, user.first_name, user.second_name, user.patronymic, user.id_function, user.email, user.phone_work, user.phone_mob, user.avatar]
	def all_user(self):
		return User.objects.all()
	def login_new(self, login):
		try:
			if User.objects.get(login = login):
				return False
		except:
			return True
	
	def save_first_name(self, login, first_name):
		User.objects.filter(login = login).update(first_name = first_name)
	def save_second_name(self, login, second_name):
		User.objects.filter(login = login).update(second_name =second_name)
	def save_patronymic(self, login, patronymic):
		User.objects.filter(login = login).update(patronymic = patronymic)
	def save_function(self, login, id_function):
		User.objects.filter(login = login).update(id_function =id_function)
	def save_email(self, login, email):
		User.objects.filter(login = login).update(email = email)
	def save_phone_mob(self, login, phone_mob):
		User.objects.filter(login = login).update(phone_mob = phone_mob)
	def save_phone_work(self, login, phone_work):
		User.objects.filter(login = login).update(phone_work = phone_work)
		if phone_work:
									user.phone_work = phone_work
									user.save()
	def save_avatar(self, login, avatar):
		user = User.objects.get(login = login)
		if avatar:
								user.avatar = avatar
								user.save()

	def save_admin_prava(self, login, admin_prava):
		User.objects.filter(login = login).update(admin_prava = admin_prava)		
	def ldap_getEntryValue(self, entry, key, default = None):
		if key in entry:
			return entry[key][0]
		else:
			default
	def authenticate(self, login, password):
		server = 'SMBSERVER.machinery.local'
		#user = 'ldap_reader@machinery.local'
		#password = 'DLstP9Nt'

		try:

			l = ldap.open(server)
			l.simple_bind_s(login + '@machinery.local', password)
			try:
				User.objects.get(login = login) 
			except:

				filter = '(&(name=*)(sAMAccountName={0}))'.format(ldap.filter.escape_filter_chars(login))
				search = l.search_s(
					'dc=machinery,dc=local',
					ldap.SCOPE_SUBTREE,
					filter,
					['givenName', 'sn', 'mail', 'sAMAccountName']
				)

				for dn, entry in search:
					if dn and entry:		
							first_name  =  self.ldap_getEntryValue(entry, 'givenName')
							second_name = self.ldap_getEntryValue(entry, 'sn')
							mail 		= self.ldap_getEntryValue(entry, 'mail')

				self.save_user(login = login, first_name = first_name, second_name = second_name, email = mail)
				print password
			return True
		except:
			return False


	def status(self, login, document):
		user 	 = User.objects.get(login = login) 
		
		document = Documents.objects.get(id_versia = document.id_versia, versia_final = True)
		if user == document.user_id:
				return 1
		try:
			status = DocumentUser.objects.get(document = document, user = user).status
			return status
		except:				
			status = DocumentGroup.objects.get(document = document, group = user.id_function.id_group).status
			return status

	def document_final(self, document_id):
		try:
			document = Documents.objects.get(id = document_id)
			documents = Documents.objects.get(id_versia = document.id_versia, versia_final = True)
			
			return document
		except:
			pass
	def documents_all_user(self, login):
		
			document = Documents.objects.filter(user_id = User.objects.get(login = login), versia_final = True)
			print document
			
			#document_group = DocumentGroup.objects.raw('SELECT * FROM')
			document_group= DocumentGroup.objects.filter(group = User.objects.get(login = login).id_function.id_group)

			document_user = DocumentUser.objects.filter(user = User.objects.get(login = login))
			dg = []
			for i in document:
				for j in range(len(document_group)):
					if document_group[j].document != i:
						dg.append(document_group[j])
					
			for j in document_user:
				for i in range(len(dg)):
					if dg[i].document != j.document:
						del dg[i]
						break
			
					
					
				
					
			return document,  dg, document_user



	def save_document(self, login, file):
		document = Documents(titel = file.name, user_id = User.objects.get(login = login), status = 1, versia_final = True, versia = '1', date = datetime.datetime.now(), file = file)
		document.id_versia = 0
		
		
		document.save()
		document.id_versia = document.id
		
		
		document.save()
	def new_versia_document(self, id_d, file, login):
		d = Documents.objects.get(id = id_d)

		v = str(int(d.versia) + 1)
		document = Documents(titel = d.titel, user_id = d.user_id, status = d.status, versia_final = True, versia = v, id_versia = d.id_versia, date = datetime.datetime.now(), update = User.objects.get(login = login))
		document.file = file
		document.save()
		user_document = DocumentUser.objects.filter(document = d).update(document = document)
		'''for i in user_document:
									i.document = document
									i.save()'''
		group_document = DocumentGroup.objects.filter(document = d).update(document = document)
		'''for i in group_document:
									i.document = document
									i.save()'''
		d.versia_final = False
		d.save()
		return document.id
	def bos_group(self, group):
		try:
			return User.objects.get(id_function = Function.objects.get(bos_function = True, id_group = group))
		except:
			pass

	def user_document(self, user, status, id_d):
		document = Documents.objects.get(id = id_d)
		document = Documents.objects.get(id_versia = document.id_versia, versia_final = True)

		try:
			
			
			if user == document.user_id:
					return 1
			else:
				status = DocumentUser.objects.get(document = document, user = user).status
				return  2
		except:
			

				document_user = DocumentUser(user = user, document = document, status = status)
				document_user.save()
				return 5
			
	def group_document(self, group, status, id_d):
		document = Documents.objects.get(id = id_d)
		document = Documents.objects.get(id_versia = document.id_versia, versia_final = True)
		try:
			status = DocumentGroup.objects.get(document = document, group = group)
			
		except:	
			document_group = DocumentGroup(group = group, document = document, status = status)
			document_group.save()
	


	def document_access(self, id_d, login):
		document 	= self.document_final(id_d)
		users 		= DocumentUser.objects.filter(document = document)
		Group 		= DocumentGroup.objects.filter(document = document)
		return users, Group, self.status(login, document)
	def delet_document_user(self, id_document_usesr):
		document_user = DocumentUser.objects.get(id = id_document_usesr)
		id_d = document_user.document.id
		document_user.delete()
		return id_d
	def delet_document_group(self, id_document_group):
		document_group = DocumentGroup.objects.get(id = id_document_group)
		id_d = document_group.document.id
		document_group.delete()
		return id_d

	def all_versia_document(self, id_d, login):
		document = Documents.objects.get(id = id_d)
		if self.status(login, document):
			return Documents.objects.filter(id_versia = document.id_versia)

		
	def delete_document(self, id_d, login):
		document = Documents.objects.get(id = id_d)
		if self.status(login, document):
			d = Documents.objects.filter(id_versia = document.id_versia).delete()						
	
	def view_document_matching(self, login):
		return Documents.objects.filter(user_id = User.objects.get(login = login), versia_final = True)

	def comment_matching(self, id_matching, comment, login):
		comment_matching = Comment_Matching(matching = Matching.objects.get(id = id_matching), user = User.objects.get(login = login), comment = comment, date = datetime.datetime.now())
		comment_matching.save()
	def matching_user_new(self, user, id_matching):
		matching =  Matching.objects.get(id = id_matching)
		try:
			matching_user = Matching_User.objects.get(matching  = matching, user = user)
			return 1
		except:				
			if matching.id_creator != user and matching.id_signatory != user:
				try:
					matching_user = Matching_User.objects.filter(matching  = matching)
					number = matching_user[0].number + 1
					for i in matching_user:
						if number == i.number:
							number += 1
				except:
					number = 2
				matching_user = Matching_User(user = user, matching = Matching.objects.get(id = id_matching), number = number, status = 1)
				matching_user.save()
	def new_matching(self, login):
		try:
			matching = Matching.objects.get(id_creator =  User.objects.get(login = login), status = 1)
		except:
			matching = Matching(id_creator = User.objects.get(login = login), date = datetime.datetime.now(), status = 1)
			matching.save()
			matching_user = Matching_User(matching = matching, user =  matching.id_creator, number = 1, status = 1)
			matching_user.save()
		return matching
	
	def document_matchin_new(self, id_matching, id_d, login):
		user = User.objects.get(login = login)
		document = Documents.objects.get(id = id_d)
		try:
			document_matching = Matching_Document.objects.get(matching = Matching.objects.get(id = id_matching), document = document)
		except:
			if self.status(login, document) == 1:
				document_matching = Matching_Document(document = document, matching = Matching.objects.get(id = id_matching))
				document_matching.save()
	
	def delete_matching_user(self, login, id_matching):
		matching_user = Matching_User.objects.get(matching = Matching.objects.get(id = id_matching), user = User.objects.get(login = login))
		matching_users = Matching_User.objects.filter(matching = Matching.objects.get(id = id_matching))
		for i in matching_users:
			if i.number > matching_user.number:
				i.number -= 1
				i.save()
		matching_user.delete()


	def delete_matching_document(self, id_d, id_matching):

		Matching_Document.objects.filter(matching = Matching.objects.get(id = id_matching), document = Documents.objects.get(id = id_d)).delete()


	def matching_performer_update(self, user, id_matching):
		matching = Matching.objects.get(id = id_matching)
		matching_user = Matching_User.objects.filter(matching = matching)
		for i in matching_user:
			if i.user == user:
				return
		Matching_User.objects.filter(matching = Matching.objects.get(id = id_matching), number = 1, status = 1).update(user = user)		
	def matching_date_update(self, id_matching, date):
		Matching.objects.filter(id = id_matching).update(date_end = date)
	
	def matching_signatory(self, user, id_matching):

		matching = Matching.objects.get(id = id_matching)
		matching_user = Matching_User.objects.filter(matching = matching)
		for i in matching_user:
			if i.user == user:
				return
		if matching.id_creator != user:
			matching.id_signatory = user
			matching.save()
	def matching_specification(self, id_matching, specification):
		Matching.objects.filter(id = id_matching).update(specification = specification)
	def matching_staus(self, id_matching, status):
		matching = Matching.objects.get(id = id_matching)
		if Matching_User.objects.filter(matching = matching, number = 1) and matching.id_signatory and matching.specification and Matching_Document.objects.filter(matching = matching) and Matching_User.objects.filter(matching = matching) and matching.status == 1 and status == 2:
			matching.status = status
			Matching_User.objects.filter(matching = matching, number = 1).update(status = 2)
			matching.save()
			return True
		if status == 3 and matching.status ==2: 
			matching_user = Matching_User.objects.filter(matching = id_matching)
			for i in matching_user:
				if i.status != 3:
					return False
			matching.status = status
			matching.save()
			return True
	def matching_titel(self, titel, id_matching):
		Matching.objects.filter(id = id_matching).update(titel = titel)

	def rework_matching(self, id_matching):
		Matching_User.objects.filter(matching = id_matching, status = 2).update(status = 1)
		Matching_User.objects.filter(matching = id_matching, status = 2).update(status = 1)
		Matching_User.objects.filter(matching = id_matching, number = 1).update(status = 2)

	def status_user_matching(self, id_matching):
		matching_user = Matching_User.objects.get(matching = id_matching, status = 2)
		matching_user.status = 3
		matching_user.save() 
		try:
			matching_user_status = Matching_User.objects.filter(matching = id_matching, status = 1, number = matching_user.number + 1).update(status = 2)
			
		except:
			if not self.matching_staus(id_matching, 3):
				matching_user.status = 1
				matching_user.save()
				self.rework_matching(id_matching)
				self.comment_matching(id_matching, "error", Matching.objects.get(id = id_matching).login)
	def delete_matching(self, id_matching):
		Matching_Document.objects.filter(matching = Matching.objects.filter(id = id_matching)).delete()
		Matching_User.objects.filter(matching = Matching.objects.filter(id = id_matching)).delete()
		Comment_Matching.objects.filter(matching = Matching.objects.filter(id = id_matching)).delete()
		Matching.objects.filter(id = id_matching).delete()
	def matching_users(self, id_matching):
		return Matching_User.objects.filter(matching = Matching.objects.get(id = id_matching))

	def matching(self, id_matching, login):
		try:
			matching = Matching.objects.get(id = id_matching)
		except:
			matching = self.new_matching(login)
			return False, matching, False, False
		user = self.matching_users(id_matching)
		document = Matching_Document.objects.filter(matching = matching)
		return True, matching, user, document

				
	def matching_all(self, login):
		matching_creator = Matching.objects.filter(id_creator = User.objects.get(login = login))
		matching_user = Matching_User.objects.filter(user = User.objects.get(login = login))
		matching = []
		user_performer = []
		flag = True
		for i in matching_creator:
			for j in matching_user:
				if i == j.matching:
					flag = False
					break
			if flag:
				matching.append(i)
				user_performer.append(Matching_User.objects.get(matching = i, number = 1))

		for i in matching_user:
			matching.append(i.matching)
			user_performer.append(Matching_User.objects.get(matching = i.matching, number = 1))
		return matching_creator, user_performer

	def user_matching_runing(self, id_matching, login):
		try:
			matching = Matching.objects.get(id = id_matching)
			user = Matching_User.objects.get(matching = matching, user = User.objects.get(login = login))
			document = Matching_Document.objects.filter(matching = matching)
			performer = Matching_User.objects.get(matching = matching, number = 1)
			return matching, document, user, performer.user
		except:
			return False, False, False, False

