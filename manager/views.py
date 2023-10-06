from django.shortcuts import render, get_object_or_404, redirect
from .models import userData, userProfile, Websites, genSettings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponseForbidden
from .forms import dataForm, editForm, editPasscode,editPin
import hashlib, base64
from grab_favicon import download_favicon
from django.core.files import File

# Create your views here.
def manager_display(request,username):
    user_profile = get_object_or_404(userProfile,user=username )
    if request.user.username == username:
        try:
            user_data = userData.filter_decrypt(request,user=user_profile)
        except userData.DoesNotExist:
            user_data = None   
        return render(request,'manager/spass.html',{'user_data':user_data,'username':username})
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
            user_data.url= user_data.url.split("//")[-1].split("/")[0]
            user_data.url = "https://" + user_data.url
            website, created = Websites.objects.get_or_create(user=user_profile, url=user_data.url)
            user_data.website = website
            user_data.save()

            if created or not website.icon:
                user_data.url = user_data.url.split("//")[-1].split("/")[0]
                download_favicon(user_data.url, size=64,path='manager/favicons/',silent=True)
                website.icon.save(f'{user_data.site}.png',  File(open('manager/favicons/' + f'{user_data.url}.png', 'rb')),save=True)
                user_data.url = "https://" + user_data.url
                website.url = user_data.url
                website.save()
                user_data.save()

            return redirect('password_manager', username=username)
    else:
        form = dataForm()
        user_profile = userProfile.objects.get(user=username)
        gen_settings = genSettings.objects.get(user=user_profile)
        context = model_to_dict(gen_settings)
        context['form'] = form
        context['username'] = username

    return render(request, 'manager/add_site.html',context)

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
            user_data.url = form.cleaned_data['url']
            user_data.save()
            return redirect("password_manager", username = username)
    else:
        initial_data = user_data.decrypt_entry(request)
        form = editForm(initial=initial_data)
        user_profile = userProfile.objects.get(user=username)
        gen_settings = genSettings.objects.get(user=user_profile)
        context = {
            'form': form,
            'username': username,
            'entry_id': entry_id,
            **model_to_dict(gen_settings)
        }


    return render(request, "manager/edit_site.html", context)

@login_required
def delete_site(request,username,entry_id):
    user_data = userData.objects.get(pk = entry_id)
    user_data.delete()
    return redirect("password_manager", username = username)

@login_required
def change_pass(request,username):
    user_profile = userProfile.objects.get(user = username)
    if request.method =='POST':
        form = editPasscode(request.POST, user=request.user)
        if form.is_valid():
            user = User.objects.get(username=username)

            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            update_session_auth_hash(request,user)

            user_data = userData.filter_decrypt(request, user = user_profile)
            new_hash = base64.b64encode(hashlib.pbkdf2_hmac('sha512',form.cleaned_data['new_password1'].encode(),bytes(user_profile.salt), iterations=1000, dklen=64)).decode()
            request.session['KDFP'] =  base64.b64encode(hashlib.pbkdf2_hmac('sha512',  bytes(user_profile.salt) + form.cleaned_data['pin'].encode() +  bytes(user_profile.salt) + base64.b64decode(new_hash),bytes(user_profile.salt),iterations=1000, dklen=32)).decode()  
            for data in user_data:
                data.read_form(data.username, data.email,data.password,request)
                data.save()
                
                

            return redirect('password_manager',username = username)

    else:
        form = editPasscode(user=request.user)
    
    return render(request, 'manager/edit_pass.html', {'form': form,'username':username})

@login_required
def change_pin(request,username):
    user_profile = userProfile.objects.get(user = username)

    if request.method == 'POST':
        form = editPin(request.POST,user=request.user)
        if form.is_valid():
            pin = form.cleaned_data['new_pin']
            user_data = userData.filter_decrypt(request, user = user_profile)
            user_profile.hash_pin(pin)
            user_profile.save()
            new_hash = base64.b64encode(hashlib.pbkdf2_hmac('sha512',form.cleaned_data['passcode'].encode(),bytes(user_profile.salt), iterations=1000, dklen=64)).decode()
            request.session['KDFP'] =  base64.b64encode(hashlib.pbkdf2_hmac('sha512',  bytes(user_profile.salt) + pin.encode() +  bytes(user_profile.salt) + base64.b64decode(new_hash),bytes(user_profile.salt),iterations=1000, dklen=32)).decode()
            for data in user_data:
                data.read_form(data.username, data.email,data.password,request)
                data.save()

            return redirect('password_manager',username = username)


    else:
        form = editPin(user=request.user)

    return render(request, 'manager/edit_pin.html',{'form':form,'username':username})

def generate_password(request,username):
    user_profile = userProfile.objects.get(user=username)
    gen_settings = genSettings.objects.get(user=user_profile)
    context = model_to_dict(gen_settings)
    context['username'] = username

    return render(request, 'manager/gen_pass.html',context)

def gen_settings(request,username):
    user_profile = userProfile.objects.get(user=username)
    gen_settings = genSettings.objects.get(user=user_profile)
    context = model_to_dict(gen_settings)
    context['username'] = username

    return render(request, 'manager/gen_settings.html', context)


def save_settings(request,username):
    if request.method =='POST':
        user_profile = userProfile.objects.get(user=username)
        gen_settings = genSettings.objects.get(user = user_profile)
        gen_settings.length = request.POST.get('length')
        gen_settings.readable = request.POST.get('readable')
        gen_settings.uppercase = bool(request.POST.get('uppercase'))
        gen_settings.lowercase = bool(request.POST.get('lowercase'))
        gen_settings.numbers = bool(request.POST.get('numbers'))
        gen_settings.symbols = bool(request.POST.get('symbols'))
        gen_settings.separate = bool(request.POST.get('separate'))
        gen_settings.words = bool(request.POST.get('words'))
        gen_settings.save()
    

    return redirect('password_manager',username = username)

    
        

