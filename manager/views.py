from django.shortcuts import render, get_object_or_404, redirect
from .models import userData, userProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from .forms import dataForm, editForm

# Create your views here.
@login_required
def manager_display(request,username):
    user_profile = get_object_or_404(userProfile,user=username )
    if request.user.username == username:
        try:
            user_data = userData.filter_decrypt(request,user=user_profile)
        except userData.DoesNotExist:
            user_data = None   
        return render(request,'manager/spass.html',{'user_data':user_data, 'username':username})
    else:
        return HttpResponseForbidden('Not Authorized')
    
@login_required
def add_site(request,username):

    if request.method =='POST':
        form = dataForm(request.POST)
        if form.is_valid():

            user_profile = userProfile.objects.get(user=username)
            user_data = form.save(commit=False)
            user_data.user = user_profile
            user_data.read_form(form.cleaned_data['username'],form.cleaned_data['email'],form.cleaned_data['password'],request)
            
            user_data.save()

            return redirect('password_manager', username= username)
    else:
        form = dataForm()



    return render(request, 'manager/add_site.html',{'form':form})

@login_required
def logout_manager(request):
    logout(request)
    return redirect('login')

@login_required
def user_settings(request,username):
    return render(request, 'manager/settings.html',{'username': username})

@login_required
def edit_site(request,username,entry_id):
    user_data = userData.objects.get(pk = entry_id)
    if request.method =='POST':
        form = editForm(request.POST)
        if form.is_valid():
            user_data.read_form(form.cleaned_data['dec_username'],form.cleaned_data['dec_email'],form.cleaned_data['dec_password'],request)
            user_data.site = form.cleaned_data['site']
            user_data.save()
            return redirect("password_manager", username = username)
    else:
        initial_data = user_data.decrypt_entry()
        form = editForm(initial=initial_data)

    return render(request, "manager/edit_site.html", {'form':form})    
