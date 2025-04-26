from rest_framework import serializers
from cashflow.models import Status, CashFlow
from category.models import Subcategory, Category, Type
from category.serializers import SubcategorySerializer, CategorySerializer, TypeSerializer


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']


class CashFlowRecordSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(), source='status', write_only=True
    )
    subcategory = SubcategorySerializer(read_only=True)
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=Subcategory.objects.all(), source='subcategory', write_only=True
    )
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    type = TypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=Type.objects.all(), source='type', write_only=True
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.DateTimeField(required=False)
    class Meta:
        model = CashFlow
        fields = ['id', 'user', 'date', 'status', 'status_id', 'subcategory', 'subcategory_id',
                  'category', 'category_id', 'type', 'type_id', 'amount', 'comment']

    def validate(self, data):
        if data['category'].type != data['type']:
            raise serializers.ValidationError("Category does not belong to the selected type.")
        if data['subcategory'].category != data['category']:
            raise serializers.ValidationError("Subcategory does not belong to the selected category.")
        return data
