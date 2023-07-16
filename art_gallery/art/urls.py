from django.urls import path
from . import views
from .views import SearchResultsView, ArtList, ArtDetail, ArtCheckoutView, PaymentComplete, cart, add_to_cart, \
    remove_from_cart, PracticeView, Compititionlist, ArtworkDetailView

urlpatterns =[
    path('',views.base,name='base'),
    path('signup/', views.Usersignup, name="signup"),
    path('userlogin/', views.User_login, name="userlogin"),
    path('admin_signup/',views.Adminsignup,name='admin_signup'),
    path('adminlogin/',views.Adminlogin,name='adminlogin'),
    path('logout/',views.Logout,name='logout'),

    path('user_nav/',views.UserHome,name='user_nav'),
    path('admin_home/',views.AdminHome,name='admin_home'),
    path('orders/',views.orders_list, name='orders'),
    path("for_user/",views.User, name="for_user"),
    path("request_arts/",views.request_arts, name="request_arts"),

    path('for_admin/',views.Admin,name='for_admin'),

    path('search/',SearchResultsView.as_view(),name='search_results'),
    path('artlist/',ArtList.as_view(), name='artlist'),
    path('artdetails/<int:pk>/',ArtDetail.as_view(), name='artdetails'),

    path('cart/',cart, name='mycart'),
    path('cart/add/<int:art_id>/',add_to_cart, name="add_to_cart"),
    path('cart/remove/<int:art_id>/',remove_from_cart, name='remove_from_cart'),

    path("customerlist/",views.user_list, name="customerlist"),
    path("see_requested_arts/",views.see_requested_arts, name="see_requested_arts"),
    path("delete_requested_arts/delete_<int:myid>/",views.delete_requested_arts, name="delete_requested_arts"),
    path("customerlist/orders/<int:myid>/",views.orders_list, name="orders_list"),
    path("customerlist/orders/<int:myid>/data/",views.data_view, name="data"),

    path('checkout/<int:pk>/', ArtCheckoutView.as_view, name='checkout'),
    path('complete/<int:pk/', PaymentComplete, name='complete'),

    path('compitition/', Compititionlist.as_view(), name='compitition'),
    path('artwork/<int:pk>/', ArtworkDetailView.as_view(), name='artwork'),
    path('practice/', PracticeView.as_view(), name='practice'),
    path('drawing/', views.drawing, name='drawing'),
]