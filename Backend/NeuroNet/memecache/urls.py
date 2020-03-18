from django.urls import path
from memecache import views



urlpatterns = [
    path('root/', views.root, name="root"),
    path('users_list/', views.users_list, name="users_list"),
    path('users_tag_list/', views.users_list, name="users_tag_list"),
    path('instructions/', views.instructions, name="instructions"),
    path('shop_create/', views.CreateShopView.as_view(), name="shop_create"),
    path('shop_details/<int:pk>/', views.shop_details, name="shop_details"),
    path('shop_update/<int:pk>/', views.UpdateShopView.as_view(), name="shop_update"),
    path('product_create/<int:pk>/', views.CreateProductView.as_view(), name="product_create"),
    path('product_update/<int:pk>/', views.UpdateProductView.as_view(), name="product_update"),
    path('product_delete/<int:pk>/', views.DeleteProductView.as_view(success_url='memecache:root'), name="product_delete"),
    path('prize_bag/', views.prize_bag, name="prize_bag"),
    path('products_list/<int:pk>/', views.products_list, name="products_list"),
    path('product_details/<int:pk>/', views.product_details, name="product_details"),
    path('update_product_selection/<int:pk>/', views.update_product_selection, name="update_product_selection"),
    path('cart_details/<int:pk>/', views.cart_details, name="cart_details"),
    path('cart_checkout/<int:pk>/', views.cart_checkout, name="cart_checkout"),
    path('account_details/<int:pk>/', views.account_details, name="account_details"),
    path('transaction_details/<int:pk>/', views.transaction_details, name="transaction_details"),
    path('purchase_details/<int:pk>/', views.purchase_details, name="purchase_details"),
    path('item_voucher_details/<int:pk>/', views.item_voucher_details, name="item_voucher_details"),
    path('item_voucher_send/<int:pk>/', views.item_voucher_send   , name="item_voucher_send"),
    path('item_voucher_use/<int:pk>/', views.item_voucher_use    , name="item_voucher_use"),
 ]
  