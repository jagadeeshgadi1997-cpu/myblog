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

class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Post
        fields = [
            "title", "slug", "content",
            "author", "category", "is_published"
        ]    
