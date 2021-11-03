from rest_framework import permissions
from django.core.cache import cache
from enum import Enum

class IsUserAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """    
    def has_permission(self, request, view):
        header = request.META.get('HTTP_AUTHORIZATION')
        if header is not None:
            user_token = header.split(' ')[1]
            result = isUserauthenticated(user_token)
            if result is not None:
                # set the requested user
                request.user = isUserauthenticated(user_token)['user']
                return True
        return False


#  mock user cache server
from users.models import UserProfile
def isUserauthenticated(token):
    user = None
    try:
        # here, request to the user cache is made to see if user is in the cache
        user = cache.get(token)
    except:
        pass
    return user



# represent user permission for a resourse
class IPermissions(Enum):
    CREATE = 'c'
    READ = 'r'
    UPDATE = 'u'
    DELETE = 'd'

# default permission message to unauthorized user
permission_denied_error_message = "Sorry, you don't have permission to \
                                    perform this operation. Contact the admin for permission"