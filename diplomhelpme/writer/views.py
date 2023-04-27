from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Content, ContentType, Comment
from django.contrib.auth.models import User
from django.views import generic
import uuid
from django.urls import reverse_lazy
from .forms import CommentForm, SignUpForm
from django.contrib.auth import authenticate, login
from django.contrib import messages



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
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        tmp = form.save(commit=False)
        if form.is_valid():
            tmp.content_id = content
            tmp.commentator = request.user
            tmp.save()
            return redirect('contentdetail', pk=pk)  # перенаправляем на ту же страницу
    return render(
        request,
        'contentdetail.html',
        context={'content':content, 'comment_form': form}
    )

class ContentListView(generic.ListView):
    model = Content

class UserListView(generic.ListView):
    model = User






class UserDetailView(generic.DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['comment_form'] = CommentForm(self.request.POST)
        else:
            context['comment_form'] = CommentForm(initial={'content_id': self.object.pk})
        return context


class ContentCreate(LoginRequiredMixin, generic.CreateView):
    model = Content
    fields = ['author','ganre','name','description','data' ]
    #template_name = 'library/comment_form.html'

    def form_valid(self, form):
        #form.instance.commentator = User.objects.filter(login=self.request.user).get()
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

class CommentCreate(generic.CreateView):
    model = Comment
    fields = ['commentator','content_id','text']
    #template_name = 'writer/content_detail.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        #form.instance.commentator = User.objects.filter(login=self.request.user).get()
        form.instance.id = uuid.uuid4()

        return super(CommentCreate, self).form_valid(form)


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #email = form.cleaned_data['email']
            #log in user
            user = authenticate(username=username, password=password)
            login(request,user)
            #essages.success(request, ("eeeeeee"))
            return redirect('index')
    return render(request, "register.html", {'form':form})
