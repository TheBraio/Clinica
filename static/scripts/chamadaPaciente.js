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
  const connectionStatus = document.createElement("div");
  connectionStatus.style.position = "fixed";
  connectionStatus.style.bottom = "10px";
  connectionStatus.style.right = "10px";
  connectionStatus.style.padding = "5px 10px";
  connectionStatus.style.borderRadius = "5px";
  connectionStatus.style.fontSize = "12px";
  document.body.appendChild(connectionStatus);

  function updateConnectionStatus(connected) {
    connectionStatus.style.backgroundColor = connected ? "green" : "red";
    connectionStatus.style.color = "white";
    connectionStatus.textContent = connected
      ? "Conectado"
      : "Desconectado - Reconectando...";
  }

  // Monitora eventos de conexão
  socket.on("connect", function () {
    console.log("Conectado ao servidor.");
    updateConnectionStatus(true);
  });

  socket.on("disconnect", function () {
    console.log("Desconectado do servidor. Tentando reconectar...");
    updateConnectionStatus(false);
  });

  socket.on("reconnect", function () {
    console.log("Reconectado ao servidor!");
    updateConnectionStatus(true);
  });

  // Processamento de próximo paciente
  socket.on("next_patient", function (data) {
    // Adiciona efeito sonoro e visual
    const audio = new Audio(`${serverUrl}/static/sounds/notification.mp3`);
    audio.play().catch((e) => console.log("Erro ao reproduzir áudio:", e));

    // Animação visual
    const namePatient = document.getElementById("namePatient");
    namePatient.style.animation = "none";
    namePatient.offsetHeight; // Trigger reflow
    namePatient.style.animation = "highlight 2s";

    // Atualização dos dados
    document.getElementById("lastCalls").innerHTML = data.chamadas
      .map(
        (chamada) => `
      <tr>
        <td> ${chamada.consultorio} </td>
        <td class='line-break'> ${chamada.nome} </td>
      </tr>
    `,
      )
      .join("");

    namePatient.innerText = data.paciente;
    document.getElementById("nameProfissional").innerText = data.doutor;
    document.getElementById("consultorio").innerText = data.consultorio;
  });
});
