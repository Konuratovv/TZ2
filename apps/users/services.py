from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .models import CustomUser



class LoginService:

    def find_user(self, request):
        return CustomUser.objects.filter(email=request.data['email']).first()
    
    def check_user(self, request, user):
        if user is None:
            raise AuthenticationFailed("User not found!")
        
        if not user.check_password(request.data["password"]):
            raise AuthenticationFailed('Incorrect password')
        
    def give_token(self, user):
        return AccessToken.for_user(user), RefreshToken.for_user(user)
        
        
