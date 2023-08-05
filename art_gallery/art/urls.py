from django.urls import path, re_path
from . import views
from .models import Art
from .views import SearchResultsView, ArtList, ArtDetail, ArtCheckoutView, PaymentComplete, cart, add_to_cart, \
    remove_from_cart, PracticeView, Compititionlist, ArtworkDetailView, HomeView, \
    Artcreate, OrderListView

urlpatterns =[
    path('',HomeView.as_view(),name='base'),

    path('login/',views.LoginPage,name='login'),
    re_path(r'^signup/$',views.SignupPage,name='signup'),

    path('artist_signup/',views.Adminsignup,name='artist_signup'),
    path('artist_login/',views.Adminlogin,name='artist_login'),

    path('user_nav/',views.UserHome,name='user_nav'),
    path('artist_home/',views.AdminHome,name='artist_home'),
    path('artcreate/',Artcreate.as_view(), name='artcreate'),

    path('orders/', OrderListView.as_view(), name='orders'),
    path("for_user/",views.User, name="for_user"),
    path("request_arts/",views.request_arts, name="request_arts"),

    path('for_admin/',views.Admin,name='for_admin'),
    path('about/', views.review, name='about'),
    path('search/',SearchResultsView.as_view(),name='search'),
    path('artlist/',ArtList.as_view(), name='artlist'),
    path('artdetails/<int:pk>/',ArtDetail.as_view(), name='artdetails'),

    path('cart/',cart, name='mycart'),
    path('cart/add/<int:art_id>/',add_to_cart, name="add_to_cart"),
    path('cart/remove/<int:art_id>/',remove_from_cart, name='remove_from_cart'),

    path("customerlist/",views.user_list, name="customerlist"),
    path("see_requested_arts/",views.see_requested_arts, name="see_requested_arts"),
    path("delete_requested_arts/delete_<int:pk>/",views.delete_requested_arts, name="delete_requested_arts"),

    path("customerlist/orders/<int:pk>/data/",views.data_view, name="data"),

    path('checkout/<int:pk>/',views.checkout, name='checkout'),
    path('buy/<int:pk>/', ArtCheckoutView.as_view(), name='buynow'),
    path('complete/<int:pk>/', PaymentComplete, name='complete'),

    path('compitition/', Compititionlist.as_view(), name='compitition'),
    path('artwork/<int:pk>/', ArtworkDetailView.as_view(), name='artwork'),
    path('practice/', PracticeView.as_view(), name='practice'),
    path('drawing/', views.drawing, name='drawing'),
]