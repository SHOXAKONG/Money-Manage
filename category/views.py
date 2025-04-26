from rest_framework import viewsets
from .models import Category, Subcategory, Type
from .serializers import SubcategorySerializer, CategorySerializer, TypeSerializer
from rest_framework.permissions import IsAuthenticated


class UserOwnedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TypeViewSet(UserOwnedModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class CategoryViewSet(UserOwnedModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class SubcategoryViewSet(UserOwnedModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

