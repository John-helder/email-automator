// =========================
//  CHECK DE AUTENTICAÇÃO
// =========================
function checkAuth() {
    const token = localStorage.getItem("token");

    // Se estiver na dashboard e não tiver token → volta pro login
    const isDashboard = window.location.pathname.includes("dashboard.html");
    if (isDashboard && !token) {
        window.location.href = "login.html";
    }
}

// Executa quando a página carrega
document.addEventListener("DOMContentLoaded", checkAuth);

// =========================
//  LOGIN
// =========================
const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const senha = document.getElementById("senha").value;

        const resp = await fetch("http://127.0.0.1:8000/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, senha })
        });

        const data = await resp.json();

        if (!resp.ok) {
            alert(data.detail || "Erro ao fazer login");
            return;
        }

        // grava token
        localStorage.setItem("token", data.access_token);

        window.location.href = "dashboard.html";
    });
}

// =========================
//  REGISTRO
// =========================
const registerForm = document.getElementById("registerForm");

if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const senha = document.getElementById("senha").value;

        const resp = await fetch("http://127.0.0.1:8000/api/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, senha })
        });

        const data = await resp.json();

        if (!resp.ok) {
            alert(data.detail || "Erro ao registrar");
            return;
        }

        alert("Registrado com sucesso! Agora faça login.");
        window.location.href = "login.html";
    });
}

// =========================
//  GET /me
// =========================
async function loadUserInfo() {
    const emailDiv = document.getElementById("userEmail");
    if (!emailDiv) return;

    const token = localStorage.getItem("token");

    const resp = await fetch("http://127.0.0.1:8000/api/auth/me", {
        headers: { "Authorization": `Bearer ${token}` }
    });

    const data = await resp.json();

    if (!resp.ok) {
        emailDiv.innerText = "Erro ao carregar usuário";
        return;
    }

    emailDiv.innerText = `Logado como: ${data.email}`;
}

// Executa automaticamente na dashboard
loadUserInfo();

// =========================
//  LOGOUT
// =========================
function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}
