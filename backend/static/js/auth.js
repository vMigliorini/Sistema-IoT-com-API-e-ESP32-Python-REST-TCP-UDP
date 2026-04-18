async function cadastrar(event){
    event.preventDefault();
    var form = document.getElementById("form-cadastro")
    var form_dados = new FormData(form)
    
    const nome = form_dados.get('nome')
    const email = form_dados.get('email')
    const senha = form_dados.get('senha')
    const confirmacao_senha = form_dados.get('confirmacao-senha')
    const cargo = form_dados.get('cargos')


    
    const erros = ["Erro! senhas não condizem", "Erro! Email fora de padrão", "Erro! Preencha todos os campos"]

    let mensagem = ""

    if (senha != confirmacao_senha){
        mensagem = erros[0]
    } 
    else if (nome == "" || email == "" || cargo == ""){
        mensagem = erros[2]
    }
    else if (!email.includes("@") || !email.includes(".com")){
        mensagem = erros[1]
    } 
    
    if (mensagem != ""){
        document.getElementById("retorno-dados-incorretos").innerHTML = `
            <div class="retorno-dados-incorretos">
                ${mensagem}
            </div>
        `
        return
    }

    const response = await fetch("/cadastro", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nome: nome,
            email: email,
            senha: senha,
            cargo: cargo
        })
    })

    const data = await response.json()
    if (data.ok){
        window.location.href = data.redirect
    }else {
        mensagem = "Erro ao cadastrar usuário"
        document.getElementById("retorno-dados-incorretos").innerHTML = `
        <div class="retorno-dados-incorretos">
            ${mensagem}
        </div>
        `
    }

}

async function logar(event){
    event.preventDefault();
    var form = document.getElementById("form-login")
    var form_dados = new FormData(form)

    const email = form_dados.get('email')
    const senha = form_dados.get('senha')

    const erros = ["Erro! Preencha todos os campos", "Erro! Email fora de padrão"]

    let mensagem = ""


    if (email == "" || senha == ""){
        mensagem = erros[0]
    }
    else if (!email.includes("@") || !email.includes(".com")){
        mensagem = erros[1]
    }
    
    if (mensagem != ""){
        document.getElementById("retorno-dados-incorretos").innerHTML = `
            <div class="retorno-dados-incorretos">
                ${mensagem}
            </div>
        `
        return
    }

    const response = await fetch("/", {
        method: "POST",
        credentials: 'include',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            senha: senha
        })
    })

    const data = await response.json()
    if (data.ok){
        window.location.href = data.redirect;
    }else{
        document.getElementById("retorno-dados-incorretos").innerHTML = `
        <div class="container-retorno" >
            <div class="retorno-dados-incorretos" id="retorno-dados-incorretos">
                ${data.erro}
            </div>
        </div>
        `
    }

    
    
    
}