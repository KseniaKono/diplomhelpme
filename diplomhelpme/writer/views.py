from django.shortcuts import render
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

class ContentDetailView(generic.DetailView):
    model = Content
    
class UserDetailView(generic.DetailView):
    model = User


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