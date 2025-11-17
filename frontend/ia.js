console.log("IA.js carregado");

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("analyzeForm");
    const textoInput = document.getElementById("textoEmail");
    const fileInput = document.getElementById("fileEmail");
    const respostaIa = document.getElementById("respostaIa");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const token = localStorage.getItem("token");
        if (!token) {
            alert("Usuário não autenticado!");
            window.location.href = "login.html";
            return;
        }

        let texto = textoInput.value;

        // Processa arquivo se enviado
        if (fileInput.files.length > 0) {
            const arquivo = fileInput.files[0];

            if (arquivo.type !== "text/plain") {
                alert("Somente arquivos .txt são aceitos.");
                return;
            }

            texto = await arquivo.text();
        }

        if (!texto.trim()) {
            alert("Insira um texto ou selecione um arquivo!");
            return;
        }

        try {
            const resp = await fetch("http://127.0.0.1:8000/api/ia/analisar-nlp", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ texto })
            });

            const data = await resp.json();
            respostaIa.innerText = JSON.stringify(data, null, 2);

        } catch (error) {
            console.error(error);
            respostaIa.innerText = "Erro ao comunicar com a API.";
        }
    });
});
