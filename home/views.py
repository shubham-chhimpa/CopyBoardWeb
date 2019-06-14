from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, HttpResponse

from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


class UserAuth:
    def __init__(self):
        self.email = ''
        self.logged = False
        self.uid = ''
        self.name = ''

    def is_logged(self):
        return self.logged

    def set_logged(self, status):
        self.logged = status

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_uid(self):
        return self.uid

    def set_uid(self, uid):
        self.uid = uid

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name


user_auth = UserAuth()


# Create your views here.


def index(request):
    if user_auth.is_logged() == False:
        print(user_auth.is_logged())

        return HttpResponseRedirect('signin')
    else:
        print(user_auth.is_logged())
        print(user_auth.get_uid())
        notes_docs = db.collection(u'users').document(user_auth.get_uid()).collection('copyboard').order_by(
            u'timestamp', direction=firestore.Query.DESCENDING).get()
        notes = []
        for doc in notes_docs:
            notes.append(doc.to_dict())
        return render(request, 'home/base.html', {'notes': notes, 'name': user_auth.get_name()})


def logout(request):
    user_auth.set_logged(False)
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
            user_auth.set_logged(True)
            user_auth.set_email(user['email'])
            user_auth.set_uid(user['id'])
            user_auth.set_name(user['name'])
            return HttpResponseRedirect('index')
        else:
            return render(request, 'home/login.html')
    if user_auth.is_logged() == False:
        print(user_auth.is_logged())
        return render(request, 'home/login.html')
    else:
        print(user_auth.is_logged())
        return HttpResponseRedirect('index')


#         except:
#             return render(request, 'home/login.html')
# except:
#     return render(request, 'home/login.html')


def take_note(request):
    if user_auth.is_logged() == False:
        print(user_auth.is_logged())

        return HttpResponseRedirect('signin')
    else:
        print(user_auth.is_logged())
        return render(request, 'home/takenote.html')


def add_note(request):
    if user_auth.is_logged() == False:
        print(user_auth.is_logged())
        return HttpResponseRedirect('signin')
    else:
        print(user_auth.is_logged())
        if request.method == "POST":
            text = request.POST.get('text')
            note_ref = db.collection(u'users').document(user_auth.get_uid()).collection('copyboard').document()
            note_ref.set({
                u'id': note_ref.id,
                u'text': text,
                u'timestamp': firestore.SERVER_TIMESTAMP
            })
            return JsonResponse({"success": "true"})
    return JsonResponse({"success": "false"})


def delete_note(request):
    if user_auth.is_logged() == False:
        print(user_auth.is_logged())
        return HttpResponseRedirect('signin')
    else:
        print(user_auth.is_logged())
        if request.method == "POST":
            nid = request.POST.get('id')
            db.collection(u'users').document(user_auth.get_uid()).collection('copyboard').document(nid).delete()

            return JsonResponse({"success": "true"})
    return JsonResponse({"success": "false"})


def edit_note(request, nid):
    if user_auth.is_logged() == False:
        print(user_auth.is_logged())
        return HttpResponseRedirect('/')
    else:
        print(user_auth.is_logged())
        print(nid)
        note_doc = db.collection(u'users').document(user_auth.get_uid()).collection('copyboard').document(nid).get()
        print(note_doc.to_dict())
        return render(request, 'home/editnote.html',{'note':note_doc.to_dict()})

def update_note(request):
    if user_auth.is_logged() == False:
        print(user_auth.is_logged())
        return HttpResponseRedirect('signin')
    else:
        print(user_auth.is_logged())
        if request.method == "POST":
            nid = request.POST.get('id')
            text = request.POST.get('text')
            print('in update_tetx',nid,text)
            db.collection(u'users').document(user_auth.get_uid()).collection('copyboard').document(nid).update({
                u'text' : text
            })

            return JsonResponse({"success": "true"})
    return JsonResponse({"success": "false"})
