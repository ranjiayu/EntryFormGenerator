import re
from django.shortcuts import render
from django.http import HttpResponse
from models import Form,Key,KeyContent
# Create your views here.

def createForm(request):
	if request.method == 'GET':
		return render(request,'form/createForm.html')
	elif request.method == 'POST':
		if 'title' in request.POST and 'author' in request.POST and 'password' in request.POST and 'key1' in request.POST and 'type1' in request.POST:
			title = request.POST['title']
			author = request.POST['author']
			new_form = Form(title = title,author = author)
			new_form.save()

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
				new_key = Key(form = new_form,keyLabel = Klabel,keyType = Ktype)
				new_key.save()


			return HttpResponse('done')
		else:
			return render(request,'form/error.html',{
					'msg' : 'At least have 1 key'
				})



def enterForm(request,id):
	return render(request,'form/enterForm.html')

def manageForm(request,id):
	return render(request,'form/manageForm.html')

