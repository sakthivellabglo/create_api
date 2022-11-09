from django.urls import path, include
from django.contrib.auth.decorators import login_required

from product import views


urlpatterns = [path('all/',views.Allproducts.as_view(), name='all'),
               path('search/', views.search_api,name='search_results'),
               path("accounts/", include("django.contrib.auth.urls")),
               path("cart/", login_required(views.ListCartItem.as_view()), name='cart'),
               path("add_to_card/<int:Product_id>",views.Add_to_cart, name="add_to_cart"),
               path("add_quntity/<int:product_id>",views.add_quntity, name="add_quntity"),
               path('remove/<int:Cart_id>/', views.cart_remove, name='cart_remove'),
              # path("add_to_order", views.add_order, name="add_to_order"),
               path("order", views.Orderproducts.as_view(), name='order'),
               path("orderhistory", views.Orderhistory.as_view(), name='orderhistory'),
               path('order_remove/<int:Cart_id>/<int:order_id>', views.order_remove, name='order_remove'),
               path("placeorder", views.order_place, name='order_place'),
               path("wishlist/<int:Product_id>/",views.add_wishlist,name = 'wishlist'),
               path("wishall", login_required(views.Wishproducts.as_view()), name='wish'),
               path("rm_wish/<int:Product_id>/", views.rm_wishlist, name='rm_wish'),
               path('product_api/', views.product_api, name='product_api') ,
               path('cart_api/', views.cart_api, name='cart_api') ,
               path('order_api/', views.order_api, name='order_api') ,
               path('webhook/', views.webhook, name='webhook') ,
               path('checkout/', views.checkout, name='checkout') ,
               path('paymentsuccess/',views.paymentsuccess,name='payment-success'),
               path('paymentcancel/',views.paymentcancel,name='payment-cancel'),
               ]
