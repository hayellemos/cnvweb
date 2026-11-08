console.log("app.js carregado com sucesso.");

document.addEventListener("DOMContentLoaded", () => {

    const btnCadastrar = document.getElementById("btnCadastrar");
    const cadEmail = document.getElementById("cadEmail");
    const cadSenha = document.getElementById("cadSenha");

    if (!btnCadastrar) {
        console.error("Botão btnCadastrar não encontrado.");
        return;
    }

    btnCadastrar.addEventListener("click", async () => {

        const email = cadEmail.value.trim();
        const senha = cadSenha.value;

        if (!email || !senha) {
            alert("Preencha o e-mail e a senha.");
            return;
        }

        if (senha.length < 6) {
            alert("A senha deve ter pelo menos 6 caracteres.");
            return;
        }

        btnCadastrar.disabled = true;
        btnCadastrar.textContent = "Cadastrando...";

        try {

            const response = await fetch("/usuarios/cadastro/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    senha: senha
                })
            });

            const data = await response.json();

            console.log("Resposta do Django:", data);

            if (response.ok && data.success) {

                alert("Cadastro realizado com sucesso!");

                cadEmail.value = "";
                cadSenha.value = "";

                // Atualiza a sessão imediatamente
                if (data.user && data.user.email) {
                    const sessionCard = document.getElementById("sessionCard");
                    const authForms = document.getElementById("authForms");
                    const loggedEmail = document.getElementById("loggedEmail");

                    if (sessionCard && authForms && loggedEmail) {
                        loggedEmail.textContent = data.user.email;
                        sessionCard.style.display = "block";
                        authForms.style.display = "none";
                    }
                }

            } else {

                alert(data.message || "Não foi possível realizar o cadastro.");

            }

        } catch (error) {

            console.error("Erro ao conectar com o Django:", error);

            alert(
                "Não foi possível conectar ao servidor. " +
                "Verifique se o Django está rodando."
            );

        } finally {

            btnCadastrar.disabled = false;
            btnCadastrar.textContent = "Cadastrar";

        }

    });

});