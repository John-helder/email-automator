// Mock inicial (simular emails recebidos)
const emails = [
    { id: 1, assunto: "Reunião amanhã", corpo: "Olá, podemos confirmar a reunião de amanhã?" },
    { id: 2, assunto: "Fatura pendente", corpo: "Favor revisar a fatura que está em aberto." },
    { id: 3, assunto: "Convite para evento", corpo: "Você está convidado para nosso evento anual!" }
];

const emailList = document.getElementById("emailList");
const emailViewer = document.getElementById("emailViewer");
const emailSubject = document.getElementById("emailSubject");
const emailBody = document.getElementById("emailBody");
const autoReplyBtn = document.getElementById("autoReplyBtn");
const loading = document.getElementById("loading");
const generatedReply = document.getElementById("generatedReply");
const replyHistory = document.getElementById("replyHistory");

let emailSelecionado = null;

// ===== CARREGAR LISTA DE EMAILS =====
function carregarLista() {
    emailList.innerHTML = "";
    emails.forEach((email) => {
        const li = document.createElement("li");
        li.textContent = email.assunto;
        li.onclick = () => selecionarEmail(email, li);
        emailList.appendChild(li);
    });
}
carregarLista();

// ===== SELECIONAR EMAIL =====
function selecionarEmail(email, element) {
    emailSelecionado = email;

    [...emailList.children].forEach(li => li.classList.remove("selected"));
    element.classList.add("selected");

    emailSubject.textContent = email.assunto;
    emailBody.textContent = email.corpo;

    generatedReply.classList.add("hidden");

    emailViewer.classList.remove("hidden");
}

// ===== CHAMAR API PARA GERAR RESPOSTA =====
autoReplyBtn.onclick = async () => {
    if (!emailSelecionado) return;

    loading.classList.remove("hidden");
    generatedReply.classList.add("hidden");

    const resp = await fetch("http://localhost:8000/api/ia/auto-reply", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ texto: emailSelecionado.corpo })
    });

    const data = await resp.json();

    loading.classList.add("hidden");
    generatedReply.classList.remove("hidden");
    generatedReply.textContent = data.resposta;

    adicionarHistorico(data.resposta);
};

// ===== HISTÓRICO =====
function adicionarHistorico(texto) {
    const li = document.createElement("li");
    li.textContent = texto;
    replyHistory.appendChild(li);
}

// ===== TEMA ESCURO =====
document.getElementById("toggleTheme").onclick = () => {
    document.body.classList.toggle("dark");
};
