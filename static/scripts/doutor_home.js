document.addEventListener("DOMContentLoaded", function () {
  // Detecta ambiente - desenvolvimento ou produção
  const isLocalhost =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1";
  const serverUrl = isLocalhost
    ? "http://localhost:5000"
    : window.location.origin;

  // Configuração de reconexão automática
  const socket = io(serverUrl, {
    reconnection: true,
    reconnectionAttempts: Infinity,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    timeout: 20000,
  });

  // Status de conexão
  const statusIndicator = document.createElement("div");
  statusIndicator.classList.add("connection-status");
  document.querySelector(".title").after(statusIndicator);

  function updateConnectionStatus(connected) {
    statusIndicator.className = connected
      ? "connection-status connected"
      : "connection-status disconnected";
    statusIndicator.textContent = connected
      ? "Conectado ao servidor"
      : "Desconectado - Reconectando...";
  }

  socket.on("connect", function () {
    let doutorID = document.getElementById("doutor").getAttribute("doutorID");
    socket.emit("doutorConnect", doutorID);
    updateConnectionStatus(true);
    console.log("Conectado ao servidor como doutor ID:", doutorID);
  });

  socket.on("disconnect", function () {
    updateConnectionStatus(false);
    console.log("Desconectado do servidor. Tentando reconectar...");
  });

  socket.on("queue_updated", function (fila) {
    let block = document.getElementById("fila_pacientes");

    if (fila.length === 0) {
      block.innerHTML = '<li class="empty-queue">Nenhum paciente na fila</li>';
    } else {
      block.innerHTML = fila
        .map(
          (nome) => `
        <li style='word-wrap: break-word; overflow-wrap: break-word;'>${nome}</li>
      `,
        )
        .join("");
    }

    // Atualiza contador de pacientes
    const filaCount = document.getElementById("fila-count");
    if (filaCount) {
      filaCount.textContent = fila.length;
    }
  });

  // Adiciona contador de pacientes na fila
  const subtitleFila = document.querySelector(".text-fila");
  if (subtitleFila) {
    const filaCount = document.createElement("span");
    filaCount.id = "fila-count";
    filaCount.className = "fila-count";
    filaCount.textContent = "0";
    subtitleFila.appendChild(filaCount);
  }

  // Botão de próximo paciente - confirmação
  const btnProxPaciente = document.querySelector(".proxPaciente");
  if (btnProxPaciente) {
    btnProxPaciente.addEventListener("click", function (e) {
      if (document.getElementById("fila_pacientes").children.length === 0) {
        e.preventDefault();
        alert("Não há pacientes na fila.");
      } else if (!confirm("Chamar o próximo paciente?")) {
        e.preventDefault();
      }
    });
  }
});
