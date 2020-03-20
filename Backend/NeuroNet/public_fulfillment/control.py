# -*- coding: utf-8 -*-
"""
This file contain the control services, used for all views
"""

#from coplay.models import UserProfile, Discussion, UserUpdate
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def func_name():
    return traceback.extract_stack(None, 2)[0][2]
    
def split_file_name_and_file_extention(filename):
   loc_of_dot = filename.find('.')
   name = filename[:loc_of_dot]
   extention = filename[loc_of_dot:]
   return name,extention
   
#http://source.mihelac.org/search/?q=ant
class ASCIIFileSystemStorage(FileSystemStorage):
    """
    Convert unicode characters in name to ASCII characters.
    """
    def get_valid_name(self, name):
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        return super(ASCIIFileSystemStorage, self).get_valid_name(name)


def simple_auth_token( key):
    if key is None:
        return None
    
    for user in User.objects.all():
        if user.auth_token.key == key:
            return user        
    return None
        
    



