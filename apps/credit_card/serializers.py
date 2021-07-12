from datetime import date
from rest_framework import serializers
from apps.credit_card.models import CreditCard

class CreditCardSerializer(serializers.ModelSerializer):
    def is_numeric(value: str):
        if not value.isnumeric():
            raise serializers.ValidationError("This field must be numeric")

    owner = serializers.CharField(read_only=True)
    card_number = serializers.CharField(min_length=16, max_length=16, required=True)
    cvc = serializers.CharField(min_length=3, max_length=3, required=True, validators=[is_numeric])
    expiry_month = serializers.IntegerField(min_value=1, max_value=12,required=True)
    expiry_year = serializers.IntegerField(min_value=date.today().year, required=True)

    class Meta:
        model = CreditCard
        fields = ('owner', 'owner_first_name', 'owner_last_name', 'alias', 'card_number', 'cvc', 'expiry_year', 'expiry_month')
