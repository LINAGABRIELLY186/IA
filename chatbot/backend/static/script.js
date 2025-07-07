async function enviarPergunta() {
  const pergunta = document.getElementById("pergunta").value;
  const respostaDiv = document.getElementById("resposta");
  respostaDiv.innerText = "Carregando...";

  const response = await fetch("https://assistente-lia.onrender.com/api/pergunta", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pergunta })
  });


  const data = await response.json();
  respostaDiv.innerText = data.resposta;
}

async function enviarImagem() {
  const file = document.getElementById("imagemInput").files[0];
  const prompt = document.getElementById("promptImagem").value;
  const reader = new FileReader();

  reader.onloadend = async function () {
    const base64 = reader.result.split(',')[1];

    const response = await fetch("https://assistente-lia.onrender.com/api/imagem", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ imagem: base64, prompt })
  });


    const data = await response.json();
    document.getElementById("resposta").innerText = data.resposta;
  };

  if (file) reader.readAsDataURL(file);
}
