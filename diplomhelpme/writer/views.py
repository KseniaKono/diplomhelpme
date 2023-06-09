import time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Content, ContentType, Comment, Like, Profile, PageView, SimilarityVote
from django.contrib.auth.models import User
from django.views import generic
import uuid
from django.urls import reverse_lazy
from .forms import CommentForm, SignUpForm, ProfileForm, SimilarContentForm, SimilarityVoteForm
from django.contrib.auth import authenticate, login
import requests


from django.contrib.auth.forms import UserCreationForm
from django import forms
# Create your views here.


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_Content=Content.objects.all().count()
    num_Users=User.objects.all().count()


    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_Content':num_Content,'num_Users':num_Users},
    )



@login_required
def contentdetail(request, pk):
    content = get_object_or_404(Content, pk=pk)
    comment_form = CommentForm()
    similar_form = SimilarContentForm()
    vote_form = SimilarityVoteForm()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.content_id = content
            comment.commentator = request.user
            comment.save()
            return redirect('contentdetail', pk=pk)

        similar_form = SimilarContentForm(request.POST)
        if similar_form.is_valid():
            similar_content = similar_form.cleaned_data['similar_content']
            content.similar_content.add(similar_content)
            content.save()
            return redirect('contentdetail', pk=pk)

        vote_form = SimilarityVoteForm(request.POST)
        if vote_form.is_valid():
            vote = vote_form.save(commit=False)
            vote.user = request.user
            vote.content = content
            vote.save()
            return redirect('contentdetail', pk=pk)

    liked = Like.objects.filter(user=request.user, content_id=content).exists()
    likes_count = content.like_set.aggregate(Count('id'))['id__count']

    # Вызов представления my_view для получения количества просмотров текущей страницы
    page_url = request.path
    views_count = 1
    try:
        page_view = PageView.objects.get(page_url=page_url)
        page_view.views_count += 1  # увеличиваем счетчик
        page_view.save()  # сохраняем изменения
        views_count = page_view.views_count
    except PageView.DoesNotExist:
        PageView.objects.create(page_url=page_url)  # создаем новую запись

    return render(
        request,
        'contentdetail.html',
        context={'content': content, 'comment_form': comment_form, 'liked': liked, 'likes_count': likes_count,
                 'views_count': views_count, 'similar_form': similar_form, 'vote_form': vote_form}
    )





@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        comment.delete()
        return redirect('contentdetail',  pk=comment.content_id.id)

class ContentLike(LoginRequiredMixin, generic.ListView):
    def post(self, request, pk):
        content = get_object_or_404(Content, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, content_id=content)
        if not created:
            like.delete()
        return redirect('contentdetail', pk=pk)

class ContentListView(generic.ListView):
    model = Content
    paginate_by = 10



class UserListView(generic.ListView):
    model = User
    paginate_by = 10

class UserDetailView(generic.DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем пользователя
        user = self.get_object()

        # Считаем количество лайков, которые поставили пользователи определенного пола к произведениям пользователя
        male_likes = Like.objects.filter(content_id__author=user, user__profile__gender='male').count()
        female_likes = Like.objects.filter(content_id__author=user, user__profile__gender='female').count()

        # Добавляем данные в контекст
        context['male_likes'] = male_likes
        context['female_likes'] = female_likes

        content_count = user.content_set.count()

        # Добавляем данные в контекст
        context['content_count'] = content_count

        return context


class ContentCreate(LoginRequiredMixin, generic.CreateView):
    model = Content
    fields = ['ganre','name','description','data' ]
    #template_name = 'library/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  # устанавливаем автора формы на текущего пользователя
        form.instance.id = uuid.uuid4()

        return super(ContentCreate, self).form_valid(form)
    
class ContentUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Content
    fields = ['ganre','name','description','data' ]

    def dispatch(self, request, *args, **kwargs):
        # Получаем контент, который нужно удалить
        self.object = self.get_object()

        # Проверяем, является ли текущий пользователь автором контента
        if self.object.author != self.request.user:
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)

class ContentDelete(LoginRequiredMixin,generic.DeleteView):
    model = Content
    success_url = reverse_lazy('books')
    def dispatch(self, request, *args, **kwargs):
        # Получаем контент, который нужно удалить
        self.object = self.get_object()

        # Проверяем, является ли текущий пользователь автором контента
        if self.object.author != self.request.user:
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)




def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                Profile.objects.create(user=user)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log in user
            user = authenticate(username=username, password=password)
            login(request,user)
            return redirect('index')
    return render(request, "register.html", {'form':form})


def top_contents(request):
    top_contents = Content.objects.annotate(num_likes=Count('like')).order_by('-num_likes')[:10]
    return render(request, 'top_contents.html', {'top_contents': top_contents})

@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # Обработка файла
        if form.is_valid():
            form.save()
            return redirect('writer-user-detail', pk=pk)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'user': user})


def check_text(request):
    if request.method == 'POST':
        api_key = 'd69477e9e12f2b481ce8ae3e3ceb3a94'
        text = request.POST['text']

        payload = {
            'text': text,
            'userkey': api_key,
            'format': 'plain',
            'jsonvisible': 'uniq',
            'visible': 'vis_on',
        }

        response = requests.post('http://api.text.ru/post', data=payload)

        if response.status_code == 200:
            result = response.json()
            text_uid = result['text_uid']
            return redirect(f'https://text.ru/antiplagiat/{text_uid}')
        else:
            return render(request, 'error.html')

    return render(request, 'check_text.html')


