# -*- coding: utf-8 -*-
from coplay.control import init_user_profile
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from memecache.control import init_user_account
from memecache.models import Transaction, Shop, Product, ItemVoucher, Purchase, \
    Cart
import time


# Create your tests here.

class MemeCacheTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user('admin', 'admin@example.com',
                                              'secret')
        self.at1 = User.objects.create_user('at1', 'user1@example.com',
                                              'secret')
        self.at2 = User.objects.create_user('at2', 'user2@example.com',
                                              'secret')
        self.at3 = User.objects.create_user('at3', 'user2@example.com',
                                              'secret')
        
        
        init_user_profile(self.admin)
        init_user_profile(self.at1)
        init_user_profile(self.at2)
        init_user_profile(self.at3)
        
        init_user_account(self.admin)
        init_user_account(self.at1)
        init_user_account(self.at2)
        init_user_account(self.at3)

    
    def test_transactins(self):
        print 'test_transactins'
        self.assertEquals(0, Transaction.objects.count())
        self.assertEquals(0, self.at1.account.get_credit())
        self.assertNotEquals(None , self.at1.account.deposit_and_return_transaction_if_ok( "add 12", 12))
        self.assertNotEquals(None  , self.at1.account.deposit_and_return_transaction_if_ok( "add 20", 20, url='www.hp.com'))
        self.assertEquals(None , self.at1.account.deposit_and_return_transaction_if_ok( "add -20", -20))
        self.assertNotEquals(None  , self.at1.account.withdraw_and_return_transaction_if_ok( "withdraw 2", 2))
        self.assertEquals(None , self.at1.account.withdraw_and_return_transaction_if_ok( "withdraw -2", -2))
        self.assertEquals(None , self.at1.account.withdraw_and_return_transaction_if_ok( "withdraw 200", 200))
        self.assertEquals(30 , self.at1.account.get_credit())
        transaction_2nd =  self.at1.account.transaction_set.all()[1]
        self.assertEquals("add 20" , transaction_2nd.title )
        self.assertEquals(20 , transaction_2nd.total_price )
        self.assertEquals(32 , transaction_2nd.credit )
        self.assertEquals('www.hp.com' , transaction_2nd.url )

        self.assertNotEquals(None  , self.at2.account.deposit_and_return_transaction_if_ok( "add 1000", 1000))
        self.assertNotEquals(None  , self.at2.account.withdraw_and_return_transaction_if_ok( "withdraw 300", 300))
        self.assertNotEquals(None  , self.at1.account.deposit_and_return_transaction_if_ok( "add 300", 300))
        self.assertEquals(330 , self.at1.account.get_credit())
        self.assertEquals(700 , self.at2.account.get_credit())
        
#        self.assertEquals(0 , self.at1.account.total_earn)
#        self.assertEquals(0 , self.at1.account.total_spent)
#        self.assertEquals(0 , self.at2.account.total_earn)
#        self.assertEquals(0 , self.at2.account.total_spent)
        
        self.at1.account.print_content()
        self.at2.account.print_content()
        
    def test_shop(self):
        print 'test_shop'
        
        self.assertEquals(0, Shop.objects.count())
        shop = Shop( admin_user = self.admin, 
                     title =  'shop 1',
                     currency_name = 'zugi',
                     description = 'shop description')
        shop.save()

        self.assertEquals(1, Shop.objects.count())
        
        
        p1 = Product( shop = shop,
                      title = 'p1',
                      description = 'p1 desc',
                      item_price  = 10,
                      number_of_abailabale_items  = 10,
                      number_of_selected_items    = 0 )
        p1.save()
        p2 = Product( shop = shop,
                      title = 'p2',
                      description = 'p2 desc',
                      item_price  = 20,
                      number_of_abailabale_items  = 100,
                      number_of_selected_items    = 0 )
        p2.save()             
                            
        
        self.assertEquals(2, Product.objects.filter( shop = shop).count())
        
        at1_cart = shop.get_cart(self.at1)
        
        self.assertNotEquals(None , at1_cart)
        
        self.assertEquals(False, at1_cart.can_take_items( p1, 3 ) )# no credit
        self.at1.account.credit = 3000
        self.at1.account.save()
        
        at1_cart = shop.get_cart(self.at1)
        
        self.assertEquals(True, at1_cart.can_take_items( p1, 3 ) )
        
        
        
        self.assertEquals(False, at1_cart.can_take_items( p1, 20 ) )#not enough availabale items
        self.assertEquals(True, at1_cart.can_take_items( p1, 10 ) )
        
        
        at2_cart = shop.get_cart(self.at2)
        self.at2.account.credit = 100
        self.at2.account.save()
        
        p3_initial_selected_items = 10
        
        p3 = Product( shop = shop,
                      title = 'p3',
                      description = 'p3 desc',
                      item_price  = 22,
                      number_of_abailabale_items  = 50,
                      number_of_selected_items    = p3_initial_selected_items )
        p3.save()
                     
        at2_cart = shop.get_cart(self.at2)
        
        p3_first_selected_items = 2
        self.assertEquals(True , at2_cart.can_take_items(p3, p3_first_selected_items) )
        at2_cart.take_items( p3 , p3_first_selected_items)
        at2_cart = shop.get_cart(self.at2)
                  
       
        self.assertEquals(44, at2_cart.total_price )
        
        self.assertEquals(56, at2_cart.get_ramaining_customer_credit() )
        
        self.assertEquals(2, at2_cart.get_number_of_additional_items_to_select( p3 ) )#returned according to remainng credit

        self.at2.account.credit = 2000
        self.at2.account.save()
        at2_cart = shop.get_cart(self.at2)
        
        self.assertEquals(48, at2_cart.get_number_of_additional_items_to_select( p3 ) )#returned according to number_of_abailabale_items

        at1_cart = shop.get_cart(self.at1)
                
        at1_cart.take_items( p1, 10 )
        self.assertEquals(0, p1.get_number_of_availabale_items() )
        at2_cart = shop.get_cart(self.at2)
        
        self.assertEquals(False, at2_cart.can_take_items( p1, 5 ) )#at1 got all items

        at1_cart = shop.get_cart(self.at1)
        
        
        at1_cart.take_items( p1, 2 )
        
        self.assertEquals(8, p1.get_number_of_availabale_items() )
        
        at2_cart = shop.get_cart(self.at2)
        
        self.assertEquals(True, at2_cart.can_take_items( p1, 5 ) )
        
        at1_cart = shop.get_cart(self.at1)
        at1_cart = shop.get_cart(self.at1)
        at1_cart.take_items( p1, 10 )        
        time.sleep(3)        
        
        at2_cart = shop.get_cart(self.at2, max_cart_inactivity_duration_seconds =  1)
        p1 = Product.objects.get( id = p1.id)# i do not know why this it is a must ?
        p1.print_content()
        
        self.assertEquals(True, at2_cart.can_take_items(p1, 10) )
        
        self.assertEquals(1, shop.cart_set.count() )
        
        self.assertEquals(10 , p1.get_number_of_availabale_items() )                                     
                     
        at2_cart.take_items( p1, 6)
         
        self.assertEquals(4 , p1.get_number_of_availabale_items() )                                     

        self.assertEquals(6 , p1.get_number_of_selected_items() )                                     
        
        at2_cart = shop.get_cart(self.at2)
        
        at2_cart.take_items( p2, 60)

        at1_cart = shop.get_cart(self.at1)
                     
        at1_cart.take_items( p1, 2)
        at1_cart = shop.get_cart(self.at1)
                             
        at1_cart.take_items( p2, 10)
        
        p1.number_of_abailabale_items = 100
        p1.save()
        p2.number_of_abailabale_items = 200
        p2.save()
        p3.number_of_abailabale_items = 300
        p3.save()
        
        at_1_p1_items = 10
        at_1_p2_items = 11
        at_1_p3_items = 22
        
        at1_cart = shop.get_cart(self.at1)
        at1_cart.take_items( p1, at_1_p1_items)
        
        at1_cart = shop.get_cart(self.at1)
        at1_cart.take_items( p2, at_1_p2_items)
        
        at1_cart = shop.get_cart(self.at1)
        at1_cart.take_items( p3, at_1_p3_items)

        at_2_p1_items = 0
        at_2_p2_items = 10
        at_2_p3_items = 20

        at2_cart = shop.get_cart(self.at2)
        at2_cart.take_items( p1, at_2_p1_items)
        at2_cart = shop.get_cart(self.at2)
        at2_cart.take_items( p2, at_2_p2_items)
        at2_cart = shop.get_cart(self.at2)
        at2_cart.take_items( p3, at_2_p3_items)

        p1_availabale = p1.get_number_of_availabale_items()
        p2_availabale = p2.get_number_of_availabale_items()
        p3_availabale = p3.get_number_of_availabale_items()
        
        print p1_availabale, p2_availabale, p3_availabale
        
        at1_cart = shop.get_cart(self.at1)
        at1_total_cart_price = at1_cart.get_total_price()
        self.assertEquals(804 , at1_total_cart_price ) #10 * 10 + 11 * 20 + 22 * 22
        
        at1_credit = self.at1.account.credit
        self.assertEquals(3000 , at1_credit )
        
        print p1.get_number_of_selected_items(), 'zugo'
        print p2.get_number_of_selected_items(), 'zugo'
        print p3.get_number_of_selected_items(), 'zugo'
        print 'before  shop', shop.print_content()
        
        shop.checkout(self.at1)
        
        print 'after  shop', shop.print_content()
        print p1.get_number_of_selected_items(), 'zugo'
        print p2.get_number_of_selected_items(), 'zugo'
        print p3.get_number_of_selected_items(), 'zugo'

        p1 = Product.objects.get( id = p1.id)# i do not know why this it is a must ?
        p2 = Product.objects.get( id = p2.id)# i do not know why this it is a must ?
        p3 = Product.objects.get( id = p3.id)# i do not know why this it is a must ?

        self.assertEquals(at1_credit - at1_total_cart_price , self.at1.account.credit )# 3000 - 804

        self.assertEquals(p1_availabale , p1.get_number_of_availabale_items())
        self.assertEquals(p2_availabale , p2.get_number_of_availabale_items())
        self.assertEquals(p3_availabale , p3.get_number_of_availabale_items())
        
        self.assertEquals( at_2_p1_items , p1.get_number_of_selected_items())
        self.assertEquals( at_2_p2_items , p2.get_number_of_selected_items())
        self.assertEquals( at_2_p3_items + p3_initial_selected_items + p3_first_selected_items, p3.get_number_of_selected_items())


        
        transaction = Transaction.objects.get( account = self.at1.account)
        purchase = Purchase.objects.get( transaction = transaction)
 
        self.assertEquals(at_1_p1_items + at_1_p2_items + at_1_p3_items, ItemVoucher.objects.filter( customer = self.at1, shop = shop, used = False, purchase = purchase).count())
        self.assertEquals(at_1_p2_items , ItemVoucher.objects.filter( product = p2).count())
        self.assertEquals(at_1_p3_items , ItemVoucher.objects.filter( product = p3).count())
        
        
        at_1_p1_items_2nd = 18
        cart = shop.get_cart( self.at1)
        cart.take_items( p1, at_1_p1_items_2nd)

        shop.checkout(self.at1)

        self.assertEquals(at1_credit - at1_total_cart_price  - (p1.item_price * at_1_p1_items_2nd), self.at1.account.credit )# 3000 - 804 - (18 * 10)

        

        at1_transactions = Transaction.objects.all().filter( account = self.at1.account)
        
        self.assertEquals(2 , at1_transactions.count())
        
        self.assertEquals( - p1.item_price * at_1_p1_items_2nd , at1_transactions.last().total_price)
        
        
        shop.checkout(self.at2)
        
        purchase = Purchase.objects.last()

        self.assertEquals( 30 , purchase.itemvoucher_set.all().count())
        
        p1.end_of_sale_at = timezone.now()
        p1.save()
                
        
        self.assertEquals(False, at2_cart.can_take_items( p1, 10) )
        
        p1.end_of_sale_at = timezone.now() + timezone.timedelta( seconds=5 )
        p1.save()

        self.assertEquals(True, at2_cart.can_take_items( p1, 10) )
        
        items = ItemVoucher.objects.all()
        self.assertEquals(True, shop.can_item_voucher_be_marked_as_used( items[0]) )

        shop.marked_item_voucher_as_used( items[0])
        
        self.assertEquals(True, shop.can_item_voucher_be_marked_as_used( items[1]) )
        
        p1.end_of_use_at = timezone.now() 
        p1.save()

        self.assertEquals(False, shop.can_item_voucher_be_marked_as_used( items[1]) )
        
        p1.end_of_use_at = timezone.now() + timezone.timedelta( seconds=5 )
        p1.save()

        self.assertEquals(True, shop.can_item_voucher_be_marked_as_used( items[1]) )

     
        
