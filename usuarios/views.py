import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token


@csrf_exempt
def cadastro_view(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Método não permitido."
        }, status=405)

    try:
        # Aceita JSON
        if request.content_type and "application/json" in request.content_type:
            data = json.loads(request.body)
            nome = data.get("nome", "").strip()
            email = data.get("email", "").strip().lower()
            senha = data.get("senha", "")
        else:
            # Aceita formulário tradicional
            nome = request.POST.get("nome", "").strip()
            email = request.POST.get("email", "").strip().lower()
            senha = request.POST.get("senha", "")

        if not email or not senha:
            return JsonResponse({
                "success": False,
                "message": "E-mail e senha são obrigatórios."
            }, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                "success": False,
                "message": "Este e-mail já está cadastrado."
            }, status=400)

        user = User.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=nome
        )

        return JsonResponse({
            "success": True,
            "message": "Cadastro realizado com sucesso!",
            "user": {
                "id": user.id,
                "nome": user.first_name,
                "email": user.email
            }
        }, status=201)

    except Exception as e:
        print("ERRO NO CADASTRO:", repr(e))

        return JsonResponse({
            "success": False,
            "message": f"Erro ao cadastrar usuário: {str(e)}"
        }, status=500)


def login_view(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Método não permitido."
        }, status=405)

    try:
        data = json.loads(request.body)

        email = data.get("email", "").strip().lower()
        senha = data.get("senha", "")

        user = authenticate(
            request,
            username=email,
            password=senha
        )

        if user is None:
            return JsonResponse({
                "success": False,
                "message": "E-mail ou senha incorretos."
            }, status=401)

        login(request, user)

        return JsonResponse({
            "success": True,
            "message": "Login realizado com sucesso!",
            "user": {
                "id": user.id,
                "nome": user.first_name,
                "email": user.email
            }
        })

    except Exception as e:
        print("ERRO NO LOGIN:", repr(e))

        return JsonResponse({
            "success": False,
            "message": "Erro ao realizar login."
        }, status=500)


def logout_view(request):
    logout(request)

    return JsonResponse({
        "success": True,
        "message": "Logout realizado com sucesso."
    })


def me_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "authenticated": False
        })

    return JsonResponse({
        "authenticated": True,
        "user": {
            "id": request.user.id,
            "nome": request.user.first_name,
            "email": request.user.email
        }
    })

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            senha = data.get("senha")

            if not email or not senha:
                return JsonResponse({"error": "Email e senha são obrigatórios"}, status=400)

            user = authenticate(username=email, password=senha)
            if user:
                login(request, user)
                return JsonResponse({"message": "Login realizado com sucesso!"})
            else:
                return JsonResponse({"error": "Credenciais inválidas"}, status=401)
                
        except json.JSONDecodeError:
            return JsonResponse({"error": "Dados inválidos"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Erro interno: {str(e)}"}, status=500)
    
    return JsonResponse({"error": "Método não permitido"}, status=405)

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logout realizado com sucesso!"})

@csrf_exempt
def get_csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})