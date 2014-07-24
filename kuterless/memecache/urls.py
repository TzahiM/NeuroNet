from django.conf.urls import patterns, url
from memecache import views


urlpatterns = patterns('',
    url(r'^shop_details/(?P<pk>[0-9]+)/$', views.shop_details, name='shop_details'),
    url(r'^product_details/(?P<pk>[0-9]+)/$', views.product_details, name='product_details'),
    url(r'^cart_details/(?P<pk>[0-9]+)/$', views.cart_details, name='cart_details'),
    url(r'^account_details/(?P<pk>[0-9]+)/$', views.account_details, name='account_details'),
    url(r'^transaction_details/(?P<pk>[0-9]+)/$', views.transaction_details, name='transaction_details'),
    url(r'^purchase_details/(?P<pk>[0-9]+)/$', views.purchase_details, name='purchase_details'),
    url(r'^item_voucher_details/(?P<pk>[0-9]+)/$', views.item_voucher_details, name='item_voucher_details'),


#    url(r'^api/users/$', api.UserList.as_view(), name='api_discussion_list'),

#    url(r'^api/users/(?P<pk>[0-9]+)/$', api.UserDetail.as_view(), name='api_user'),

)

    
    
    