from  django.contrib.auth.models import User
from rest_framework import  serializers

class RegisterSerializer(serializers.ModelSerializer):
    
    password_confirmation = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','password_confirmation')
        extra_kwargs = {'password': {'write_only': True}}
        
    def save(self):
        
        password =self.validated_data['password']
        password2 =self.validated_data['password_confirmation']
        
        if password != password2:
            raise serializers.ValidationError({'password': 'password  must be not match'})
        
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({'email': 'This email already exists'})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        
        return  account
        
        
        