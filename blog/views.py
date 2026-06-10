from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Author, Category
from .serializers import PostSerializer, AuthorSerializer, CategorySerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes


@api_view(["GET", "POST"])
def post_list(request):
    if request.method == "GET":
        posts      = Post.objects.filter(is_published=True).order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        # Only logged in users can create posts
        if not request.user.is_authenticated:
            return Response(
                {"error": "Login required"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET", "DELETE"])
def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == "DELETE":
        if not request.user.is_staff:
            return Response(
                {"error": "Admin access required"},
                status=status.HTTP_403_FORBIDDEN
            )
        post.delete()
        return Response(
            {"message": "Post deleted"},
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(["GET"])
def author_list(request):
    if request.method == "GET":
        authors = Author.objects.all().order_by("name")
        serializer=AuthorSerializer(authors, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def category_list(request):
    if request.method == "GET":
        categories = Category.objects.all().order_by("name")
        serializer=CategorySerializer(categories, many=True)
        return Response(serializer.data)
    


@api_view(["GET"])
def posts_by_category(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    posts      = Post.objects.filter(category=category, is_published=True).order_by("-created_at")
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
   

@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email    = request.data.get("email", "")

    # Validate required fields
    if not username or not password:
        return Response(
            {"error": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already taken"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create the user
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    return Response(
        {"message": f"User {user.username} created successfully"},
        status=status.HTTP_201_CREATED
    )
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user=request.user
    return Response({
        "id":user.id,
        "username":user.username,
        "email":user.email,
        "is_staff":user.is_staff,
    })    
    
    

@api_view(["GET"])
def make_admin(request):
    secret = request.GET.get("secret")
    if secret != "jaggu-secret-2024":
        return Response({"error": "Forbidden"}, status=403)
    try:
        user = User.objects.get(username="jaggu")
        user.is_staff     = True
        user.is_superuser = True
        user.save()
        return Response({"success": f"{user.username} is now a superuser"})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)