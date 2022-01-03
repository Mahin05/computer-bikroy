import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from ComputerShop.forms import UserForm,ProductForm,UserProfileForm,UserUpdateForm,EditPostForm
from ComputerShop.models import product,userprofile
from django.contrib.auth.models import User

# Create your views here.
from django.template.context_processors import csrf


def base(request):
    data = product.objects.all()
    return render(request,'index.html',{'data':data})

def signup(request):
    if request.method == 'POST':
        data = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if data.is_valid() and profile_form.is_valid():
            password = data.save()
            password.set_password(password.password)
            password.save()
            # user = data.save()  ###add user to database
            profile = profile_form.save(commit=False)
            profile.user = password
            profile.save()
            return redirect('/login')
        else:
            messages.success(request,f'Something Went Wrong!')
            return redirect('/signup')
    data = UserForm()
    profile_form = UserProfileForm()
    return render(request,'signup.html',{'data':data,'profile_form':profile_form})


def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user :
            login(request,user)
            data = User.objects.get(username=username)
            request.session['username'] =data.username
            request.session['password'] =data.password
            request.session['superuser'] =data.is_superuser
            return redirect('/userview')
        else:
            # messages.success(request,f'Wrong username or password!')
            return redirect('/login')
    return render(request,'login.html')

@login_required(login_url='/login')
def userlogout(request):
    del request.session['username']
    # del request.session['email']
    del request.session['superuser']
    logout(request)
    return redirect('/')

@login_required(login_url='/login')
def addproduct(request):
    if request.method == 'POST':
        brand = request.POST['brand']
        model = request.POST['model']
        condition = request.POST['condition']
        price = request.POST['price']
        details = request.POST['details']
        datentime= datetime.datetime.now()
        image = request.FILES['image']
        user=request.user
        ins = product(brand=brand,model=model,condition=condition,price=price,details=details,datentime=datentime,image=image,user=user)
        ins.save()
        return redirect('/userview')
    return render(request,'product.html')

@login_required(login_url='/login/')
def userview(request):
    data = userprofile.objects.filter(user = request.user)
    posts = product.objects.filter(user= request.user)
    return render(request,'user.html',{'data':data,'posts':posts})

@login_required(login_url='/login/')
def DeleteUserProfile(request):
    data = User.objects.filter(username = request.user)
    data.delete()
    return redirect('/')

@login_required(login_url='/login/')
def EditUserProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = UserProfileForm(request.POST,instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('/userview')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.userprofile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request,'UserUpdate.html',context)

@login_required(login_url='/login/')
def EditPost(request,id):
    item = product.objects.get(product_id=id)
    if request.user == item.user:
        if request.method == 'POST':
            form = EditPostForm(request.POST,request.FILES, instance=item)
            if form.is_valid():
                form.save()
                return redirect('/userview')
        else:
            form = EditPostForm(instance=item)

        context ={
            'item':item

        }

        return render(request,'edit.html',context)

@login_required(login_url='/login/')
def DeletePost(request,id):
    item = product.objects.get(product_id=id)
    if request.user == item.user:
        product.objects.filter(product_id=id).delete()
        return redirect('/userview')
