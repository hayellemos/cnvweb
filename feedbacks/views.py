import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Feedback

@csrf_exempt
def novo_feedback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            perfil = data.get("perfil")
            serie = data.get("serie", "")
            idade = data.get("idade")
            entendeu = data.get("entendeu") == "Sim"
            comentario = data.get("comentario", "")
            estrelas = int(data.get("estrelas", 0))

            if not perfil or not idade or estrelas == 0:
                return JsonResponse({"error": "Campos obrigatórios faltando"}, status=400)

            Feedback.objects.create(
                perfil=perfil,
                serie=serie,
                idade=idade,
                entendeu=entendeu,
                comentario=comentario,
                estrelas=estrelas
            )

            return JsonResponse({"message": "Feedback registrado com sucesso!"})
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Dados inválidos"}, status=400)
        except ValueError:
            return JsonResponse({"error": "Dados inválidos"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Erro interno do servidor: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método não permitido"}, status=405)