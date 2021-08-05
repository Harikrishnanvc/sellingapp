from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from plaster.compat import urlparse

from .models import Register
from products.models import Post
from django.shortcuts import redirect
from django.core.mail import send_mail
from sellingapp.settings import EMAIL_HOST_USER
from django.contrib import messages
import uuid
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class WelcomeView(TemplateView):
    template_name = 'welcome.html'

    def welcome(self, request):
        return render(request, 'welcome.html')
def send_email_after_registeration(Email, Token):
    Subject = 'Verify your email'
    Message = 'The link to verify your email is {0}'.format(f'http://localhost:8000/account-verify/{Token}')
    Recepient = str(Email)
    send_mail(Subject, Message, EMAIL_HOST_USER, [Recepient], fail_silently=False)
    return redirect('register')


# register page
class RegisterView(View):
    def post(self, request):
        Fullname = request.POST['Fullname']
        Username = request.POST['Username']
        Email = request.POST['Email']
        DBEmail = Register.objects.filter(Email=Email)
        Password = request.POST['Password']
        Phonenumber = request.POST['Phonenumber']
        Confirm_password = request.POST.get('Confirm_password')
        if Password == Confirm_password:
            if len(DBEmail) == 0:
                uid = uuid.uuid4()
                Register(Fullname=Fullname, Username=Username, Email=Email, Password=Password, Phonenumber=Phonenumber,
                         Token=uid).save()
                send_email_after_registeration(Email,uid)
                messages.success(request, 'A verification link is sent to ' + request.POST['Email'] + " please verify")
                return render(request, 'register.html')
            else:
                messages.success(request, 'Email already exist ' + request.POST['Email'])
                return render(request, 'register.html')

        else:
            messages.success(request, 'Password is not matching ')
            return render(request, 'register.html')

    def get(self, request):
        return render(request, 'register.html')


def account_verify(request, Token):
    pf = Register.objects.filter(Token=Token).first()
    pf.Verify = True
    pf.save()
    messages.success(request, 'Your account is verified ')
    return redirect('login')

# login page
class LoginPageView(View):
    def post(self, request):
        if request.method == "POST":
            try:
                Userdetails = Register.objects.get(Email=request.POST['Email'], Password=request.POST['Password'],)
                request.session['Username'] = Userdetails.Username
                request.session['Fullname'] = Userdetails.Fullname

                if Userdetails.Verify == 1:
                    return redirect('post_list')
                else:
                    messages.success(request,'Account is not verified !')
                    return render(request,'login.html')
            except Register.DoesNotExist as e:
                messages.success(request, 'Username / password is invalid')

            return render(request, 'login.html')
        else:
            return render(request, 'login.html')

    def get(self, request):
        return render(request, 'login.html')




#forgot password
class ForgotPasswordView(TemplateView):
    template_name = 'reset_password.html'


#email authentication

# EMAIL AUTHENTICATION for forgot password
class EmailAuthenticationView(View):
    def post(self,request):
        if request.method == "POST":
            Emailid = request.POST.get('Email')
            DBEmail = Register.objects.filter(Email=Emailid)
            if len(DBEmail) == 0:
                messages.success(request, 'Email does not exist ' + request.POST['Email'])
                return render(request, 'reset_password.html')
            Subject = 'Password Reset'
            Message = 'The link to reset your password is {0}'.format('http://localhost:8000/changepassword?Email='+Emailid)
            Recepient = str(Emailid)
            send_mail(Subject, Message, EMAIL_HOST_USER, [Recepient], fail_silently=False)
        messages.success(request, 'An Email has been sent, please check. ')
        return render(request, 'reset_password.html')
    def get(self, request):
        return render(request, 'reset_password.html')

#password change
class PasswordChangeView(View):
    def post(self,request):
        url_get = urlparse.urlparse(request.POST['Email'])
        Useremail = urlparse.parse_qs(url_get.query)['Email'][0]
        if request.method == "POST":
            try:
                Email = Useremail
                Password = request.POST['Password']
                confirmpassword = request.POST['CPassword']
                if Password == confirmpassword:
                    DBpassword = Register.objects.get(Email=Email)
                    DBpassword.Password = Password
                    DBpassword.confirmpassword = Password
                    DBpassword.save()
                    messages.success(request, "Password has been updated..")
                    return redirect('login')

                else:
                    messages.success(request, "Password is not matching")
                    return redirect('changepassword?Email='+Useremail)
            except Register.DoesNotExist as e:
                messages.success(request, 'Enter a registerd email')
                return render(request, 'changepassword.html?Email='+Useremail)

        else:
            return render(request, 'changepassword.html?Email='+Useremail)
    def get(self, request):
        return render(request, 'changepassword.html')