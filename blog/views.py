from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Author, Category
from .serializers import PostWriteSerializer, AuthorSerializer, CategorySerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator
from django.db.models import Q


@api_view(["GET", "POST"])
def post_list(request):

    if request.method == "GET":
        # ── Get query parameters ──────────────────────────────
        search        = request.GET.get("search",   "").strip()
        category_slug = request.GET.get("category", "").strip()
        page_number   = request.GET.get("page",     1)

        # ── Start with all published posts ────────────────────
        posts = Post.objects.filter(
            is_published=True
        ).order_by("-created_at")

        # ── Apply search filter ───────────────────────────────
        # Q objects let you do OR queries
        # This searches in both title AND content
        if search:
            posts = posts.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )

        # ── Apply category filter ─────────────────────────────
        if category_slug:
            posts = posts.filter(category__slug=category_slug)

        # ── Paginate ──────────────────────────────────────────
        paginator = Paginator(posts, 5)     # 5 posts per page
        page_obj  = paginator.get_page(page_number)

        # ── Serialize ─────────────────────────────────────────
        serializer = PostWriteSerializer(page_obj.object_list, many=True)

        # ── Return data + pagination info ─────────────────────
        return Response({
            "posts":      serializer.data,
            "pagination": {
                "current_page":  page_obj.number,
                "total_pages":   paginator.num_pages,
                "total_posts":   paginator.count,
                "has_next":      page_obj.has_next(),
                "has_previous":  page_obj.has_previous(),
            }
        })

    elif request.method == "POST":
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response(
                {"error": "Admin access required"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = PostWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

   
@api_view(["GET", "PATCH", "DELETE"])
def post_detail(request, post_id):

    # Get the post or return 404
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(
            {"error": "Post not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # ── GET — return post data ────────────────────────────────
    if request.method == "GET":
        serializer = PostWriteSerializer(post)
        return Response(serializer.data)

    # ── PATCH — update post (admin only) ──────────────────────
    elif request.method == "PATCH":
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response(
                {"error": "Admin access required"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = PostWriteSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ── DELETE — delete post (admin only) ─────────────────────
    elif request.method == "DELETE":
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response(
                {"error": "Admin access required"},
                status=status.HTTP_403_FORBIDDEN
            )
        post.delete()
        return Response(
            {"message": "Post deleted successfully"},
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
    serializer = PostWriteSerializer(posts, many=True)
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
    
    
