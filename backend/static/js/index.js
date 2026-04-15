async function cadastrar(){
    var form = document.getElementById("form-cadastro")
    var form_dados = new FormData(form)

    const dados = Object.fromEntries(form_dados);
    
    const nome = form_dados.get('nome')
    const email = form_dados.get('email')
    const senha = form_dados.get('senha')
    const confirmacao_senha = form_dados.get('confirmacao-senha')

    
    const erros = ["Erro! senhas não condizem", "Erro! Email fora de padrão", "Erro! Nome incompleto"]

    let mensagem = ""

    if (senha != confirmacao_senha){
        mensagem = erros[0]
    } 
    else if (!email.includes("@") || !email.includes(".com")){
        mensagem = erros[1]
    } 
    else if (nome == ""){
        mensagem = erros[2]
    }

    document.getElementById("retorno-dados-incorretos").innerHTML = `
        <div class="retorno-dados-incorretos">
            ${mensagem}
        </div>
    `
    const response = await fetch("http://localhost:5000/cadastro", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      noem: nome,
      email: email,
      senha: senha
    })
  });

  const data = await response.json();
  console.log(data);
}