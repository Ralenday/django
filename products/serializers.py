from rest_framework import serializers
from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):
    # Se recibe el ID de la categoría al crear/actualizar (POST/PUT)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_name = serializers.StringRelatedField(source='category', read_only=True)  # Muestra el nombre

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category', 'category_name')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
