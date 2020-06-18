from django.shortcuts import render, get_object_or_404
# use to reverse to new page
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from blog.models import Post, Comment
from blog import model_helpers
from blog import navigation
from blog.forms import CreateCommentForm


# Create your views here.


def message_posted(request, post_id, comment):
    return HttpResponse('Thanks, your form has been submitted {}'.format(comment))


#  default category will be category_name=model_helpers.post_category_all.slug() ie post_category_all
def post_list(request, category_name=model_helpers.post_category_all.slug()):
    #  model_helpers return a tuple (category, posts)
    category, posts = model_helpers.get_category_and_posts(category_name)  # allows loading all posts
    categories = model_helpers.get_categories()
    #  get_categories et get_category_name are separated from views to reusing in others spots

    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_POSTS),
        'category': category,
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog/posts_list.html', context)
    #  post_list.html is the template that display content of context
    #  must give relative path


def post_detail(request, post_id, message=''):
    post = get_object_or_404(Post, pk=post_id)
    #  get_object_or_404 allows to get a post
    # variable that contents list of post in same category
    posts_same_category = Post.objects.filter(published=True, category=post.category) \
        .exclude(pk=post_id)
    # short comment by status and order by created date
    comments = post.comments.exclude(status=Comment.STATUS_HIDDEN).order_by('created_at')

    #  treatment of form comment
    # tests if the method HTTP used is a post request so form was sent
    if request.method == 'POST':
        comment_form = CreateCommentForm(request.POST)
        #  request.POST a parameter give to constructor that gather data content in form

        # checks form validity
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            #  associate comment to a post by FK
            comment.post = post
            # save in BDD
            comment.save()

            args = [post.pk, 'Thanks, your comment has been posted']
            #  display message to user to confirm submit of form content
            #  post-detail-message is url of redirection if a post wa submitted
            return HttpResponseRedirect(reverse('post-detail-message',
                                        args=args) + '#comments')
            #  to place browser near the id that represents comment that posted
    else:
        comment_form = CreateCommentForm()

    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_POSTS),
        'post': post,
        'posts_same_category': posts_same_category,
        'comments': comments,
        'comment_form': comment_form,
        'message': message,
    }
    return render(request, 'blog/post_detail.html', context)


def about(request):
    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_ABOUT),
    }
    return render(request, 'blog/about.html', context)
