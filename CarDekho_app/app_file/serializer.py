from rest_framework import serializers
from .. models import Carlist,Showroomlist,Review



class ReviewSerializer(serializers.ModelSerializer):
    User = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        # exclude = ('car',)
        fields = "__all__"  

class CarSerializers(serializers.ModelSerializer):
    
    discounted_price = serializers.SerializerMethodField()
    Review = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Carlist
        fields = "__all__"
        # exclude = ['name']

    def get_discounted_price(self, obj):
        if hasattr(obj, 'price'):
            dis = obj.price - 5000
            return dis
        return None

    
    def validate_price(self, value):
        if value <= 200000.00:
            raise serializers.ValidationError("The price must be grater than 200000.00")
        return value
    
    def validate(self,data):
        if data ['name'] == data['description']:
            raise serializers.ValidationError("Name and Description should not be same")
        return data

class ShowroomSerializer(serializers.ModelSerializer):
    showroom = CarSerializers(many = True , read_only = True)
    class Meta:
        model = Showroomlist
        fields = "__all__"
