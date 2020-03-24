from django.conf.urls import patterns, url
from memecache import views


urlpatterns = patterns('',
    url(r'root/$', views.root, name='root'),
    url(r'users_list/$', views.users_list, name='users_list'),
    url(r'^users_tag_list/(?P<pk>[0-9]+)/$', views.users_list, name='users_tag_list'),    
    url(r'instructions/$', views.instructions, name='instructions'),
    url(r'^shop_create/$', views.CreateShopView.as_view(), name='shop_create'),
    url(r'^shop_details/(?P<pk>[0-9]+)/$', views.shop_details, name='shop_details'),
    url(r'^shop_update/(?P<pk>[0-9]+)/$', views.UpdateShopView.as_view(), name='shop_update'),
    url(r'^product_create/(?P<pk>[0-9]+)/$', views.CreateProductView.as_view(), name='product_create'),
    url(r'^product_update/(?P<pk>[0-9]+)/$', views.UpdateProductView.as_view(), name='product_update'),
    url(r'^product_delete/(?P<pk>[0-9]+)/$', views.DeleteProductView.as_view(success_url='memecache:root'), name='product_delete'),
#    url(r'^product_list/(?P<pk>[0-9]+)/$', views.products_list, name='products_list'),

    
    url(r'prize_bag/$', views.prize_bag, name='prize_bag'),
    url(r'^products_list/(?P<pk>[0-9]+)/$', views.products_list, name='products_list'),
    
    url(r'^product_details/(?P<pk>[0-9]+)/$', views.product_details, name='product_details'),
    url(r'^update_product_selection/(?P<pk>[0-9]+)/$', views.update_product_selection, name='update_product_selection'),
    
    url(r'^cart_details/(?P<pk>[0-9]+)/$', views.cart_details, name='cart_details'),
    url(r'^cart_checkout/(?P<pk>[0-9]+)/$', views.cart_checkout, name='cart_checkout'),
    url(r'^account_details/(?P<pk>[0-9]+)/$', views.account_details, name='account_details'),
    url(r'^transaction_details/(?P<pk>[0-9]+)/$', views.transaction_details, name='transaction_details'),
    url(r'^purchase_details/(?P<pk>[0-9]+)/$', views.purchase_details, name='purchase_details'),
    url(r'^item_voucher_details/(?P<pk>[0-9]+)/$', views.item_voucher_details, name='item_voucher_details'),
    url(r'^item_voucher_send/(?P<pk>[0-9]+)/$', views.item_voucher_send, name='item_voucher_send'),
    url(r'^item_voucher_use/(?P<pk>[0-9]+)/$', views.item_voucher_use, name='item_voucher_use'),


#    url(r'^api/users/$', api.UserList.as_view(), name='api_discussion_list'),

#    url(r'^api/users/(?P<pk>[0-9]+)/$', api.UserDetail.as_view(), name='api_user'),

)

    
    
    