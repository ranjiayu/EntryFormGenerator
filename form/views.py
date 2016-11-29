import re
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from models import Form, Key, KeyContent


# Create your views here.

def createform(request):
    if request.method == 'GET':
        return render(request, 'form/createForm.html')
    elif request.method == 'POST':
        if 'password' in request.POST and 'title' in request.POST and 'author' in request.POST and 'password' in request.POST and 'key1' in request.POST and 'type1' in request.POST:
            title = request.POST['title']
            author = request.POST['author']
            password = request.POST['password']
            if len(title) < 70 and len(author) < 70:
                new_form = Form(title=title, author=author, password=password)
                new_form.save()
            else:
                return render(request, 'form/error.html', {
                    'msg': 'Some contents are too long.',
                })

            keylist = list()
            typelist = list()
            for i in request.POST:
                key_pattern = re.compile(r'^key[0-9]+$')
                key_match = key_pattern.match(i)
                type_pattern = re.compile(r'^type[0-9]+$')
                type_match = type_pattern.match(i)
                if key_match:
                    keylist.append(str(key_match.group()))

                if type_match:
                    typelist.append(str(type_match.group()))

            keylist = sorted(keylist, key=lambda x: int(x[-1:]))
            typelist = sorted(typelist, key=lambda x: int(x[-1:]))

            for (k, t) in zip(keylist, typelist):
                klabel = request.POST[k]
                ktype = request.POST[t]
                if klabel != '' and ktype != '':
                    if len(klabel) < 70 and len(ktype) < 10:
                        new_key = Key(form=new_form, keyLabel=klabel, keyType=ktype)
                        new_key.save()
                    else:
                        return render(request, 'form/error.html', {
                            'msg': 'Some contents are too long.',
                        })
                else:
                    return render(request, 'form/error.html', {
                        'msg': 'Please check the inputs.',
                    })

            form_id = new_form.id
            return HttpResponseRedirect('/form/enter/' + str(form_id) + '/')
        else:
            return render(request, 'form/error.html', {
                'msg': 'AT LEAST have 1 key'
            })


def enterform(request, form_id):
    if request.method == 'GET':
        data = get_object_or_404(Form, pk=int(form_id))
        key = data.key_set.all().order_by('create_time')
        return render(request, 'form/enterForm.html', {
            'data': data,
            'key': key,
        })
    elif request.method == 'POST':
        data = get_object_or_404(Form, pk=int(form_id))
        key = list(data.key_set.all().order_by('create_time'))

        for i in key:
            new_keycontent = KeyContent(key=i, content=request.POST[str(i.id)])
            new_keycontent.save()

        return render(request, 'form/success.html', {
            'msg': 'Done.We have got it!',
        })


def manageform(request, form_id):
    if request.method == 'GET':
        data = get_object_or_404(Form, pk=int(form_id))
        return render(request, 'form/manageForm.html', {
            'pass': False,
            'data': data,
        })

    elif request.method == 'POST':
        if 'password' in request.POST:
            password = request.POST['password']
        data = get_object_or_404(Form, pk=int(form_id))
        if data.password == password:
            key = data.key_set.all().order_by('create_time')
            key_content = list()
            for i in range(len(key)):
                key_content.append(list(key[i].keycontent_set.all().order_by('create_time')))

            key_data = [[0 for i in range(len(key_content))] for j in range(len(key_content[0]))]

            for i in range(len(key_content)):
                for j in range(len(key_content[i])):
                    key_data[j][i] = key_content[i][j]

            return render(request, 'form/manageForm.html', {
                'pass': True,
                'msg': None,
                'data': data,
                'key': key,
                'key_data': key_data,
            })
        else:
            return render(request, 'form/manageForm.html', {
                'data': data,
                'pass': False,
                'msg': 'Wrong Password.',
            })
