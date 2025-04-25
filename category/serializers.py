from rest_framework import serializers
from .models import Type, Category, Subcategory


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=Type.objects.all(), source='type', write_only=True
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'type_id']


class SubcategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category', 'category_id']
