from django.shortcuts import render, redirect
from .models import Content, ContentType, Comment
from django.contrib.auth.models import User
from django.views import generic
import uuid
from django.urls import reverse_lazy
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



class ContentListView(generic.ListView):
    model = Content

class UserListView(generic.ListView):
    model = User


from .forms import CommentForm
class ContentDetailView(generic.DetailView):
    model = Content
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm(initial={'content_id': self.object.pk})
        context['content'] = self.get_object()
        return context


    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            content = self.get_object()
            comment = form.save(commit=False)
            comment.content = content
            comment.save()
            return redirect('content-detail', pk=content.pk)  # перенаправляем на ту же страницу
        else:
            context = self.get_context_data(**kwargs)
            context['comment_form'] = form  # передаем форму в контекст для повторного отображения
            return render(request, self.template_name, context)



class UserDetailView(generic.DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['comment_form'] = CommentForm(self.request.POST)
        else:
            context['comment_form'] = CommentForm(initial={'content_id': self.object.pk})
        return context


class ContentCreate(generic.CreateView):
    model = Content
    fields = ['author','ganre','name','description','data' ]
    #template_name = 'library/comment_form.html'

    def form_valid(self, form):
        #form.instance.commentator = User.objects.filter(login=self.request.user).get()
        form.instance.id = uuid.uuid4()

        return super(ContentCreate, self).form_valid(form)
    
class ContentUpdate(generic.UpdateView):
    model = Content
    fields = ['author','ganre','name','description','data' ]

class ContentDelete(generic.DeleteView):
    model = Content
    success_url = reverse_lazy('books')


class CommentCreate(generic.CreateView):
    model = Comment
    fields = ['commentator','content_id','text']
    #template_name = 'writer/content_detail.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        #form.instance.commentator = User.objects.filter(login=self.request.user).get()
        form.instance.id = uuid.uuid4()

        return super(CommentCreate, self).form_valid(form)



