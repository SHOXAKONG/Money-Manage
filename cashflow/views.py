from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from cashflow.models import Status, CashFlow
from cashflow.serializers import StatusSerializer, CashFlowRecordSerializer
from rest_framework.response import Response
from .serializers import StatsSerializer
from django.db.models import Sum


class StatusViewSet(viewsets.ModelViewSet):
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Status.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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


class FilteredStatsViewSet(viewsets.GenericViewSet):
    serializer_class = StatsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CashFlow.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        category_id = request.query_params.get('category_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        type_id = request.query_params.get('type_id')
        status_id = request.query_params.get('status_id')

        queryset = self.get_queryset()

        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if type_id:
            queryset = queryset.filter(type__id=type_id)
        if status_id:
            queryset = queryset.filter(status__id=status_id)

        stats = queryset.values('category__name').annotate(total_sum=Sum('amount')).order_by('category__name')

        serializer = self.get_serializer(stats, many=True)
        return Response(serializer.data)