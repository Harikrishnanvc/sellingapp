from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from user.models import Register
from products.models import Post
from django.shortcuts import redirect
from django.contrib import messages



# Create your views here.
class UserProfileView(TemplateView):
    template_name = 'userprofile.html'

    def post(self, request):
        username = request.session['Username']
        userdetails = Register.objects.filter(username=username)
        return render(request, 'userprofile', {'userdetails': userdetails})

    def get(self, request):
        return render(request, 'userprofile.html')


#   User Details
class UserDetailsView(View):
    print('user details class')

    def post(self, request):
        return render(request, 'userprofile.html')

    def get(self, request):
        # username = request.user.username
        Username = request.session['Username']
        request.session['Username'] = Username
        userdetails = Register.objects.filter(Username=Username)
        return render(request, 'userprofile.html', {'userdetails': userdetails})


class EditProfileView(View):
    def post(self, request):
        return render(request, 'edit_profile.html')

    def get(self, request):
        Username = request.session['Username']
        request.session['Username'] = Username
        userdetails = Register.objects.filter(Username=Username)
        return render(request, 'edit_profile.html', {'userdetails': userdetails})


# passwordchange
def passwordchange(request):
    if request.method == "POST":
        Email = request.POST['Email']
        Fullname = request.POST['Fullname']
        Username = request.session['Username']
        print(Username)
        Phonenumber = request.POST['Phonenumber']
        DBpassword = Register.objects.get(Username=Username)
        DBpassword.Fullname = Fullname
        DBpassword.Email = Email
        DBpassword.Phonenumber = Phonenumber
        DBpassword.save()
        messages.success(request, "Password has been updated..")
        return redirect('edit_profile')
    else:
        return render(request, 'userprofile')


# logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


#   search bar
def searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        post = Post.objects.all().filter(Product_name = search)
        return render(request,'searchbar.html', {'post':post})