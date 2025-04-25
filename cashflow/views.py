from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from cashflow.models import Status, CashFlow
from cashflow.serializers import StatusSerializer, CashFlowRecordSerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated]


class CashFlowRecordViewSet(viewsets.ModelViewSet):
    serializer_class = CashFlowRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['date', 'status', 'type', 'category', 'subcategory']
    ordering_fields = ['date', 'amount']

    def get_queryset(self):
        return CashFlow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
