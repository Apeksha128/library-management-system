import datetime
from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from lmsApp import models, forms
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group








def context_data(request):
    fullpath = request.get_full_path()
    abs_uri = request.build_absolute_uri()
    abs_uri = abs_uri.split(fullpath)[0]
    context = {
        'system_host' : abs_uri,
        'page_name' : '',
        'page_title' : '',
        'system_name' : 'Library Managament System',
        'topbar' : True,
        'footer' : True,
    }

    return context
    
def userregister(request):
    context = context_data(request)
    context['topbar'] = False
    context['footer'] = False
    context['page_title'] = "User Registration"
    if request.user.is_authenticated:
        return redirect("home-page")
    return render(request, 'register.html', context)

def save_register(request):
    resp={'status':'failed', 'msg':''}
    if not request.method == 'POST':
        resp['msg'] = "No data has been sent on this request"
    else:
        form = forms.SaveUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account has been created succesfully")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if resp['msg'] != '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.name}] {error}.")
            
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def update_profile(request):
    context = context_data(request)
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = forms.UpdateProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = forms.UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile-page")
        else:
            context['form'] = form
            
    return render(request, 'manage_profile.html',context)

@login_required
def update_password(request):
    context =context_data(request)
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = forms.UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)

# Create your views here.
def login_page(request):
    context = context_data(request)
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    return render(request, 'login.html', context)

def admin_signup(request):
        if request.method == "POST":
                form = forms.AdminSigupForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    user.save()
                    username=form.cleaned_data.get('username')
                    email       = form.cleaned_data.get("email")
                    password    = form.cleaned_data.get("password")
                    
                    new_user    = User.objects.create_user(username, password)
                    print(new_user)
                    user = authenticate(username=username, password=password)
                    login(request, user)

                return redirect("/home")
        else:
                form = forms.AdminSigupForm()

        return render(request, "adminsignup.html", {"form":form})
    # return render(request, 'adminsignup.html')
    # form=forms.AdminSigupForm(request.POST)
    # if form.is_valid():
    #         user = form.save()
    #         user.refresh_from_db()  
    #         # load the profile instance created by the signal
    #         user.save()
    #         raw_password = form.cleaned_data.get('password')

    #         # login user after signing up
    #         user = authenticate(username=user.username, password=raw_password)
    #         login(request, user)

    #         # redirect user to home page
    #         return redirect('home')
    # else:
    #     form = admin_signup(request)
    # return render(request, 'adminsignup.html', {'form': form})



def studentclick_view(request):
    if request.user.is_authenticated:
        return render(request,'studentclick.html')
    return render(request,'studentclick.html')




def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

@login_required
def home(request):
    context = context_data(request)
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['categories'] = models.Category.objects.filter(delete_flag = 0, status = 1).all().count()
    context['books'] = models.Students.objects.filter(delete_flag = 0, status = 1).all().count()
    

    return render(request, 'home.html', context)

def logout_user(request):
    logout(request)
    return redirect('login-page')
    
@login_required
def profile(request):
    context = context_data(request)
    context['page'] = 'profile'
    context['page_title'] = "Profile"
    return render(request,'profile.html', context)

@login_required
def users(request):
    context = context_data(request)
    context['page'] = 'users'
    context['page_title'] = "User List"
    context['users'] = User.objects.exclude(pk=request.user.pk).filter(is_superuser = False).all()
    return render(request, 'users.html', context)

def studentbooks(request):
    context = context_data(request)
    context['page'] = 'book'
    context['page_title'] = "Book List"
    context['books'] = models.Books.objects.filter(delete_flag = 0).all()
    return render(request, 'student_book_view.html', context)

@login_required
def books(request):
    context = context_data(request)
    context['page'] = 'book'
    context['page_title'] = "Book List"
    context['books'] = models.Books.objects.filter(delete_flag = 0).all()
    return render(request, 'books.html', context)




@login_required
def save_book(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            book = models.Books.objects.get(id = post['id'])
            form = forms.SaveBook(request.POST, instance=book)
        else:
            form = forms.SaveBook(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Book has been saved successfully.")
            else:
                messages.success(request, "Book has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_book(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_book'
    context['page_title'] = 'View Book'
    if pk is None:
        context['book'] = {}
    else:
        context['book'] = models.Books.objects.get(id=pk)
    
    return render(request, 'view_book.html', context)

@login_required
def manage_book(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_book'
    context['page_title'] = 'Manage Book'
    if pk is None:
        context['book'] = {}
    else:
        context['book'] = models.Books.objects.get(id=pk)
    context['sub_categories'] = models.SubCategory.objects.filter(delete_flag = 0, status = 1).all()
    return render(request, 'manage_book.html', context)

@login_required
def delete_book(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Book ID is invalid'
    else:
        try:
            models.Books.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Book has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Book Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

