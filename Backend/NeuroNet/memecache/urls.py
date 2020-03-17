from django.urls import path
from memecache import views



urlpatterns = [
    path('root/', views.root, "root"),
    path('users_list/', views.users_list, "users_list"),
    path('users_tag_list/', views.users_list, "users_tag_list"),
    path('instructions/', views.instructions, "instructions"),
    path('shop_create/', views.CreateShopView.as_view(), "shop_create"),
    path('shop_details/<int:pk>/', views.shop_details, name="shop_details"),
    path('shop_update/<int:pk>/', views.UpdateShopView.as_view(), "shop_update"),
    path('product_create/<int:pk>/', views.CreateProductView.as_view(), "product_create"),
    path('product_update/<int:pk>/', views.UpdateProductView.as_view(), "product_update"),
    path('product_delete/<int:pk>/', views.DeleteProductView.as_view(success_url='memecache:root'), "product_delete"),
    path('prize_bag/', views.prize_bag, "prize_bag"),
    path('products_list/<int:pk>/', views.products_list, "products_list"),
    path('product_details/<int:pk>/', views.product_details, "product_details"),
    path('update_product_selection/<int:pk>/', views.update_product_selection, "update_product_selection"),
    path('cart_details/<int:pk>/', views.cart_details, "cart_details"),
    path('cart_checkout/<int:pk>/', views.cart_checkout, "cart_checkout"),
    path('account_details/<int:pk>/', views.account_details, "account_details"),
    path('transaction_details/<int:pk>/', views.transaction_details, "transaction_details"),
    path('purchase_details/<int:pk>/', views.purchase_details, "purchase_details"),
    path('item_voucher_details/<int:pk>/', views.item_voucher_details, "item_voucher_details"),
    path('item_voucher_send/<int:pk>/', views.item_voucher_send   , "item_voucher_send"),
    path('item_voucher_use/<int:pk>/', views.item_voucher_use    , "item_voucher_use"),
 ]
  