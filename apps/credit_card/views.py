from rest_framework import viewsets
from apps.credit_card.models import CreditCard
from apps.credit_card.serializers import CreditCardSerializer, CreditCardUpdateSerializer
from apps.credit_card.permissions import IsOwner


class CreditCardView(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = (IsOwner, )

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return CreditCardUpdateSerializer
        return CreditCardSerializer
    
    def get_queryset(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CreditCard.objects.filter(owner=self.request.user)
        return CreditCard.objects.all()

    def perform_create(self, serializer: CreditCardSerializer):
        serializer.save(owner=self.request.user)