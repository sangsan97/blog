from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Publication, Comment, MyUser, Member
from .forms import PostForm, CommentForm, UserForm, LoginForm, PublicationForm, MemberForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from django.http import HttpResponseRedirect

# Create your views here.

class HomePageView(ListView):
    model = Publication
    template_name = 'blog/slide2.html'

    def get_context_data(self):
        context = super(HomePageView, self).get_context_data()
        context['recent_publications'] = Publication.objects.order_by('-year_of_publication')[0:3]
        context['recent_posts'] = Post.objects.order_by('-published_date').filter(where_to_status='post_list')[0:2]
        context['recent_posts2'] = Post.objects.order_by('-published_date').filter(where_to_status='post_list2')[0:2]
        return context
        

class AboutView(TemplateView):
    template_name = 'blog/about.html'

# Professor, Members View

class ProfessorView(TemplateView):
    template_name = 'blog/professor.html'

@login_required(redirect_field_name='blog/member_form.html', login_url='/login/')
def member_upload(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm()
    return render(request, 'blog/member_form.html', { 'form': form })

class MembersView(ListView):
    model = Member
    context_object_name = 'members'

    def get_queryset(self):
        return Member.objects.order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super(MembersView, self).get_context_data()
        context['where_to_status'] =  [['postdoc','Post Doctorate'],
        ['phd','PhD.'],
        ['master','Master Degree'],
        ['visiting','Visiting Student']]

        return context

# registration view

def Signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

def Signout(request):
    logout(request)
    return redirect('/')

def Signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = MyUser.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('/')
    else:
        form = UserForm()
        return render(request, 'blog/adduser.html', {'form': form})

# Post View

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(where_to_status='post_list').order_by('-published_date')

class PostList2View(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(where_to_status='post_list2').order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

@login_required(redirect_field_name='blog/post_form.html', login_url='/login/')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.where_to_status == 'draft':
                post.save()
                return redirect('post_draft_list')
            elif post.where_to_status == 'post_list':
                post.published_date = timezone.now()
                post.save()
                return redirect('post_list')
            else:
                post.published_date = timezone.now()
                post.save()
                return redirect('post_list2')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', { 'form': form })

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_draft_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# TO-DO part
# class PostEditView(LoginRequiredMixin, UpdateView):
    # login_url = '/login/'
    # redirect_field_name = 'blog/post_edit.html'
    # form_class = PostForm(instance=)
    # model = Post
    # form_class = PostForm()
    
    
    # fields = ('title','text', 'photo', 'document', 'where_to_status', )
    # context_object_name = 'post'
    
    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     return redirect('post_draft_list')

    # def get_queryset(self):
    #     Post.objects.filter(pk=self.kwargs['pk'])
        
class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    # redirect_field_name = 'blog/post_draft_list.html'
    model = Post
    fields = ('text', )
    template_name = 'blog/post_draft_list.html'
    # context_object is defined by the get_queryset
    # then the name of the object is used in the html file is defined as below
    context_object_name = 'posts'

    def get_queryset(self):
        # draft_posts = Post.objects.filter(published_date__isnull=True).order_by('created_date').reverse()
        draft_posts = Post.objects.filter(where_to_status='draft').order_by('created_date').reverse()
        return draft_posts

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
        
    def get_success_url(self):
        if self.object.where_to_status == 'draft':
            redirect_to = 'post_draft_list'
        elif self.object.where_to_status == 'post_list':
            redirect_to = 'post_list'
        elif self.object.where_to_status == 'post_list2':
            redirect_to = 'post_list2'
        return reverse(redirect_to)

# Publication View
class CreatePublicationView(LoginRequiredMixin, CreateView):
    # below 2 objects checks the login user and renders the form
    login_url = '/login/'
    redirect_field_name = 'blog/publication_form.html'
    model = Publication
    form_class = PublicationForm

    def post(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            print('form is valid')
            return self.form_valid(form)
        else:
            print('form is not valid')

    def form_valid(self, form):
        publication=form.save(commit=False)
        # should be changed after making the list view
        redirect_to = 'publication_list'
        publication.save()
        return HttpResponseRedirect(self.get_success_url(redirect_to))

    def get_success_url(self, redirect_to):
        return reverse(redirect_to)

class PublicationListView(ListView):
    model = Publication
    context_object_name = 'publications'

    def get_queryset(self):
        return Publication.objects.order_by('-year_of_publication')
    # get_context_data 사용 > 또 다른 variable인 years를 listview를 이용해서 전달할 수 있다.

    def get_context_data(self):
        context = super(PublicationListView, self).get_context_data()
        context['years'] = []
        years_list = []
        publications = Publication.objects.order_by('-year_of_publication')
        
        for publication in publications:
            years_list.append(publication.year_of_publication.year)
        
        years_list = list(set(years_list))
        # years_list에서 중복된 연도를 set method로 없앤 뒤, 다시 list로 변환.
        years_list.sort(reverse=True)
        # 연도의 역순으로 순서 배열
        context['years'] = years_list

        return context

class PublicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Publication
    
    def get_success_url(self):
        return reverse('publication_list')

# publish is not needed. user can publish in the edit page 
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = CommentForm()

    return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)