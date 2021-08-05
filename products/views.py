from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.views.generic import ListView
from django.views.generic import DetailView
from products.models import Post
from products.models import Buyer
from user.models import Register
from products.models import Seller
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from sellingapp.settings import EMAIL_HOST_USER
from twilio.rest import Client

#   Create your post
class CreatePostView(View):
    def post(self, request):
        if request.method == "POST":
            Product_name = request.POST['Product_name']
            Productdescription = request.POST['Product_description']
            Product_category = request.POST['Product_category']
            image = request.FILES['Product_image']
            Product_price = request.POST['Product_price']
            Username = request.session['Username']
            Post(Product_name=Product_name, Product_description=Productdescription, Product_category=Product_category,
                 Product_image=image, Product_price=Product_price, Product_status=1, Username=Username).save()
            messages.success(request, "Successfully posted")
            return redirect('post_list')

        return render(request, 'post_list')

    def get(self, request):
        return render(request, 'create_post.html')

#   Home page product list
def Product_list(request):
    post_list = Post.objects.all()
    return render(request, 'homepage.html', {'post_list': post_list})


#   product view by id
class BuyProductView(View):
    def get(self, request, id):
        Product_details = Post.objects.filter(id=id)
        request.session['Product_id'] = id
        request.session['Seller_username'] = Product_details[0].Username
        request.session['Product_name'] = Product_details[0].Product_name
        return render(request, 'product/buy.html', {'Product_details': Product_details})

#   Product buy and send mail to buyer
class GetBuyerDetailsView(View):
    def post(self, request):
        if request.method == "POST":
            Username_buyer = request.session['Username']
            Product_name = request.session['Product_name']
            Product_id = request.session['Product_id']
            Buyer_price = request.POST['Buyer_price']
            existing_data = Buyer.objects.filter(Username_buyer=Username_buyer, Product_id=Product_id)
            print(len(existing_data))
            if len(existing_data)==0:
                Buyer(Username_buyer=Username_buyer, Product_id=Product_id, Buyer_price=Buyer_price, Product_name=Product_name).save()
                seller_details = Register.objects.filter(Username = request.session['Seller_username'])
                seller_fullname = seller_details[0].Fullname
                username = request.session['Username']
                userdetails = Register.objects.filter(Username=username)
                Buyer_email = userdetails[0].Fullname
                Emailid = seller_details[0].Email
                Subject = 'Buyer'
                Message = f'{Buyer_email} has shown interest in {Product_name} for the price {Buyer_price}'
                Recepient = str(Emailid)
                send_mail(Subject, Message, EMAIL_HOST_USER, [Recepient], fail_silently=False)

                messages.success(request, "An email has been sent to the seller, please wait for the response ")
            else:
                messages.success(request, "Already applied for this product")
            return redirect('post_list')
        return render(request, 'post_list')

    def get(self, request):
        return render(request, 'post_list')

#   My product
class MyProductsView(View):
    def get(self, request):
        Seller_username = request.session['Username']
        my_products = Post.objects.filter(Username=Seller_username)
        return render(request,'product/my_products.html', {'my_products':my_products})


#   My Product view by id
class SellProductView(View):
    def get(self, request, id):
       Product_details = Post.objects.filter(id=id)
       request.session['My_product_id']=id
       return render(request, 'product/Sell.html', {'Product_details': Product_details } )




class EditProductView(View):
    def get(self, request):
       id = request.session['My_product_id']
       Product_details = Post.objects.filter(id=id)
       return render(request, 'product/edit_product.html', {'Product_details': Product_details } )


# Edit Products
def Edit_product(request):
    if request.method == "POST":
        Product_name = request.POST['Product_name']
        Product_description = request.POST['Product_description']
        Product_category = request.POST['Product_category']
        Product_price = request.POST['Product_price']
        Productimage = request.FILES['Productimage']
        Product_edit = Post.objects.get(id=request.session['My_product_id'])
        Product_edit.Product_name = Product_name
        Product_edit.Product_description = Product_description
        Product_edit.Product_category = Product_category
        Product_edit.Product_price = Product_price
        Product_edit.Product_image = Productimage

        Product_edit.save()
        messages.success(request, "Successfully updated Product details")
        return redirect('edit_product_view')
    else:
        return render(request, 'product/Sell.html')


#   Delete Product
def Delete_Product(request,):
    delete_product = Post.objects.filter(id=request.session['My_product_id'])
    delete_product.delete()
    messages.success(request, "Post deleted")
    return redirect('my_products')



#   List of buyers
class BuyerListView(View):
    def get(self, request, id):
       Product_details = Buyer.objects.filter(Product_id=id)
       try:
             Buyer_email = Register.objects.get(Username=Product_details[0].Username_buyer)
             return render(request, 'product/buyer_list.html', {'Buyer_list': Product_details})
       except:
           messages.success(request,'No buyers for this product !')
           return render(request,'product/buyer_list.html')





#   sell the product from buyers list
class SellProduct(View):
    def get(self,request, id):
        #   sending mail to buyer
        Sell_details = Buyer.objects.filter(id=id)
        Product_info = Post.objects.get(id=Sell_details[0].Product_id)
        Seller_email = Register.objects.get(Username=Product_info.Username)
        Buyer_email = Register.objects.get(Username = Sell_details[0].Username_buyer)

        Emailid = Buyer_email.Email
        Subject = f'Approval for buying {Product_info.Product_name}'
        Message = f'{Seller_email.Fullname} has approved to buy {Product_info.Product_name} for the price {Sell_details[0].Buyer_price}.\n Contact seller : Phonenumber: {Seller_email.Phonenumber} \n Email id: {Seller_email.Email}'
        Recepient = str(Emailid)
        send_mail(Subject, Message, EMAIL_HOST_USER, [Recepient], fail_silently=False)

        #   sending sms to seller
        account_sid = 'AC5fd96e5c16d47416cecc71f1adc084da'
        auth_token = '898a55639b097f0800503baa1c9b3b20'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f'Contact info: {Buyer_email.Fullname}\n Phonenumber: {Buyer_email.Phonenumber} \n Email id: {Buyer_email.Email}',
            from_='+14844303220',
            to=f'+{Seller_email.Phonenumber}',)
        Product_info.Product_status = 0
        Product_info.save()
        Buyer_name = Buyer_email.Username
        Product_id = Product_info.id
        Seller(Buyer_name=Buyer_name, Product_id=Product_id).save()
        messages.success(request, "An sms has been sent to you and an email has been sent to the buyer")
        return redirect('post_list')

class IntoAppliedProducts(View):
    def get(self, request):
        Username_buyer = request.session['Username']
        applied_products = Buyer.objects.filter(Username_buyer=Username_buyer)
        li = []
        new_list = []
        for i in applied_products:
            product_details = Post.objects.get(id=i.Product_id)
            li.append(product_details)
            # seller = Seller.objects.get(Product_id=i.Product_id)
            # new_list.append(seller)
        Buyer_username = request.session['Username']
        return render(request, 'product/applied_products.html', {'applied_products': applied_products,'product_details':li, 'seller':Buyer_username})
