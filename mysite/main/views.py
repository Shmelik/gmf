#!/usr/bin/env python
#-*- coding: utf-8-*-
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from models import *
# Create your views here.

model = MadelMain()
def new_user(request):
	form = MediaForm()
	return render(request, "Form_profile.html", {
									"form"			: form,																		
									}) 
def user_save(request):
	form = MediaForm(request.POST, request.FILES)
	if form.is_valid():
           form.save()
           return HttpResponseRedirect('/success/url/')
	

	return HttpResponseRedirect("http://192.168.0.144/new_user/")
	'''form = FormProfile(request.POST, request.FILES)
	if form.is_valid():
		if (model.login_new(form.cleaned_data['login'])):
			model.save_user(request.FILES[avatar_file], form.cleaned_data['avatar'], form.cleaned_data['login'], form.cleaned_data['first_name'], form.cleaned_data['second_name'], form.cleaned_data['patronymic'], form.cleaned_data['id_function'], form.cleaned_data['email'], form.cleaned_data['phone_mob'], form.cleaned_data['phone_work'], request.FILES) 
	print form.errors
	return HttpResponseRedirect("http://192.168.0.144/")'''
def all_user(request):
	user = model.user_profile(request.session["login"])
	if user.admin_prava:
		all_user = model.all_user()

		return render(request, "all_users.html", {
										"users"	: all_user,																		
										}) 
	return HttpResponseRedirect("http://192.168.0.144/")
def update_user(request):
	#form = MediaForm()
	form_phone = FormProfile(login = request.session["login"])
	
	
	user = model.user_profile(request.session["login"])
	
	return render(request, "user_profile.html", {
									"user"			: user,
									"admin_prava"	: user.admin_prava,
									"view"			: False,
									"form_phone"	: form_phone,
									"login"			: request.session["login"],
									}) 
def profile(request):
	user = model.user_profile(request.session["login"])
	
	return render(request, "user_profile.html", {
									"user"		 : user,
									"view"		 : True,
									
									}) 
def profile_user(request, login):
	user = model.user_profile(request.session["login"])
	if user.admin_prava:
		user = model.user_profile(login)
		form_phone = FormProfile(login = login)
		return render(request, "user_profile.html", {
									"user"			: user,									
									"view"			: False,
									"form_phone" 	: form_phone,
									"admin_prava"	: True,
									"login"			: request.session["login"],
									}) 
	return HttpResponseRedirect("http://192.168.0.144/all_user")

def save_profile(request, login_ad):
	form =  FormProfile(request.POST, request.FILES)

	login = request.session["login"]
	user = User.objects.get(login = login)

	if user.admin_prava and (user.login != login_ad):
		user = User.objects.get(login = login_ad)
	if form.is_valid():
		pass

	try:
		if form.cleaned_data['first_name']:		
			model.save_first_name(user.login, form.cleaned_data['first_name'])  
	except:
		pass
	
	try:
		if form.cleaned_data['second_name']:
			model.save_second_name(user.login, form.cleaned_data['second_name'])
	except:
		pass

	try:
		if form.cleaned_data['patronymic']:
			model.save_patronymic(user.login, form.cleaned_data['patronymic'])
	except:
		pass
	try:
		if form.cleaned_data['id_function']:
			model.save_function(user.login, form.cleaned_data['id_function'])
	except:
		pass

	
	try:
		if  form.cleaned_data['email']:
			model.save_email(user.login, form.cleaned_data['email'])
	except:
		pass

	try:
		if form.cleaned_data['avatar']:
			model.save_avatar(user.login, form.cleaned_data['avatar'])
	except:
		pass
	if login_ad != login:
		try:
			model.save_admin_prava(user.login, form.cleaned_data['admin_prava_form'])
		except:
			model.save_admin_prava(user.login, False)
	try:	
		if form.cleaned_data['phone_mob_form']:
			model.save_phone_mob(user.login, form.cleaned_data['phone_mob_form'])
	except:
		pass

	try:
		if form.cleaned_data['phone_work_form']:
			model.save_phone_work(user.login, form.cleaned_data['phone_work_form'])
	except:
		pass
	print form.errors
	return HttpResponseRedirect("http://192.168.0.144/")

def logout(request):
	del request.session["login"]
	return HttpResponseRedirect("http://192.168.0.144/")



def start_page_lgoin(request):

	if "login" in request.session:
		user = model.user_profile(request.session["login"])

		return render(request, "start_page.html", {"user"	: user,
													"admin"	: user.admin_prava})
	else:
		if request.method == 'GET':
			form = LoginForm()
			return render(request, "login.html", {
										"forms": form,								
										})
		else:
			form = LoginForm(request.POST)
			if form.is_valid():

				if model.authenticate(form.cleaned_data['username'], form.cleaned_data['password'] ):
					print form.cleaned_data['password']
					if request.session.test_cookie_worked():
						request.session.delete_test_cookie()

					request.session["login"] = form.cleaned_data['username'] 
					user = model.user_profile(request.session["login"])

					return render(request, "start_page.html", {"user"	: user,
																"admin"	: user.admin_prava,})
					
				else:
					return render(request, "login.html", {
												"forms": form,	
												"error": True,							
												}) 	  
					
			else: 
				return render(request, "login.html", {
												"forms": form,	
												"error": True,							
												})


def document(request):
	document,  document_function, document_user = model.documents_all_user(request.session["login"])
	#document_function = [1232]
	return render(request, "document.html", {
											"document": document,
											"document_user": document_user,
											"document_function": document_function,
											})
def document_new(request):
	form = DocumentForm()

	return render(request, "new_document.html", {
											"form": form
											})
def document_information(request, id_d):
	document = model.document_final(id_d)
	prava = model.status(request.session["login"], document)
	return render(request, "document_information.html", {
														"document": document,
														"user_flag": prava,
														})

def document_save(request):
	form = DocumentForm(request.POST, request.FILES)
	if form.is_valid():
		model.save_document(request.session["login"],form.cleaned_data['file'])
		return HttpResponseRedirect("http://192.168.0.144/document/")	

	return HttpResponseRedirect("http://192.168.0.144/new_document/")

def document_access(request, id_d):
	user, group, status 	= model.document_access(id_d, request.session["login"])
	form_user 				= UserForm()
	form_group 				= GroupForm()
	return render(request, "document_access.html", {
														"user"		: user,
														"group"		: group,
														"status"	: status,
														"form_user"	: form_user,
														"form_group": form_group,
														"id"		: id_d,
														"login"		: request.session["login"],
														})

def access_group(request, id_d):
	form = GroupForm(request.POST)
	if form.is_valid():
		pass
	if 1:
		try:
			form.cleaned_data['status_group']
			model.group_document(form.cleaned_data['group'], 1, id_d)		
		except:
			model.group_document(form.cleaned_data['group'], 2, id_d)	
	return HttpResponseRedirect("http://192.168.0.144/document_access/%s"%id_d)


def access_user(request, id_d):
	form = UserForm(request.POST)
	if form.is_valid():
		pass
	try:

		try:
		 	form.cleaned_data['status_user']
			model.user_document(form.cleaned_data['user'], 1, id_d)
		except:

			model.user_document(form.cleaned_data['user'], 2, id_d)
			
	except:
		pass

	return HttpResponseRedirect("http://192.168.0.144/document_access/%s"%id_d)

def delet_document_user(request, id_document_user):
	id_d = model.delet_document_user(id_document_user)
	return HttpResponseRedirect("http://192.168.0.144/document_access/%s"%id_d)
def delet_document_group(request, id_document_group):
	id_d = model.delet_document_group(id_document_group)
	return HttpResponseRedirect("http://192.168.0.144/document_access/%s"%id_d)
def new_versia(request, id_d):
	form = DocumentForm()
	return render(request, "new_versia_document.html", {
														"form"	: form,
														"id"	: id_d,
														})
def versia_save(request, id_d):
	form = DocumentForm(request.POST, request.FILES)
	if form.is_valid():
		id_d = model.new_versia_document(id_d, form.cleaned_data['file'], request.session["login"])
		return HttpResponseRedirect("http://192.168.0.144/document_information/%s"%id_d)

def all_versia(request, id_d):
	documents = model.all_versia_document(id_d, request.session["login"])
	if documents:
		return render(request, "all_versia_documents.html", {
														"document"	: documents,
														"id"		: id_d,
														})
	return HttpResponseRedirect("http://192.168.0.144/document")

def delete_document(request, id_d):
	model.delete_document(id_d, request.session["login"])
	
	return HttpResponseRedirect("http://192.168.0.144/document/")
def matching_new(request):
	matching 	= model.new_matching(request.session["login"])
	return HttpResponseRedirect("http://192.168.0.144/matching_new/%s"%matching.id)
def matching_write(request, id_matching):
	flag, matching, user, document = model.matching(id_matching, request.session["login"])
	if not flag:
		return HttpResponseRedirect("http://192.168.0.144/matching_new/%s"%matching.id)
	form_matching 	= MatchingForm(id = matching.id)
	form_matching_user	= MatchingUserForm()	
	return render(request, "matching.html", {
														"matching"				: matching,
														"form_matching"			: form_matching,
														"form_matching_user"	: form_matching_user,
														"users"					: user,
														"document"				: document,
														})

def Form_Matching_Write(request, id_matching):
	form_matching 	= MatchingForm(request.POST)
	if form_matching.is_valid():
		pass
	try:	
		model.matching_date_update(form_matching.cleaned_data['date'], id_matching)
	except:
		pass
	try:	
		model.matching_titel(form_matching.cleaned_data['titel'], id_matching)
	except:
		pass
	try:	
		model.matching_performer_update(form_matching.cleaned_data['user_performe'], id_matching)
	except:
		pass
	try:	
		model.matching_specification(id_matching, form_matching.cleaned_data['specification'])
	except:
		pass
	try:	
		model.matching_signatory(form_matching.cleaned_data['user_signatory'], id_matching)
	except:
		pass
	

def matching_document(request, id_matching):
	Form_Matching_Write(request, id_matching)
	document = model.view_document_matching(request.session["login"])
	return render(request, "matching_document.html", {
														"id_matching"			: id_matching,
														"document"				: document,
														})
def matching_document_save(request, id_matching, id_d):
	model.document_matchin_new(id_matching, id_d, request.session["login"])
	return HttpResponseRedirect("http://192.168.0.144/matching_new/%s"%id_matching)
	



def matching_not(request, id_matching):
	model.delete_matching(id_matching)
	return HttpResponseRedirect("http://192.168.0.144/")
def matching_document_delete(request, id_matching, id_d):
	Form_Matching_Write(request, id_matching)
	model.delete_matching_document(id_d, id_matching)
	return HttpResponseRedirect("http://192.168.0.144/matching_new/%s"%id_matching)

def matching_user_save(request, id_matching):
	Form_Matching_Write(request, id_matching)
	form_matching_user	= MatchingUserForm(request.POST)	
	if form_matching_user.is_valid():
		model.matching_user_new(form_matching_user.cleaned_data['user'], id_matching)
	return HttpResponseRedirect("http://192.168.0.144/matching_new/%s"%id_matching)
def matching_user_delete(request, id_matching, login):
	Form_Matching_Write(request, id_matching)
	model.delete_matching_user(login, id_matching)
	return HttpResponseRedirect("http://192.168.0.144/matching_new/%s"%id_matching)


def matching_start(request, id_matching):
	Form_Matching_Write(request, id_matching)
	flag = model.matching_staus(id_matching, 2)
	if flag:
		return HttpResponseRedirect("http://192.168.0.144/")
	return HttpResponseRedirect("http://192.168.0.144/matching_new/%s"%id_matching)
	pass











def matching_path(request, id_matching):
	flag, matching, user, document = model.matching(id_matching, request.session["login"])
	if not flag:
		return HttpResponseRedirect("http://192.168.0.144/all_matching_user/")
	return render(request, "matching_path.html", {
															"matching"	: matching,
															"users"		: users,
															"document"	: document,
															})

def matching_user_status(request, id_matching):
	matching, document, user, performer = model.user_matching_runing(id_matching, request.session["login"])
	if not matching:
		return HttpResponseRedirect("http://192.168.0.144/all_matching_user/")
	if user.status == 3 and matching.status == 3:
		return matching_path(request, id_matching)
	elif user.status == 2:
		return render(request, "matching_runing.html", {
															"matching"	: matching,
															"document"	: document,
															"user"		: user,
															"performer"	: performer,
															})
	else:
		return HttpResponseRedirect("http://192.168.0.144/all_matching_user/")
def all_matching_user_status(request):
	matching_all, user_performe = model.matching_all(request.session["login"])
	return render(request, "matching_all.html", {
															"matching"	: matching_all,
															"user"			: user_performe,
															})
def matching_return():
	pass
def matching_next():
	pass
