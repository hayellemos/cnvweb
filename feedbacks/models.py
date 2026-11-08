from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    perfil = models.CharField(max_length=50)   # Aluno, Professor, Funcionário
    serie = models.CharField(max_length=50, blank=True, null=True)
    idade = models.CharField(max_length=20)
    entendeu = models.BooleanField()
    comentario = models.TextField(blank=True, null=True)
    estrelas = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.perfil} - {self.estrelas} estrelas"
