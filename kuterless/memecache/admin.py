from django.contrib import admin
from memecache.models import Account, Transaction, Purchase, Shop, Product, Cart, \
    ProductSelection, ItemVoucher

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'credit', 'created_at')
    
class TransactionAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'item_price', 'number_of_items', 'total_price', 'credit')
    ordering = [ 'account', 'created_at']



class PurchaseAdmin(admin.ModelAdmin):
    list_display = ( 'transaction', 'total_price')
    ordering = [ 'transaction', 'created_at']


class ShopAdmin(admin.ModelAdmin):
    list_display = ( 'admin_user', 'title', 'segment')
    ordering = [ 'created_at']


class ProductAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'updated_at')
    ordering = [ 'created_at']

class CartAdmin(admin.ModelAdmin):
    list_display = ( 'shop', 'customer', 'total_price')
    ordering = [ 'created_at', 'updated_at']

class ProductSelectionAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart')
    ordering = [ 'cart', 'updated_at']
    
class ItemVoucherAdmin(admin.ModelAdmin):
    list_display = ( 'product', 'customer')

        
admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Purchase, PurchaseAdmin)

admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(ProductSelection, ProductSelectionAdmin)
admin.site.register(ItemVoucher, ItemVoucherAdmin)


