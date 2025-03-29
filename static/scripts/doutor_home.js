document.addEventListener("DOMContentLoaded", function () {
  const socket = io("http://localhost:5000");

  socket.on("connect", function () {
    console.log("Conectado ao servidor WebSocket.");
  });

  socket.on('queue_updated', function (fila) {
    let block = document.getElementById('fila_pacientes')

    block.innerHTML = fila.map(nome => `
      <li>${nome}</li>
    `).join('');
  })
});
