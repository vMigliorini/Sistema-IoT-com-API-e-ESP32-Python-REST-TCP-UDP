window.onload = async function() {

    const dados_user = await fetch("/me")
    const user = await dados_user.json()
    if (!user.ok){
        window.location.href = "/"
    }

    document.getElementById("nome-user-perfil").innerHTML = user.nome
    document.getElementById("cargo-user-perfil").innerHTML = user.cargo
}

async function adicionar_chat(event){
    event.preventDefault();
}

async function enviar_mensagem(event) {
    event.preventDefault();
    var form = document.getElementById("form-mensagem-digitada")
    var form_mensagem = new FormData(form)

    const mensagem = form_mensagem.get('conteudo-mensagem')

    var chat = `
                    <div class="mensagem">
                        <div class="icone-user">
                            <i class="fa-solid fa-circle-user"></i>
                        </div>
                        <div class="conteudo-mensagem">
                            <div class="nome-autor">
                                User
                            </div>
                            <div class="texto-autor">
                                oi
                            </div>
                        </div>
                    </div>
    `

    const response = await fetch("/chat_rooms", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body:JSON.stringify({
            // PRECISA CRIAR A CHAT ROOM ANTES DE ENVIAR A MENSAGEM DO CHAT
        })
    })
}