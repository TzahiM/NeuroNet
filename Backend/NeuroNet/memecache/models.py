# -*- coding: utf-8 -*-
from coplay.models import Segment
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone
from datetime import timedelta
# Create your models here.
MAX_TEXT = 2000
MAX_CART_ACTIVITY_SECONDS = 15 * 60

# Register your models here.
class Account(models.Model):
    user = models.OneToOneField(User, default = None, null=True, blank=True ,on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    credit     = models.PositiveIntegerField(default = 0)
    total_earn    = models.PositiveIntegerField(default = 0)
    total_spent   = models.PositiveIntegerField(default = 0)
    
    def __str__(self):
        return "id {}:{}- {} left ".format(self.id, self.user.username, self.credit)
    
    def get_absolute_url(self):
        return (
        reverse('memecache:account_details', kwargs={'pk': str(self.id)}) )

    def get_credit(self):
        return self.credit    
    
    def add_transaction(self, title, item_price, number_of_items, total_price = None, url = None):
        if total_price is None:
            total_price = item_price * number_of_items
        
        calculated_credit = self.credit + total_price
        
        if calculated_credit < 0:
            return None
        
        self.credit = calculated_credit

        if total_price > 0:
            self.total_earn =  self.total_earn + total_price
        else:
            self.total_spent = self.total_spent - total_price                 
        self.clean()
        self.save()
        
        transaction = self.transaction_set.create(account=self, title=title,
                                    item_price = item_price,
                                    number_of_items = number_of_items,
                                    total_price = total_price,
                                    credit = self.credit,
                                    url = url)
        transaction.clean()
        transaction.save()
        return transaction
        
    def deposit_and_return_transaction_if_ok(self, title, positive_item_price, number_of_items = 1, total_price = None, url = None):
        if positive_item_price >= 0 and number_of_items > 0:
            return self.add_transaction(title, positive_item_price, number_of_items, total_price, url)
        
        return None
            
    def withdraw_and_return_transaction_if_ok(self, title, positive_item_price, number_of_items = 1, total_price = None, url = None):
        if positive_item_price >= 0 and number_of_items > 0:
            return self.add_transaction(title, - positive_item_price, number_of_items, total_price, url)
        
        return None

            
    def print_content(self):
        print( 'Account for user', self.user.username, 'credit', self.credit , 'updated_at', self.updated_at, 'created_at', self.created_at, 'total_earn', self.total_earn, 'total_spent', self.total_spent )
        for tranaction in self.transaction_set.all().order_by("-created_at"):
            tranaction.print_content()
            

        
class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(_("title"), max_length=200)
    
    item_price       = models.IntegerField(default = 0)
    number_of_items  = models.PositiveIntegerField(default = 1)
    total_price      = models.IntegerField(default = 0)
    credit           = models.IntegerField(default = 0)
    
    url = models.CharField(_("url"),null=True, blank=True, default = None , max_length=200)
    

    def __str__(self):
        return "id {}:{}: {} * {} = {}".format( self.id, self.created_at, self.title, self.total_price, self.credit)
    
    def get_absolute_url(self):
        return (
        reverse('memecache:transaction_details', kwargs={'pk': str(self.id)}) )
    
    def print_content(self):
        print( 'Transaction updated_at', self.updated_at, 'created_at', self.created_at, 'item_price', self.item_price , 'number_of_items', self.number_of_items, 'total_price', self.total_price, 'credit', self.credit, 'cause', self.title, 'url', self.url)
        for purchase in self.purchase_set.all():
            purchase.print_content()

    
class Purchase(models.Model):
    transaction      = models.ForeignKey(Transaction,on_delete=models.CASCADE)
    total_price      = models.IntegerField()
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "id {}:{} {}".format( self.id, self.created_at, self.item_price)
    
    def get_absolute_url(self):
        return (
        reverse('memecache:purchase_details', kwargs={'pk': str(self.id)}) )
    
    def print_content(self):
        print( 'purchase updated_at', self.updated_at, 'created_at', self.created_at, 'total price', self.total_price)
        for item_voucher in self.itemvoucher_set.all():
            item_voucher.print_content()

            
class Shop(models.Model):
    segment = models.ForeignKey(Segment, default = None, null=True, blank=True,on_delete=models.CASCADE)
    admin_user         = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)    
    title = models.CharField("shop name", max_length=200)
    currency_name = models.CharField("coin name", default = 'MemeCash', max_length=200)
    description = models.TextField("Description", blank=True, null=True,
                                   validators=[MaxLengthValidator(MAX_TEXT)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "id {}:{}".format( self.id, self.title)

    def get_absolute_url(self):
        return (
        reverse('memecache:shop_details', kwargs={'pk': str(self.id)}) )

    def can_user_enter(self, user):
        if user.userprofile.get_segment() != self.segment:
            return False
        return True

    def get_cart(self, user, max_cart_inactivity_duration_seconds = MAX_CART_ACTIVITY_SECONDS):
        if self.can_user_enter(user):
            self.empty_unused_carts(max_cart_inactivity_duration_seconds)
            return self.cart_set.get_or_create( shop = self, customer = user)[0]
        return None
        
    def empty_unused_carts(self, max_cart_inactivity_duration_seconds = MAX_CART_ACTIVITY_SECONDS):
        now = timezone.now()
        oldest_active_cart_allowed = now - timedelta(seconds = max_cart_inactivity_duration_seconds)
        
        used_carts = self.cart_set.all().exclude( total_price = 0)
        for cart in used_carts:
            if cart.updated_at < oldest_active_cart_allowed: 
                cart.remove_all_items()
                self.delete_cart(cart)

    def delete_cart( self, cart):        
        for product in self.product_set.all():
            cart.take_items( product, 0)                
        cart.delete()
                      
    def checkout(self, user):
        if not self.can_user_enter(user):
            return
        cart = self.get_cart(user)
        transaction_title =  u'Purchase in ' + self.title
        transaction = user.account.withdraw_and_return_transaction_if_ok(title = transaction_title, 
                                                                         positive_item_price = cart.total_price, 
                                                                         number_of_items = 1, 
                                                                         url = self.get_absolute_url())
        if transaction:
            purchase = Purchase(transaction = transaction,
                                total_price = cart.total_price)
            purchase.save()
            for product_selection in cart.productselection_set.all():
                number_of_selected_items = product_selection.number_of_selected_items
                for item_index  in range(number_of_selected_items):
                    item_voucher =  ItemVoucher( shop = self, 
                                            product = product_selection.product,
                                            customer = user,
                                            purchase = purchase,
                                            price =  product_selection.product.item_price,
                                            used = False)
                    item_voucher.clean()
                    item_voucher.save()
                    
                product_selection.product.bought_items( product_selection.number_of_selected_items)
                
                product_selection.delete()
            
            cart.delete()
                    
    def can_item_voucher_be_marked_as_used(self, item_voucher):
        return ( self.can_user_enter(item_voucher.customer ) and  item_voucher.product.can_use() and item_voucher.used == False)
                
    def marked_item_voucher_as_used(self, item_voucher):
        if self.can_item_voucher_be_marked_as_used(item_voucher):
            item_voucher.used = True
            item_voucher.save()
        
    
    def print_content(self):
                
        print_string = 'shop name is ' + self.title
        
        print_string += 'admin name is ' + self.admin_user.username
        
        print_string = 'currency name is ' + self.currency_name
        
 
        if self.segment:
            print_string += 'segment is ' + self.segment.title
            
        
        print( print_string, 'number of products:', self.product_set.count())
        
        for product in self.product_set.all():
            product.print_content()
            
        print( 'carts')
        
        for cart in self.cart_set.all():
            cart.print_content()

            
            
class Product(models.Model):
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE)
    title = models.CharField("Product name", max_length=200)
    description = models.TextField("Description", blank=True, null=True,
                                   validators=[MaxLengthValidator(MAX_TEXT)])
    picture = models.ImageField( "A picture that describe the product",upload_to='uploads/%Y/%m/%d/', null=True, blank=True,default = None,
                                        max_length = 500000)

    item_price  = models.PositiveIntegerField("Price",default = 0)
    number_of_abailabale_items  = models.PositiveIntegerField("Availabale",default = 0)
    number_of_selected_items    = models.PositiveIntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_of_sale_at = models.DateTimeField("End of sale",null=True, blank=True,default = None)
    end_of_use_at  = models.DateTimeField("Valid until",null=True, blank=True,default = None)
    
    def __str__(self):
        return "id {}:{} {}".format( self.id, self.title, self.item_price)
    
    def get_absolute_url(self):
        return (
        reverse('memecache:product_details', kwargs={'pk': str(self.id)}) )
    
    
    
    def can_buy(self):
        if self.end_of_sale_at:
            if self.end_of_sale_at < timezone.now():
                return False
        return self.can_use()
    
    def can_use(self):
        if self.end_of_use_at:
            if self.end_of_use_at < timezone.now():
                return False
        return True
    
    def get_number_of_availabale_items(self):
        if not self.can_buy():
            return 0
        
        return  self.number_of_abailabale_items 
    
    def get_number_of_selected_items(self):
        if not self.can_buy():
            return 0
                    
        return ( self.number_of_selected_items )

    
    def select_items(self, number_of_items_diff):
        if number_of_items_diff <= self.get_number_of_availabale_items():
            self.number_of_abailabale_items -= number_of_items_diff
            self.number_of_selected_items += number_of_items_diff
            self.save()
    
    def bought_items(self, number_of_sold_items):        
        if self.get_number_of_selected_items()  >= number_of_sold_items:         
            self.number_of_selected_items -= number_of_sold_items
            self.save() 
    
    def print_content(self):
        print( 'product name' ,self.title , 'item_price', self.item_price, 'shop', self.shop.title, 'description', self.description, 'availabale items:', self.number_of_abailabale_items, 'selected', self.number_of_selected_items,  'sold', self.itemvoucher_set.filter(used = False).count(), 'used', self.itemvoucher_set.filter(used = True).count())
        print( 'created_at' , self.created_at , 'updated_at', self.updated_at, 'end_of_sale_at', self.end_of_sale_at, 'end_of_use_at', self.end_of_use_at )
        
        for procduct_selection in self.productselection_set.all():
            print( procduct_selection.print_content())
            
        
        for item in self.itemvoucher_set.all():
            item.print_content()
    
class Cart(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    customer         = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)
    total_price      = models.PositiveIntegerField(default = 0)

    class Meta:
        unique_together = (
            ('shop', 'customer'),
        )

    
    def __str__(self):
        return "id {}:{} {}".format( self.id, self.customer.username, self.total_price)
    
    def get_absolute_url(self):
        return (
        reverse('memecache:cart_details', kwargs={'pk': str(self.id)}) )
    
    

#    def get_product_selection_handle(self, product):
#        return self.productselection_set.get_or_create( cart = self, product = product)[0]

    def get_ramaining_customer_credit(self):
        return self.customer.account.get_credit() - self.total_price
    
    def get_cart_number_of_selected_items(self, product):
        if self.productselection_set.filter( product = product).count() != 0:            
            product_selection = self.productselection_set.get(product = product)
            return product_selection.number_of_selected_items
        return 0

    def set_cart_number_of_selected_items(self, product, new_number_of_selected_items):
        if new_number_of_selected_items != 0:
            productselection = self.productselection_set.get_or_create( cart = self, product = product)[0]
            productselection.number_of_selected_items = new_number_of_selected_items
            productselection.save()
        else:
            if self.productselection_set.filter( product = product).count() != 0:
                productselection = self.productselection_set.get( product = product)
                productselection.delete()
            
 
    def get_number_of_additional_items_to_select (self, product):
        if not product.can_buy():
            return 0
        
        remaining_items = product.get_number_of_availabale_items() 
        
        if self.get_ramaining_customer_credit() >= product.item_price and product.item_price != 0:
            remainind_items_to_select_whithin_credit = int (self.get_ramaining_customer_credit() /  product.item_price) 
        else:
            remainind_items_to_select_whithin_credit = 0
            
        
        if remaining_items < remainind_items_to_select_whithin_credit:
            return remaining_items
        
        return remainind_items_to_select_whithin_credit
        
        
    def can_take_items(self, product, new_number_of_items):
        current_selection = self.get_cart_number_of_selected_items(product)
        selection_diff = new_number_of_items - current_selection
        if self.get_number_of_additional_items_to_select( product) < selection_diff :
            return False
        return True        

    def take_items(self, product, new_number_of_items):
        if not self.can_take_items(product, new_number_of_items):
            return
        
        current_selection = self.get_cart_number_of_selected_items(product)
        selection_diff =   new_number_of_items - current_selection
        self.total_price +=  ( selection_diff * product.item_price)
        self.save()
        
        product.select_items( selection_diff)
        
        self.set_cart_number_of_selected_items(product, new_number_of_items)

                    
    def remove_all_items(self):
        for product_selection in self.productselection_set.all():
#            print( 'remove_all_items', product_selection.number_of_selected_items, 'of', product_selection.product.title, 'user', self.customer.username
            self.take_items(product_selection.product, 0)
#            product_selection.product.select_items( - product_selection.number_of_selected_items)
#            print( 'after pro sel', product_selection.product.number_of_abailabale_items
#            product_selection.delete()

        self.total_price = 0
        self.save()
        
    def get_total_price(self):
        return self.total_price
    
    
    def print_content(self):
        print( 'shop', self.shop.title, 'cart of', self.customer.username, 'current price:', self.total_price)
        for procduct_selection in self.productselection_set.all():
            print( procduct_selection.print_content())


            
class ProductSelection(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE)
    number_of_selected_items  = models.PositiveIntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ('product', 'cart'),
        )

    def __str__(self):
        return "id {}:{} {} {}".format( self.id, self.cart.customer.username, self.product.title, self.number_of_selected_items)
        
    def print_content(self):
        print( 'product selection of', self.product.title, 'user', self.cart.customer.username, 'selected items', self.number_of_selected_items)


    
class ItemVoucher (models.Model):
    shop    = models.ForeignKey(Shop, on_delete=models.CASCADE)    
    product = models.ForeignKey(Product, on_delete = models.SET_NULL,null=True)    
    customer         = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase         = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    price            = models.IntegerField()
    used             = models.BooleanField(default = False)    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "id {}:{} {} updated_at {}".format( self.id, self.product.title, self.customer.username,  self.updated_at)

    def get_absolute_url(self):
        return (
        reverse('memecache:item_voucher_details', kwargs={'pk': str(self.id)}) )
    

    
    def print_content(self):
                
        print( 'ItemVoucher from shop', self.shop.title, 'product', self.product.title, 'sold to', self.customer.username, 'at price', self.price, 'used', self.used)
