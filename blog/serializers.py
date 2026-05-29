from rest_framework import serializers
from .models import Post, Author, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name","slug"]
        
        
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields=["id","name","email","bio"]

class PostSerializer(serializers.ModelSerializer):
    author=serializers.StringRelatedField()
    category=serializers.StringRelatedField()
    
    class Meta:
        model= Post
        fields=[
            "id",
            "title",
            "slug",
            "content",
            "author",
            "category",
            "is_published",
            "created_at",
            "updated_at"
        ]       
        read_only_fields=["id","created_at","updated_at"]