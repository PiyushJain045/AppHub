from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Post
from .forms import CommentForm

# Create your views here.

class home_page(View):
    def get(self, request):
        posts = Post.objects.all().order_by("-date")[:3]
        return render(request, "Blog/home-page.html", {"posts": posts})
    
    
class all_posts(View):
    def get(self, request):
        posts = Post.objects.all().order_by("-date")
        return render(request, "Blog/all-posts.html", {"posts": posts})
    
    
class blog_page(View):
    def readlater_on_button(self, request, post_id):
        stored_posts = request.session.get('stored_posts')
        
        if stored_posts == None or post_id not in stored_posts:
            read_later_on_button = True
        else:
            read_later_on_button = False

        return read_later_on_button
    
    def get(self, request, slug):
        identified_blog = Post.objects.get(slug=slug)
        
        return render(request, "Blog/blog-page.html", {
            "blog": identified_blog,
            "post_tags": identified_blog.tags.all(),
            "comments":identified_blog.comments.all().order_by("-id"),
            "comment_form": CommentForm(),
            "read_later_on_button": self.readlater_on_button(request, identified_blog.id)
            })
        
    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        identified_blog = Post.objects.get(slug=slug)
        
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = identified_blog
            comment.save()
            HttpResponseRedirect(reverse("page3", args=[slug]))
        
        return render(request, "Blog/blog-page.html", {
            "blog": identified_blog,
            "post_tags": identified_blog.tags.all(),
            "comments":identified_blog.comments.all().order_by("-id"),
            "comment_form": CommentForm(),
            "read_later_on_button": self.readlater_on_button(request, identified_blog.id)
            })
        
        
class ReadLaterView(View):
        def get(self, request):
            stored_posts = request.session.get('stored_posts', [])
            
            if len(stored_posts) == 0:
                posts_for_later = False
                posts = None
            else:
                posts_for_later = True 
                posts = Post.objects.filter(id__in=stored_posts)   
            
            return render(request, "Blog/stored-posts.html",{
                "posts_for_later": posts_for_later,
                "posts": posts
            })
        
        
        def post(self, request):
            stored_posts = request.session.get('stored_posts', [])
            post_id = int(request.POST['button_wali_value'])
            
            if post_id not in stored_posts:
                stored_posts.append(post_id)
            else:
                stored_posts.remove(post_id)
                
            request.session["stored_posts"] = stored_posts
            
            return HttpResponseRedirect("/Blog/")
            
            