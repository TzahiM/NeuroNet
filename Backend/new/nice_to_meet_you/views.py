from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from .models import *
from .control import get_sound_to_play_name, get_buisness_card_name
# Create your views here.



def home(request):
    return render(
        request,
        'nice_to_meet_you/index.html',
        {}
    )

@login_required
def view_cards (request):
    return render(request, 'nice_to_meet_you/view_cards.html', 
                      {  'cards_list'   :  BusinessCard.objects.all(),})


def scanned_user (request):
    message = request.GET.get('message')

#    tts_object = gTTS( text = message, lang='en', slow=False)
#    tts_object.save("media/latest_message.mp3")

#OK    return HttpResponseRedirect('http://127.0.0.1:8000/media/zzz.mp3')
    return render(request, 'nice_to_meet_you/message.html', 
                      {  'message'      :  message,
                       'rtl': 'dir="rtl"'})


def view_card(request, pk):
    try:
        business_card = BusinessCard.objects.get(id=int(pk))
    except BusinessCard.DoesNotExist:
        return None
    return render(request, 'nice_to_meet_you/view_card.html', 
                      {  'card'   :  business_card,})
                       
def scan_card(request, pk):
    try:
        business_card = BusinessCard.objects.get(id=int(pk))
    except BusinessCard.DoesNotExist:
        return None
    

#    message_to_play_text = 'my name is ' + business_card.private_name + ' ' + business_card.family_name + ' nice to meet you'
    message_to_play_text = 'ding ding ding ' + business_card.private_name + ' ' + business_card.family_name 
    if request.user.is_authenticated:
        message_to_play_text = 'It is very nice to meet you, ' + request.user.get_full_name() + ' my name is ' + business_card.private_name + ' ' + business_card.family_name 

#    message_to_play_text = 'ting'
    new_acquaintance = Acquaintance(business_card = business_card, message =  message_to_play_text)
    new_acquaintance.save()
    business_card.score += 1
    business_card.save()

    
#    return HttpResponseRedirect( '/media/contacts.vcf')
    return HttpResponseRedirect( '/'+ get_buisness_card_name(business_card.id) )

    
def get_message(request):
    copyfile("media/latest_message.mp3", "media/message_to_play.mp3")
    copyfile("media/empty.mp3", "media/latest_message.mp3")

    return HttpResponseRedirect("http://127.0.0.1:8000/media/message_to_play.mp3")
#    return HttpResponseRedirect('http://127.0.0.1:8000/media/latest_message.mp3')
    
def get_latest_message(request):
    if Acquaintance.objects.count() is 0:
        return HttpResponseRedirect( '/media/audio_messages/empty.mp3' )
#        return None
    
    acquaintance = Acquaintance.objects.all().order_by("-updated_at").first()
    if acquaintance.is_played:
        return HttpResponseRedirect( '/media/audio_messages/empty.mp3' )
#        return None
    acquaintance.is_played = True
    acquaintance.save()
    return HttpResponseRedirect( '/'+ get_sound_to_play_name(acquaintance.id) )
#    dst_file_name = 'media/'+ get_sound_to_play_name(acquaintance.id)
#    copyfile( get_sound_to_play_name(acquaintance.id), dst_file_name)
#    return HttpResponseRedirect( '/'+ dst_file_name )
     

def message_board(request):
    return render(request, 'nice_to_meet_you/message_board.html')


                   
class CardHoldersTableRow():
    place = 0
    card_holder = None
    score = 0

def scoring_board(request):
    card_holders_list = BusinessCard.objects.order_by("-score")
    card_holders_rows_list = []
    place = 0
    
    for card_holder in card_holders_list:
        if card_holder.score != 0:        
            row = CardHoldersTableRow()
            place += 1
            row.place = place
            row.card_holder = card_holder
            row.score = card_holder.score
            card_holders_rows_list.append(row)
        
    return render(request, 'nice_to_meet_you/card_holders_list.html',
                  {'card_holders_rows_list': card_holders_rows_list})



def scoring_clear(request):

    card_holders_list = BusinessCard.objects.all()
    for card_holder in card_holders_list:
        card_holder.score = 0     
        card_holder.save()

    return HttpResponseRedirect( '/ntmu/scoring_board' ) 
    



