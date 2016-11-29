import re
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from models import Form,Key,KeyContent
# Create your views here.

def createForm(request):
	if request.method == 'GET':
		return render(request,'form/createForm.html')
	elif request.method == 'POST':
		if 'password' in request.POST and 'title' in request.POST and 'author' in request.POST and 'password' in request.POST and 'key1' in request.POST and 'type1' in request.POST:
			title = request.POST['title']
			author = request.POST['author']
			password = request.POST['password']
			if len(title) < 70 and len(author) < 70:
				new_form = Form(title = title,author = author,password = password)
				new_form.save()
			else:
				return HttpResponse('too long')

			keyList = list()
			typeList = list()
			for i in request.POST:
				key_pattern = re.compile(r'^key[0-9]+$')
				key_match = key_pattern.match(i)
				type_pattern = re.compile(r'^type[0-9]+$')
				type_match = type_pattern.match(i)
				if key_match:
					keyList.append(str(key_match.group()))

				if type_match:
					typeList.append(str(type_match.group()))

			keyList = sorted(keyList,key = lambda x:int(x[-1:]))
			typeList = sorted(typeList,key = lambda x:int(x[-1:]))

			for (k,t) in zip(keyList,typeList):
				Klabel = request.POST[k]
				Ktype = request.POST[t]
				if Klabel != '' and Ktype != '':
					if len(Klabel) < 70 and len(Ktype) < 10:
						new_key = Key(form = new_form,keyLabel = Klabel,keyType = Ktype)
						new_key.save()
					else:
						return HttpResponse('too long')
				else:
					return HttpResponse('Check the input')

			form_id = new_form.id
			return HttpResponseRedirect('/form/enter/' + str(form_id) + '/')
		else:
			return render(request,'form/error.html',{
					'msg' : 'At least have 1 key'
				})



def enterForm(request,id):
	if request.method == 'GET':
		data = get_object_or_404(Form,pk = int(id))
		key = data.key_set.all().order_by('create_time')
		return render(request,'form/enterForm.html',{
			'data' : data,
			'key' : key,
		})
	elif request.method == 'POST':
		data = get_object_or_404(Form,pk = int(id))
		key = list(data.key_set.all().order_by('create_time'))

		for i in key:
			new_keycontent = KeyContent(key = i,content = request.POST[str(i.id)])
			new_keycontent.save()

		return HttpResponse('ok')


def manageForm(request,id):
	if request.method == 'GET':
		data = get_object_or_404(Form,pk = int(id))
		return render(request,'form/manageForm.html',{
			'pass' : False,
			'data' : data,
		})

	elif request.method == 'POST':
		if 'password' in request.POST:
			password = request.POST['password']
		data = get_object_or_404(Form,pk = int(id))
		if data.password == password:
			key = data.key_set.all().order_by('create_time')
			key_content = list()
			for i in range(len(key)):
				key_content.append(list(key[i].keycontent_set.all().order_by('create_time')))
			return render(request,'form/manageForm.html',{
				'pass' : True,
				'msg' : None,
				'data' : data,
				'key' : key,
				'key_content' : key_content,
			})
		else:
			return render(request,'form/manageForm.html',{
				'data' : data,
				'pass' : False,
				'msg' : 'Wrong Password.',
			})