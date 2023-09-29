import hashlib, base64
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login,logout
from .forms import CreateUser, PinForm
from .models import userProfile
from manager.models import userData,genSettings
from django.contrib.auth.decorators import login_required

# Create your views here.

class LoginScreen(LoginView):
    template_name ='login/login.html'
    def get(self,request,*args,**kwargs):
        if self.request.user.is_authenticated:
            logout(request)
        return super().get(request,*args,**kwargs)
    
    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        user = form.get_user()
        login(self.request,user)
        print(self.request.session,'SESION CHECK-----------------------------------------')


        user_profile = userProfile.objects.get(user=user)
        key = base64.b64encode(hashlib.pbkdf2_hmac('sha512',form.cleaned_data.get('password').encode(),bytes(user_profile.salt), iterations=1000, dklen=64)).decode()
        self.request.session['key'] = key
        self.request.session.save()

        pin_url = reverse('decryption_pin',args=[user.username])
        return redirect(pin_url)
        
        
    

def register(request):
    if request.method =='POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user_profile = userProfile.objects.create(user=username)
            genSettings.objects.create(user=user_profile)
            user = form.save(commit=False)
            user.save()

            key = base64.b64encode(hashlib.pbkdf2_hmac('sha512',form.cleaned_data.get('password1').encode(),bytes(user_profile.salt), iterations=1000, dklen=64)).decode()
            login(request,user)
            request.session['key'] = key
            request.session.save()
            create_pin_url = reverse('create_pin', args=[username])

            return redirect(create_pin_url)    
    else:
        form = CreateUser()
    return render(request, 'login/create_user.html',{'form':form})

@login_required
def create_pin(request,username):
    if request.method =='POST':
        form = PinForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data.get('pin')
            user_profile = userProfile.objects.get(user = username)

            request.session['KDFP'] = base64.b64encode(hashlib.pbkdf2_hmac('sha512', bytes(user_profile.salt) + pin.encode() + bytes(user_profile.salt) + base64.b64decode(request.session['key'].encode()),bytes(user_profile.salt),iterations=1000, dklen=32)).decode()
            del request.session['key']

            manager_url = reverse('password_manager', args =[username])
            user_profile.hash_pin(pin = pin)
            user_profile.save()
            return redirect(manager_url)
    else:
        form = PinForm()
    return render(request, 'login/decrypt_pin.html', {'form':form})

@login_required
def enter_pin(request,username):
    if request.method == 'POST':
        print(request.user,'pin')
        form = PinForm(request.POST)
        if form.is_valid():
            user_profile = userProfile.objects.get(user = username)
            print('user_profile:', user_profile)
            pin = form.cleaned_data.get('pin')
            manager_url = reverse('password_manager', args =[username])
            print(manager_url)

            if user_profile.check_pin(pin = pin):
                key = hashlib.pbkdf2_hmac('sha512',  bytes(user_profile.salt) + pin.encode() +  bytes(user_profile.salt) + base64.b64decode(request.session['key'].encode()),bytes(user_profile.salt),iterations=1000, dklen=32)
                del request.session['key']

                request.session['KDFP'] = base64.b64encode(key).decode()
                print(request.session['KDFP'])
                return redirect(manager_url)
        else:
            print('form errors:', form.errors)
    else:
        form = PinForm()
    return render(request, 'login/decrypt_pin.html',{'form':form})
                



            


