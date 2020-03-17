# -*- coding: utf-8 -*-
# from coplay.control import post_update_to_user, string_to_email_subject, \
#     get_user_fullname_or_username, send_html_message_to_users
from coplay.control import send_html_message_to_users, post_update_to_user
from coplay.models import Discussion, Feedback, LikeLevel, Decision, Task, \
    Viewer, FollowRelation, UserUpdate
from coplay.services import get_user_fullname_or_username
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, User
from django.core.mail.message import EmailMessage
from django.urls import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.base import Template
from django.template.context import Context
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _
from django.views import generic
from django.views.generic import UpdateView, DeleteView, CreateView
from memecache.control import get_shop, get_product
from memecache.models import Product, Shop, Account, Cart, ItemVoucher
from taggit.models import Tag
import floppyforms as forms
from NeuroNet import settings

# Create your views here.





def root(request):
    if request.user.is_authenticated():
        segment_name = request.user.userprofile.get_segment_title()
        segment = request.user.userprofile.segment
    else:
        segment = None
        segment_name = u'האתר הציבורי'
    try:
        shop = Shop.objects.get(segment = segment)
    except Shop.DoesNotExist:
        return render(request, 'memecache/message.html', 
                      {  'message'      :  'עוד לא הוגדרה חנות',
                       'rtl': 'dir="rtl"'})
    
    try:
        shop = Shop.objects.get(segment = segment)
    except Shop.DoesNotExist:
        return render(request, 'memecache/message.html', 
                      {  'message'      :  u'עוד לא הוגדרה חנות',
                       'rtl': 'dir="rtl"'})
        
        
    return render(request, 'memecache/root.html',
                  {'shop': shop,
                   'segment_name': segment_name})

class UsersTableRow():
    place = 0
    user = None
    total_earn = 0

    

def users_list(request, pk = None):
    
    if request.user.is_authenticated():
        segment_name = request.user.userprofile.get_segment_title()
        segment = request.user.userprofile.segment
    else:
        segment = None
        segment_name = u'אתר הציבורי'
    try:
        shop = Shop.objects.get(segment = segment)
    except Shop.DoesNotExist:
        return render(request, 'memecache/message.html', 
                      {  'message'      :  u'עוד לא הוגדרה חנות',
                       'rtl': 'dir="rtl"'})
        
    page_name = u' '+ u'רשימת המשתתפים ב' + segment_name + u' '
    

    if pk is not None:
        try:
            tag_to_filter_by = Tag.objects.get(id = int(pk))
            page_name += u' בקטגורית ' + tag_to_filter_by.name
        except Tag.DoesNotExist:
            tag_to_filter_by = None
    
        
    currency_name = shop.currency_name
    account_list = Account.objects.order_by("-total_earn")
    users_rows_list = []
    place = 0
    
    for account in account_list:
        
        add_user = True
        if account.user.userprofile.segment != segment:
            add_user = False
                            
        if add_user:
            row = UsersTableRow()
            place += 1
            row.place = place
            row.user = account.user
            row.total_earn = account.total_earn
            users_rows_list.append(row)
        
    return render(request, 'memecache/users_list.html',
                  {'currency_name': currency_name,
                   'segment_name':  segment_name,
                   'users_rows_list': users_rows_list,
                   'page_name': page_name})


def instructions(request):
    if request.user.is_authenticated():
        segment_name = request.user.userprofile.get_segment_title()
        segment = request.user.userprofile.segment
    else:
        segment = None
        segment_name = 'אתר הציבורי'
    try:
        shop = Shop.objects.get(segment = segment)
    except Shop.DoesNotExist:
        return render(request, 'memecache/message.html', 
                      {  'message'      :  u'עוד לא הוגדרה חנות',
                       'rtl': 'dir="rtl"'})
    
  
    
    instructions_text = """

    על התחלת פעילות חדשה מקבלים         27
    על השלמת משימה עבור משתמש אחר        23
    על ביטול משימה עבור משתמש אחר        19
    על השלמת משימה עבור המשתמש עצמו        17
    על ביטול משימה עבור המשתמש עצמו        13
    על אישור עדכון של מצב משימות        11
    על תגובה בפעילות של משתמש אחר        7
    על פירסום רעיון להצבעה של מוביל פעילות        5
    על הצבעה על רעיון של מישהו אחר        3
    על צפייה בפעילות של מישהו אחר מקבלים         2
    """
        
    return render(request, 'memecache/instruction.html', {'shop':shop, 'instructions_text': instructions_text})



    
    
@login_required
def shop_details(request, pk):
    return HttpResponseRedirect(reverse('memecache:root'))


class PrizesOfAProduct():    
    id_name = ''
    product_title = ''
    item_voucher_list = []
    count = 0


@login_required
def prize_bag(request):
    user = request.user
    
    product_prize_list = []
    
    for product in Product.objects.all().order_by("title"):
        item_voucher_query_set = ItemVoucher.objects.filter( customer = user, used = False, product = product).order_by("id")
        if item_voucher_query_set.exists():
            product_prize = PrizesOfAProduct()
            product_prize.product_title = product.title
            product_prize.id_name = 'ProductSet'+ str(product.id)
            product_prize.item_voucher_list =  list( item_voucher_query_set)
            product_prize.count = len(product_prize.item_voucher_list)
            product_prize_list.append(product_prize)
        
    return render(request, 'memecache/prize_bag.html',
                  {'product_prize_list': product_prize_list})
    
@login_required
def products_list(request, pk):
    shop = get_shop(request.user, pk)
    if None == shop:
        return render(request, 'memecache/message.html', 
                      {  'message'      :  u'אין גישה לחנות',
                       'rtl': 'dir="rtl"'})
        
    product_list = shop.product_set.all().order_by("title")

    cart = shop.get_cart(request.user)
    
        
    return render(request, 'memecache/products_list.html',
                  {'shop': shop,
                   'product_list': product_list,
                   'cart': cart})

MAX_PRODUCT_SELECTION = 0
class SelectItemsForm(forms.Form):
#    number_of_selected_items = forms.IntegerField(label = u'מספר פריטים', min_value = 0, max_value = MAX_PRODUCT_SELECTION)
    max_value = 0
    number_of_selected_items = forms.IntegerField(label = '',  min_value = 0)


@login_required
def update_product_selection(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = SelectItemsForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            try:
                product = Product.objects.get(id=int(pk))
            except Task.DoesNotExist:
                return render(request, 'memecache/message.html', 
                      {  'message'      :  u'מוצר שאיננו קיים',
                       'rtl': 'dir="rtl"'})

            if request.user.userprofile.segment != product.shop.segment:
                return render(request, 'memecache/message.html', 
                      {  'message'      :  u'אין גישה למוצר',
                       'rtl': 'dir="rtl"'})
                
            cart = product.shop.get_cart(request.user)
            if cart == None:
                return render(request, 'memecache/message.html', 
                      {  'message'      :  u'אין גישה לקניה',
                       'rtl': 'dir="rtl"'})

            cart.take_items( product , form.cleaned_data['number_of_selected_items'])

            return HttpResponseRedirect(reverse('memecache:products_list', kwargs={'pk': product.shop.id}))


    return HttpResponseRedirect('memecache:root') # Redirect after POST
    
@login_required
def product_details(request, pk):
    product = get_product(request.user, pk)
    if None == product:
        return render(request, 'memecache/message.html', 
                      {  'message'      :  u'אין גישה לחנות',
                       'rtl': 'dir="rtl"'})
        
    cart = product.shop.get_cart(request.user)
    
    if cart == None:
        return render(request, 'memecache/message.html', 
                      {  'message'      :  u'אין גישה לחנות',
                       'rtl': 'dir="rtl"'})
        
    max_availabale_items = cart.get_cart_number_of_selected_items(product) + cart.get_number_of_additional_items_to_select( product )
    
    additional_items_to_select = cart.get_number_of_additional_items_to_select( product )

    MAX_PRODUCT_SELECTION = max_availabale_items  
    
    product_selection_form = SelectItemsForm( initial={'number_of_selected_items': cart.get_cart_number_of_selected_items(product),
                                                       'max_value': max_availabale_items}  )

    return render(request, 'memecache/product_details.html',
                  {'product': product,
                   'cart': cart,
                   'additional_items_to_select': additional_items_to_select,
                   'product_selection_form': product_selection_form,
                   'shop': product.shop})
    


class CreateShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = (
            'title',
            'description',
            'currency_name',
        )
        widgets = {
            'title': forms.Textarea(
                                attrs={'rows': '1', 'cols': '50'}),
            'description': forms.Textarea,
        }


class CreateShopView(CreateView):
    model = Shop
    form_class = CreateShopForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.admin_user = request.user
        self.segment = request.user.userprofile.segment
        
        return super(CreateShopView, self).dispatch(request, *args,
                                                              **kwargs)

    def form_valid(self, form):
        form.instance.admin_user = self.admin_user
        form.instance.segment = self.segment
        resp = super(CreateShopView, self).form_valid(form)
        

        return resp


class ShopOwnerView(object):
    model = Shop

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.shop = self.get_object()
        if self.shop.admin_user != request.user:
            return HttpResponse("Unauthorized", status=401)
        
        return super(ShopOwnerView, self).dispatch(request, *args,
                                                              **kwargs)

class UpdateShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = (
            'title',
            'description',
            'currency_name',
        )
        widgets = {
            'title': forms.Textarea(
                                attrs={'rows': '1', 'cols': '50'}),
            'description': forms.Textarea,
        }


        
class UpdateShopView(ShopOwnerView, UpdateView):
    
    form_class = UpdateShopForm
    template_name = 'memecache/shop_update.html'
    





class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'title',
            'description',
            'item_price',
            'number_of_abailabale_items',
            'end_of_sale_at',
            'end_of_use_at',

        
        )
        widgets = {
            'title': forms.Textarea(
                                attrs={'rows': '1', 'cols': '50'}),
            'description': forms.Textarea,
            'end_of_sale_at': forms.DateInput,
            'end_of_use_at': forms.DateInput,
        }


class CreateProductView( CreateView):
    model = Product
    form_class = ProductForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        segment = request.user.userprofile.segment
        self.shop = get_object_or_404(Shop, segment = segment)
        if self.shop.admin_user != request.user:
            return HttpResponse("Unauthorized", status=401)
        return super(CreateProductView, self).dispatch(request, *args,
                                                              **kwargs)

    def form_valid(self, form):
        form.instance.shop = self.shop
        resp = super(CreateProductView, self).form_valid(form)
        

        return resp



class UpdateProductView( UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'memecache/product_update.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        segment = request.user.userprofile.segment
        self.shop = get_object_or_404(Shop, segment = segment)
        if self.shop.admin_user != request.user:
            return HttpResponse("Unauthorized", status=401)
        return super(UpdateProductView, self).dispatch(request, *args,
                                                              **kwargs)

class DeleteProductView( DeleteView):

    model = Product

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        segment = request.user.userprofile.segment
        self.shop = get_object_or_404(Shop, segment = segment)
        if self.shop.admin_user != request.user:
            return HttpResponse("Unauthorized", status=401)
        return super(DeleteProductView, self).dispatch(request, *args,
                                                              **kwargs)



class ProductSelectionTableRow():
    product_name = ''
    unit_price = 0
    number_of_selected_items = 0
    total_price = 0


@login_required
def cart_details(request, pk):
    try:
        cart = Cart.objects.get(id = int(pk))
    except Cart.DoesNotExist:
        return render(request, 'memecache/message.html', 
                      {  'message'      :  'לא נמצאה עגלה',
                       'rtl': 'dir="rtl"'})
        
    
    procduct_selection_rows = []
    
    for procduct_selection in cart.productselection_set.all():
        row = ProductSelectionTableRow()
        row.product_name = procduct_selection.product.title
        row.unit_price = procduct_selection.product.item_price
        row.number_of_selected_items = procduct_selection.number_of_selected_items
        row.total_price = row.unit_price * row.number_of_selected_items        
        procduct_selection_rows.append(row)
        
    return render(request, 'memecache/cart_details.html',
                  {'cart': cart,
                   'procduct_selection_rows':  procduct_selection_rows})
    
    
    
@login_required
def cart_checkout(request, pk):
    try:
        cart = Cart.objects.get(id = int(pk))
    except Cart.DoesNotExist:
        return render(request, 'memecache/message.html', 
                      {  'message'      :  u'לא נמצאה עגלה',
                       'rtl': 'dir="rtl"'})
        
    cart.shop.checkout(request.user)    
            
    return HttpResponseRedirect(reverse('memecache:prize_bag'))
    
    
    
@login_required
def account_details(request, pk):
    return HttpResponse('account_details ' +pk)
@login_required
def transaction_details(request, pk):
    return HttpResponse('transaction_details ' +pk)
@login_required
def purchase_details(request, pk):
    return HttpResponse('purchase_details ' + pk)

@login_required
def item_voucher_details(request, pk):
    
    try:
        item_voucher = ItemVoucher.objects.get(id = int(pk))
    except ItemVoucher.DoesNotExist:
        return render(request, 'memecache/message.html', 
                      {  'message'      :  u'פרס לא קיים',
                       'rtl': 'dir="rtl"'})
        
    if None == get_product( request.user, str( item_voucher.product.id)):
        return render(request, 'memecache/message.html', 
                      {  'message'      :  u'אין גישה לחנות',
                       'rtl': 'dir="rtl"'})
        
    return render(request, 'memecache/item_voucher_details.html',
                  {'item_voucher': item_voucher})
        

@login_required
def item_voucher_send(request, pk):
    
    try:
        item_voucher = ItemVoucher.objects.get(id = int(pk))
    except ItemVoucher.DoesNotExist:
        return render(request, 'memecache/message.html', 
                      {  'message'      :  u'פרס לא קיים',
                       'rtl': 'dir="rtl"'})
        
    if None == get_product( request.user, str( item_voucher.product.id)):
        return render(request, 'memecache/message.html', 
                      {  'message'      :  u'אין גישה לחנות',
                       'rtl': 'dir="rtl"'})

    if item_voucher.customer != request.user:
        return render(request, 'memecache/message.html', 
                      {  'message'      :  u'זה לא הפרס שלך',
                       'rtl': 'dir="rtl"'})

    
    sender_name = get_user_fullname_or_username(request.user)
         
    html_message = render_to_string("memecache/email_voucher_use.html",
                                    {'ROOT_URL': settings.SITE_URL,
                                     'sender_name': sender_name,
                                     'item_voucher': item_voucher})
    
    to_users_list = [item_voucher.shop.admin_user]
    
    send_html_message_to_users(u'מימוש פרס של ' + sender_name, html_message, to_users_list)
    
    
    post_update_to_user(item_voucher.shop.admin_user.id, u'מימוש פרס של ' + sender_name,  details_url = item_voucher.get_absolute_url())

        
    return render(request, 'memecache/message.html', 
                      {  'message'      :  u'הפרס נשלח למימוש',
                       'rtl': 'dir="rtl"'})

@login_required
def item_voucher_use(request, pk):
    
    try:
        item_voucher = ItemVoucher.objects.get(id = int(pk))
    except ItemVoucher.DoesNotExist:
        return render(request, 'memecache/message.html', 
                      {  'message'      :  u'פרס לא קיים',
                       'rtl': 'dir="rtl"'})
        
    if None == get_product( request.user, str( item_voucher.product.id)):
        return render(request, 'memecache/message.html', 
                      {  'message'      :  u'אין גישה לחנות',
                       'rtl': 'dir="rtl"'})
        
    if item_voucher.used:
        return HttpResponseRedirect(
                item_voucher.get_absolute_url())
        

    item_voucher.shop.marked_item_voucher_as_used(item_voucher)

        
    return render(request, 'memecache/item_voucher_details.html',
                  {'item_voucher': item_voucher,
                   'just_used': True})
        
    
    

    

"""
memcache Ooosh
product list
product create
product update
product details
product selection
cart
my coupons
coupon details





"""
