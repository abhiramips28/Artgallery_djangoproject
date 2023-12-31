from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView

from .models import Art, Order, Admin, Cart, CartItem, Request_Art, Artworks, Compitition


# Create your views here.

class HomeView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def SignupPage(request):

        if request.method == "POST":
            unname = request.POST.get('username')
            email = request.POST.get('email')
            pass1 = request.POST.get('password1')
            pass2 = request.POST.get('password2')

            if pass1 != pass2:
                return HttpResponse("Your password and conform password are not Same!!")
            else:
                my_user = User.objects.create_user(unname,email,pass1)
                my_user.save()
                return redirect('login.html')
        return render(request, 'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('artlist')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def Adminsignup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            name = request.POST['name']
            email_id = request.POST['email_id']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if len(username) > 15:
                messages.info(request, "Username must be under 15 characters.")
                return redirect('/artist_signup')
            if not username.isalnum():
                messages.info(request, "Username must contain only letters and numbers.")
                return redirect('/artist_signup')
            if password1 != password2:
                messages.info(request, "Passwords do not match.")
                return redirect('/artist_signup')

            admin = Admin.objects.create_user(username, email_id, password1)
            admin.name = name

            admin.save()
            return render(request, 'artist_login.html')
    return render(request, "artist_signup.html")

def Adminlogin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            user_username = request.POST['user_username']
            user_password = request.POST['user_password']

            user = authenticate(username=user_username, password=user_password)

            if user is not None:
                login(request, user)
                messages.success(request, "Successfully Logged In")
                return redirect("/artist_home")
            else:
                messages.error(request, "Please provide a valid username and password")
    return render(request, "artist_login.html")


def UserHome(request):
    return render(request,'user_nav.html')

def AdminHome(request):
    return render(request,'artist_home.html')

class Artcreate(CreateView):
    model = Art
    fields = ['title,artist,category,description,price,image_url,Stock']
    success_url = reverse_lazy('artlist')
    template_name = 'artcreate.html'



class SearchResultsView(ListView):
    model = Art
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('Q')
        return Art.objects.filter(
            Q(category=query)
        )

class ArtList(ListView):
    model = Art
    context_object_name = 'arts'
    template_name = 'artlist.html'


class ArtDetail(DetailView):
    model = Art
    context_object_name = 'arts'
    template_name = 'artdetails.html'

class ArtCheckoutView(DetailView):
    model = Art
    template_name = 'buy.html'


def PaymentComplete(request,pk):
    product = Art.objects.get(id=pk)
    Order.objects.create(
        product=product
    )
    return JsonResponse('Payment Completed',safe=False)


@login_required
def cart(request):
    cart_qs = Cart.objects.filter(user=request.user)
    if cart_qs.exists():
        cart_obj = cart_qs.first()
        cart_items = CartItem.objects.filter(cart=cart_obj)
    else:
        cart_obj = None
        cart_items = []

    context = {
        'cart':cart_obj,
        'cart_items':cart_items
    }
    return render(request,'mycart.html',context)


@login_required
def add_to_cart(request,art_id):
    arts = get_object_or_404(Art,id=art_id)
    cart_qs = Cart.objects.filter(user=request.user)
    if cart_qs.exists():
        cart_obj = cart_qs.first()
    else:
        cart_obj = Cart.objects.create(user=request.user ,total_price=Decimal('0.00'))
    cart_item, created = CartItem.objects.get_or_create(arts=arts ,cart=cart_obj)
    if not created:
        cart_item.quantity +=1
        cart_item.save()
    cart_obj.total_price += Decimal(str(arts.price))
    cart_obj.save()
    return redirect('mycart')

@login_required
def remove_from_cart(request,art_id):
    arts = get_object_or_404(Art,id=art_id)
    cart_qs = Cart.objects.filter(user=request.user)
    if cart_qs.exists():
        cart_obj = cart_qs.first()
        cart_item_qs = CartItem.objects.filter(arts=arts,cart=cart_obj)
        if cart_item_qs.exists():
            cart_item = cart_item_qs.first()
            if cart_item.quantity >1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
            cart_obj.total_price -= Decimal(str(arts.price))
            cart_obj.save()
    return redirect('mycart')


def Admin(request):
    arts = Art.objects.all()
    total_arts = arts.count()
    return render (request, "for_admin.html", {'arts':arts, 'total_arts':total_arts})

def Delete_Arts(request, myid):
    arts = Art.objects.get(id=pk)
    if request.method == "POST":
        arts.delete()
        return redirect('/add_arts')
    return render(request, 'delete_art.html', {'arts':arts})





def User(request):
    arts = Art.objects.all()
    total_arts = arts.count()
    return render (request, "for_user.html", {'arts':arts, 'total_arts':total_arts})

def Add_Arts(request):
    if request.method=="POST":
        form = ArtForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "add_arts.html")
    else:
        form=ArtForm()
    return render(request, "add_arts.html", {'form':form})

def request_arts(request):
    if request.method=="POST":
        user = request.user
        art_title = request.POST['art_title']
        artist = request.POST['artist']
        art = Request_Art(user=user, art_title=art_title, artist=artist)
        art.save()
        thank = True
        return render(request, "request_arts.html", {'thank':thank})
    return render(request, "request_arts.html")

def see_requested_arts(request):
    requested_art = Request_Art.objects.all()
    requested_arts_count = requested_art.count()
    return render(request, "see_requested_arts.html", {'requested_art':requested_art, 'requested_arts_count':requested_arts_count})

def delete_requested_arts(request,pk):
    delete_art = Request_Art.objects.get(id=pk)
    if request.method == "POST":
        delete_art.delete()
        return redirect('/see_requested_arts')
    return render(request, "delete_requested_arts.html", {'delete_art':delete_art})

def user_list(request):
    user = Order.objects.all()
    user_count = user.count()
    return render(request, "customerlist.html", {'user':user, 'user_count':user_count})

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = context['orders'].filter(user=self.request.user)
        return context

def data_view(request,pk):
    orders = Order.objects.get(id=pk)
    return JsonResponse(request, {'data':orders.items_json})


def checkout(request,pk):
    checkout = Art.objects.get(id=pk)

    if request.method=="POST":
        user = request.user
        items = request.POST.get('items', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        order = Order(user=user, items=items, name=name, email=email, address=address, phone=phone)
        order.save()
        thank = True

        context ={
            'checkout': checkout,
            'thank': thank,

        }
        return render(request, 'buy.html', context)
    return render(request, 'checkout.html')


class Compititionlist(ListView):
    model = Artworks
    context_object_name = 'compitition'
    template_name = 'compitition.html'


class ArtworkDetailView(DetailView):
    model = Artworks
    template_name = 'artwork.html'

class PracticeView(CreateView):
    model = Compitition
    fields = ['name', 'email', 'feedback', 'image_url']
    success_url = reverse_lazy('artlist')
    template_name = 'practice.html'

def drawing(request):
    return render(request, 'drawing.html')

def review(request):
    return render(request, 'about.html')
