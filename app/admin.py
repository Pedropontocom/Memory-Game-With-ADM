from django.contrib import admin
from .models import Player

class PlayerAdmin(admin.ModelAdmin):
  list_display="nome_jogador","tentativas","tempo","data_hora"

admin.site.register(Player, PlayerAdmin)
