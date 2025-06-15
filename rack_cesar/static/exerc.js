document.addEventListener("DOMContentLoaded", function() {
    document.querySelector(".submit-button").addEventListener("click", function() {
        const questaoId = document.getElementById("questao_id").value;
        const respostaSelecionada = document.querySelector('input[name="answer"]:checked');

        if (!respostaSelecionada) {
            alert("❌ Selecione uma alternativa antes de enviar!");
            return;
        }

        // Enviar os dados para Flask
        fetch("/verificar_resposta", {
            method: "POST",
            body: new URLSearchParams({
                questao_id: questaoId,
                answer: respostaSelecionada.value
            }),
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then(response => response.json())
        .then(data => {
            const resultadoDiv = document.getElementById("resultado");

            if (resultadoDiv) {
                resultadoDiv.textContent = data.mensagem;
                resultadoDiv.style.color = data.correto ? "green" : "red";
            }

            // Aguarda 1,5 segundos e então carrega uma nova questão
            setTimeout(carregarNovaQuestao, 1500);
        })
        .catch(error => console.error("Erro na requisição:", error));
    });
});

// Função para buscar uma nova questão automaticamente
function carregarNovaQuestao() {
    fetch("/nova_questao")
    .then(response => response.json())
    .then(data => {
        document.querySelector(".question-text").textContent = data.texto;
        
        // Atualiza as alternativas corretamente
        document.querySelectorAll("label").forEach((label, index) => {
            label.innerHTML = `<input type="radio" name="answer" value="${String.fromCharCode(65 + index)}"> ${String.fromCharCode(65 + index)}) ${data[`alternativa_${String.fromCharCode(97 + index)}`]}`;
        });

        document.getElementById("questao_id").value = data.id;

        // Limpa a seleção do usuário e resultado
        document.querySelectorAll("input[name='answer']").forEach(input => input.checked = false);
        document.getElementById("resultado").textContent = "";
    })
    .catch(error => console.error("Erro ao carregar nova questão:", error));
}
