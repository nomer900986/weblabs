from .models import Article
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
	try:
		post = Article.objects.get(id=article_id)
		return render(request, 'article.html', {"post": post})
	except Article.DoesNotExist:
		raise Http404
		
def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            if form["text"] and form["title"]:
                if not Article.objects.filter(title=form['title']).exists():
                    Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('get_article', article_id=Article.objects.count())
                else:
                    form['errors'] = u"Статья с таким названием уже существует"
                    return render(request, 'create_post.html', {'form': form})
            else:

                form['errors'] = u"Не все поля запонены"
                return render(request, 'create_post.html', {'form': form})
        else:

            return render(request, 'create_post.html', {})
    else:
        raise Http404

def regFunc(request):
    if request.method == "POST":
        form = {
            'username': request.POST["username"],
            'email': request.POST["email"],
            'password': request.POST['password']
        }
        if form["username"] and form['email'] and form['password']:
            try:
                User.objects.get(username=request.POST["username"])
                form['errors'] = u"Пользователь с таким именем уже существует"
                return render(request, 'reg_form.html', {'form': form})
            except User.DoesNotExist:
                User.objects.create_user(
                    username=request.POST["username"], email=request.POST["email"], password=request.POST['password'])
                return redirect('login_form')
        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'reg_form.html', {'form': form})
    else:
        return render(request, 'reg_form.html', {})

def loginFunc(request):
    if request.method == "POST":
        form = {
                'username': request.POST["username"], 
                'password': request.POST['password']
                }
        if form["username"] and form["password"]:
            user = authenticate(request, username = request.POST["username"], password = request.POST["password"])
            if user is not None:
                login(request, user)
                return redirect("archive")
            else:
                form['errors'] = u"Введеный пользователь не существует"
                return render(request, 'login_form.html', {'form': form})
        else: 
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'login_form.html', {'form': form})
    else:
        return render(request, 'login_form.html', {})

def logoutFunc(request):
    logout(request)
    return redirect('archive')
