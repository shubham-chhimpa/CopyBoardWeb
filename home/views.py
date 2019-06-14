from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, HttpResponse, redirect

from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


# Create your views here.


def index(request):
    try:
        if request.session['logged'] == False:

            return HttpResponseRedirect('signin')
        else:
            notes_docs = db.collection(u'users').document(request.session['uid']).collection(
                'copyboard').order_by(
                u'timestamp', direction=firestore.Query.DESCENDING).get()
            notes = []
            for doc in notes_docs:
                notes.append(doc.to_dict())
            return render(request, 'home/base.html', {'notes': notes, 'name': request.session['name']})
    except:
        return HttpResponseRedirect('signin')




def logout(request):
    request.session.flush()
    return HttpResponseRedirect('signin')


def signin(request):
    # try:
    if request.method == "POST":
        # try:
        email = request.POST.get('email')
        password = request.POST.get('pass')
        user_docs = db.collection(u'users').where(u'email', u'==', email).get()
        users = []
        for doc in user_docs:
            print(doc.to_dict())
            users.append(doc.to_dict())
        user = users[0]
        if user['pass'] == password:
            print(user['pass'], password)
            request.session['logged'] = True
            request.session['email'] = user['email']
            request.session['uid'] = user['id']
            request.session['name'] = user['name']

            return HttpResponseRedirect('index')
        else:
            return render(request, 'home/login.html')
    return render(request, 'home/login.html')


#         except:
#             return render(request, 'home/login.html')
# except:
#     return render(request, 'home/login.html')


def take_note(request):
    if request.session['logged'] == False:

        return HttpResponseRedirect('signin')
    else:
        return render(request, 'home/takenote.html')


def add_note(request):
    if request.session['logged'] == False:
        return HttpResponseRedirect('signin')
    else:
        if request.method == "POST":
            text = request.POST.get('text')
            note_ref = db.collection(u'users').document(request.session['uid']).collection('copyboard').document()
            note_ref.set({
                u'id': note_ref.id,
                u'text': text,
                u'timestamp': firestore.SERVER_TIMESTAMP
            })
            return JsonResponse({"success": "true"})
    return JsonResponse({"success": "false"})


def delete_note(request):
    if request.session['logged'] == False:
        return HttpResponseRedirect('signin')
    else:
        if request.method == "POST":
            nid = request.POST.get('id')
            db.collection(u'users').document(request.session['uid']).collection('copyboard').document(nid).delete()

            return JsonResponse({"success": "true"})
    return JsonResponse({"success": "false"})


def edit_note(request, nid):
    if request.session['logged'] == False:
        return HttpResponseRedirect('/')
    else:
        print(nid)
        note_doc = db.collection(u'users').document(request.session['uid']).collection('copyboard').document(nid).get()
        print(note_doc.to_dict())
        return render(request, 'home/editnote.html', {'note': note_doc.to_dict()})


def update_note(request):
    if request.session['logged'] == False:
        return HttpResponseRedirect('signin')
    else:
        if request.method == "POST":
            nid = request.POST.get('id')
            text = request.POST.get('text')
            print('in update_tetx', nid, text)
            db.collection(u'users').document(request.session['uid']).collection('copyboard').document(nid).update({
                u'text': text
            })

            return JsonResponse({"success": "true"})
    return JsonResponse({"success": "false"})
