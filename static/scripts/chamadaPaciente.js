document.addEventListener("DOMContentLoaded", function () {
  const socket = io("http://localhost:5000");

  socket.on("connect", function () {
    console.log("Conectado ao servidor WebSocket.");
  });

  socket.on("next_patient", function (data) {
    console.log("Atualizou", data);
    document.getElementById("lastCalls").innerHTML = data.chamadas.map(chamada => `
      <tr> 
        <td> ${chamada.consultorio} </td>
        <td> ${chamada.nome} </td>
      </tr>
    `).join('');
    document.getElementById("namePatient").innerText = data.paciente;
    document.getElementById('nameProfissional').innerText = data.doutor;
    document.getElementById('consultorio').innerText = data.consultorio;
  });
});
