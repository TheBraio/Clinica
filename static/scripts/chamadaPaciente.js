document.addEventListener("DOMContentLoaded", function () {
  const socket = io("http://localhost:5000");

  socket.on("connect", function () {
    console.log("Conectado ao servidor WebSocket.");
  });

  socket.on("handshake", function (data) {
    console.log("Handshake:", data);
    if (data.paciente) {
      document.getElementById("namePatient").innerText = data.nome;
    } else {
      document.getElementById("namePatient").innerText = "Não definido.";
    }
  });

  socket.on("next_patient", function (data) {
    console.log("Atualizou", data);
    document.getElementById("lastCalls").innerText = document.getElementById("namePatient").innerText;
    document.getElementById("namePatient").innerText = data.nome;
  });
});
