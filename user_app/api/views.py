from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from user_app.api.serializers import RegisterSerializer
from user_app import models
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def logout_view(request):
    # The request.method check is not needed here because @api_view(['POST']) ensures only POST requests are accepted
    request.user.auth_token.delete()  # Delete the user's token to log them out
    return Response({'success': 'Successfully logged out'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}  # Initialize the data dictionary
        
        if serializer.is_valid():
            account = serializer.save()  # Save the user and get the account object
            data['username'] = account.username
            data['email'] = account.email
            # token = Token.objects.create(user=account).key  # Create a new token for the user
            # data['token'] = token
            # return Response(data, status=status.HTTP_201_CREATED)
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
