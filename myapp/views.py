from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Comment,Post
# Create your views here.
def index(request):
    return render(request,"index.html",{
        'posts':Post.objects.filter(user_id=request.user.id).order_by("id").reverse(),
        'top_posts':Post.objects.all().order_by("-likes"),
        'recent_posts':Post.objects.all().order_by("-id"),
        'user':request.user,
        'media_url':settings.MEDIA_URL
    })


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already Exists")
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already Exists")
                return redirect('signup')
            else:
                User.objects.create_user(username=username,email=email,password=password).save()
                return redirect('signin')
        else:
            messages.info(request,"Password should match")
            return redirect('signup')
            
    return render(request,"signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("index")
        else:
            messages.info(request,'Username or Password is incorrect')
            return redirect("signin")
            
    return render(request,"signin.html")

def logout(request):
    auth.logout(request)
    return redirect('index')

def blog(request):
    # Lấy tất cả bài viết sắp xếp theo thứ tự mới nhất
    all_posts = Post.objects.all().order_by("-id")
    
    # Phân trang
    paginator = Paginator(all_posts, 3)  # Mỗi trang sẽ hiển thị 3 bài viết
    page_number = request.GET.get('page', 1)  # Mặc định trang đầu tiên nếu không có tham số page
    
    try:
        current_page = paginator.page(page_number)
    except PageNotAnInteger:
        # Nếu page_number không phải số nguyên, hiển thị trang đầu tiên
        current_page = paginator.page(1)
    except EmptyPage:
        # Nếu page_number quá lớn, hiển thị trang cuối cùng
        current_page = paginator.page(paginator.num_pages)
    
    return render(request, "blog.html", {
        'posts': Post.objects.filter(user_id=request.user.id).order_by("id").reverse(),
        'top_posts': Post.objects.all().order_by("-likes"),
        'recent_posts': current_page,  # Danh sách bài viết đã phân trang
        'user': request.user,
        'media_url': settings.MEDIA_URL,
        'paginator': paginator,
        'current_page': current_page,
    })
    
def create(request):
    if request.method == 'POST':
        try:
            postname = request.POST['postname']
            content = request.POST['content']
            category = request.POST['category']
            image = request.FILES.get('image')
            audio = request.FILES.get('audio')
            Post(postname=postname,content=content,category=category,image=image,audio=audio,user=request.user).save()
        except Exception as e:
            print(f"Error: {e}")
        return redirect('index')
    else:
        return render(request,"create.html")

def search(request):
    query = request.GET.get('query', '')
    
    if query:
        # Tìm kiếm bài viết theo tiêu đề (postname) chứa từ khóa tìm kiếm
        search_results = Post.objects.filter(postname__icontains=query).order_by('-id')
    else:
        search_results = Post.objects.none()
        
    return render(request, "search_results.html", {
        'query': query,
        'results': search_results,
        'media_url': settings.MEDIA_URL,
        'user': request.user,
        'count': len(search_results),
    })

def category_filter(request, category):
    # Lấy danh sách bài viết theo category
    filtered_posts = Post.objects.filter(category__iexact=category).order_by('-id')
    
    return render(request, "category_results.html", {
        'category': category,
        'results': filtered_posts,
        'media_url': settings.MEDIA_URL,
        'user': request.user,
        'count': len(filtered_posts),
    })
           
def profile(request,id):
    
    return render(request,'profile.html',{
        'user':User.objects.get(id=id),
        'posts':Post.objects.all(),
        'media_url':settings.MEDIA_URL,
    })
    
    
def profileedit(request,id):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
    
        user = User.objects.get(id=id)
        user.first_name = firstname
        user.email = email
        user.last_name = lastname
        user.save()
        return profile(request,id)
    return render(request,"profileedit.html",{
        'user':User.objects.get(id=id),
    })
    
def increaselikes(request,id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        post.likes += 1
        post.save() 
    return redirect("index")


def post(request,id):
    post = Post.objects.get(id=id)
    
    return render(request,"post-details.html",{
        "user":request.user,
        'post':Post.objects.get(id=id),
        'recent_posts':Post.objects.all().order_by("-id"),
        'media_url':settings.MEDIA_URL,
        'comments':Comment.objects.filter(post_id = post.id),
        'total_comments': len(Comment.objects.filter(post_id = post.id))
    })
    
def savecomment(request,id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        content = request.POST['message']
        Comment(post_id = post.id,user_id = request.user.id, content = content).save()
        return redirect("index")
    
def deletecomment(request,id):
    comment = Comment.objects.get(id=id)
    postid = comment.post.id
    comment.delete()
    return post(request,postid)
    
def editpost(request,id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        try:
            postname = request.POST['postname']
            content = request.POST['content']
            category = request.POST['category']
            
            post.postname = postname
            post.content = content
            post.category = category
            
            # Xử lý ảnh mới nếu được tải lên
            if 'image' in request.FILES:
                post.image = request.FILES['image']
                
            # Xử lý file âm thanh mới nếu được tải lên
            if 'audio' in request.FILES:
                post.audio = request.FILES['audio']
                
            post.save()
        except Exception as e:
            print(f"Error: {e}")
        return profile(request,request.user.id)
    
    return render(request,"postedit.html",{
        'post':post
    })
    
def deletepost(request,id):
    Post.objects.get(id=id).delete()
    return profile(request,request.user.id)


def contact_us(request):
    context={}
    if request.method == 'POST':
        name=request.POST.get('name')    
        email=request.POST.get('email')  
        subject=request.POST.get('subject')  
        message=request.POST.get('message')  

        obj = Contact(name=name,email=email,subject=subject,message=message)
        obj.save()
        context['message']=f"Dear {name}, Thanks for your time!"

    return render(request,"contact.html")
