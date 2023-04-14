from django.shortcuts import render, HttpResponse, redirect
import pyrebase
from django.contrib import messages
# import firebase_admin
# from firebase_admin import db,auth,storage
config = {
  'apiKey': "AIzaSyBP7flMKxSAanmJEQpWEGm0Fb2NtYw8PHY",
  'authDomain': "fir-c545c.firebaseapp.com",
  'projectId': "fir-c545c",
  'storageBucket': "fir-c545c.appspot.com",
  'messagingSenderId': "281167381966",
  'appId': "1:281167381966:web:dd339812bbc3a27004979f",
  'measurementId': "G-8GCKWNJB2V",
  'databaseURL':"https://fir-c545c-default-rtdb.firebaseio.com/",
}

firebase = pyrebase.initialize_app(config)
storage,auth,db = firebase.storage(),firebase.auth(),firebase.database()
# cred = firebase_admin.credentials.Certificate('1.json')
# firebase1 = firebase_admin.initialize_app(cred)


def index(request):
    # try:
        if not auth.current_user:
            if request.method=='POST':
                email, password = request.POST['email'], request.POST['password']
                user = auth.sign_in_with_email_and_password(email,password)
                # if email=='admin' and password=='711':return redirect('/admin')
                if user:
                    messages.add_message(request,messages.INFO,'Login Successful')
                    # print(user)
                    u1 = auth.get_account_info(user['idToken'])
                    print(u1)
                    # return redirect('/admin')
                    # claims = auth.sign_in_with_custom_token(user['idToken'])
                    # if claims['admin'] == True: return redirect ('/admin')
                    return redirect(f'/indi/{user["localId"]}')
                else:messages.add_message(request,messages.INFO,'Incorrect Credentials')
            return render(request,'index.html')
        else:return redirect(f'/indi/{auth.current_user["localId"]}')
    # except:
    #     messages.add_message(request,messages.INFO,'Some Error Occured')
    #     return redirect('/')

def post(request):
    try:
        if request.method=='POST':
            name,password,email,balance,pin = request.POST['username'],request.POST['password'],request.POST['email'],request.POST['balance'],request.POST['pin']
            user = auth.create_user_with_email_and_password(email,password)
            x={'username':name,'balance':balance,'pin':pin}
            db.child('users').child(user['localId']).set(x)
            messages.add_message(request,messages.INFO,f'User Created Successfully')
            return redirect('/')
        return render (request,'create.html')
    except:
        messages.add_message(request,messages.INFO,'Some Error Occured')
        return redirect('/create')


def indi(request,id):
    try:
        if auth.current_user:
            if auth.current_user['localId'] == id:
                users = db.child('users').child(id).get()
                trans = db.child('transactions').order_by_child('id').equal_to(id).get().val()
                context= {'users':[dict(users.val())],'id':id,'trans':list(dict(trans).values())}
                return render(request,'indi.html',context)
            else:return HttpResponse('Forbidden',status=403)
        else:return HttpResponse('Forbidden',status=403)
    except:
        messages.add_message(request,messages.INFO,'Some Error Occured')
        return redirect('/')
    
def credit(request,id):
    try:
        if auth.current_user:
            if auth.current_user['localId'] == id:
                if request.method == 'POST':
                    amount,pin = request.POST['credit'],request.POST['pin']
                    user = db.child('users').child(id).get().val()
                    if pin == dict(user)['pin']:
                        balance = float(dict(user)['balance']) + float(amount)
                        db.child('users').child(id).update({'balance':balance})
                        tran = {'transaction_type':'CREDIT','balance':balance,'amount':amount,'id':id}
                        db.child('transactions').push(tran)
                        messages.add_message(request,messages.INFO,f'{amount} credited successfully')
                    else:messages.add_message(request,messages.INFO,f'{amount} credited successfully')
                    return redirect(f'/indi/{id}')
            else:return HttpResponse('Forbidden',status=403)
        else:return HttpResponse('Forbidden',status=403)
    except:
        messages.add_message(request,messages.INFO,'Some Error Occured')
        return redirect('/')

def debit(request,id):
    try:
        if auth.current_user:
            if auth.current_user['localId'] == id:
                if request.method == 'POST':
                    amount,pin = request.POST['debit'],request.POST['pin']
                    user = db.child('users').child(id).get().val()
                    if pin == dict(user)['pin']:
                        balance = float(dict(user)['balance']) - float(amount)
                        db.child('users').child(id).update({'balance':balance})
                        tran = {'transaction_type':'DEBIT','balance':balance,'amount':amount,'id':id}
                        db.child('transactions').push(tran)
                        messages.add_message(request,messages.INFO,f'{amount} debited successfully')
                    else:messages.add_message(request,messages.INFO,f'{amount} debited successfully')
                    return redirect(f'/indi/{id}')
            else:return HttpResponse('Forbidden',status=403)
        else:return HttpResponse('Forbidden',status=403)
    except:
        messages.add_message(request,messages.INFO,'Some Error Occured')
        return redirect('/')

def logout(request):
    try:auth.current_user=None
    except KeyError: pass
    except:pass
    return redirect('/')
