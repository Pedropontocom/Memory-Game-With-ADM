from django.shortcuts import redirect, render
from .models import Player
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout

def index(request):
  return render(request, 'index.html')

def indexTelaNome(request):
  if request.user.is_authenticated:
    return render(request, 'indexTelaNome.html')
  
  return redirect('login')

def indexTelaGame(request):
  return render(request, 'indexTelaGame.html')

def add(request):
  x=request.POST['nome_jogador']
  y=request.POST['tentativas']
  z=request.POST['tempo']
  player=Player(nome_jogador=x, tentativas=y, tempo=z, user=request.user)
  player.save()
  return redirect("/")
  
def indexTelaOpicoes(request):
  return render(request, 'indexTelaOpicoes.html')

def indexTelaRanking(request):
  player=Player.objects.all().order_by("tentativas", "tempo").values()
  return render(request, 'indexTelaRanking.html', {'player':player})

def custom_logout(request):
    logout(request)
    return redirect('login')   

class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('indexTelaNome')  # Substitua pelo nome correto da rota

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verifica se o usuário já existe
        user = User.objects.filter(username=username).first()
        if not user:
            # Cria um novo usuário
            user = User.objects.create_user(username=username, password=password)
            messages.success(request, 'Usuário criado com sucesso! Faça login para continuar.')

        # Autentica o usuário
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(self.success_url)
        else:
            messages.error(request, 'Falha no login. Verifique as informações e tente novamente.')
            return render(request, self.template_name)

# class CustomLoginView(LoginView):
#     template_name = 'login.html'
#     def login(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = User.objects.filter(username=username).first()
#         if not user:
#             user = User.objects.create_user(username=username, password=password)

#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('indexTelaNome')
#         else:
#             messages.error(request, 'Usuário ou senha incorretos. Tente novamente.')
#             return self.form_invalid(self.get_form())