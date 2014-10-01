# -*- coding: utf-8 -*-
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

        
@api_view(['GET'])
def get_server_time(request, format=None):
    content = {
        'server_time': timezone.now(),
    }
    
    return Response(content)

