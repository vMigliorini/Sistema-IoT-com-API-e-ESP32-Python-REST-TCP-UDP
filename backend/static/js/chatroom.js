var socket = null;

window.onload = async function() {
    const dialog = document.getElementById('pop_up_adiocionar_chat');
    dialog.close()
    const dados_user = await fetch("/me")
    const user = await dados_user.json()
    if (!user.ok){
        window.location.href = "/"
    }

    document.getElementById("nome-user-perfil").innerHTML = user.nome
    document.getElementById("cargo-user-perfil").innerHTML = user.cargo

    await inserir_chatroom()
}



async function abrir_popup_add_chat() {
    const dialog = document.getElementById('pop_up_adiocionar_chat');
    dialog.showModal()
}

async function fechar_popup_add_chat() {
    const dialog = document.getElementById('pop_up_adiocionar_chat');
    dialog.close()
}

async function criar_chatroom() {
    const nome_sala = document.getElementById("nome-sala").value
    const response = await fetch("/chat_rooms", {
        method:"POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nome_sala: nome_sala
        })

    })
    const sala = await response.json()
    if (!sala.ok){
        document.getElementById("campo-retorno-erros").innerHTML = sala.erro
    }
    else{
        fechar_popup_add_chat()
        inserir_chatroom()
    }
}

async function inserir_chatroom() {
    const response = await fetch("/chat_rooms/listar")
    const users_conectados = await response.json()
    document.getElementById("container-multi-chats").innerHTML = ""
    for (var i = 0; i < users_conectados.length; i ++){

        var template = `
                    <div class="container-chat-individual"> <!--   Aqui usaremos Js para adicionar os chats à sessão     -->

                        <div class="chat-room">
                            <div class="informacoes-chatroom">
                                <div class="titulo-chatroom">
                                    sala: ${users_conectados[i].nome}
                                </div>
                                <div class="participantes-chatroom">
                                    online: ${users_conectados[i].usuarios}
                                </div>
                            </div>
                            <div class="icone-entrar-chatroom">
                                <button onclick=entrar_chatroom()><i class="fa-solid fa-circle-arrow-right"></i></button>
                            </div>
                        </div>
                        
                    </div>
        `
        document.getElementById("container-multi-chats").innerHTML += template
    }
}

async function entrar_chatroom(){

    if (socket) socket.disconnect();
    socket = io();

    socket.on("message", function(data) {
        var mensagens = document.getElementById("mensagem")
        template = `
                    <div class="mensagem">
                        <div class="icone-user">
                            <i class="fa-solid fa-circle-user"></i>
                        </div>
                        <div class="conteudo-mensagem">
                            <div class="nome-autor">
                                ${data.username}
                            </div>
                            <div class="texto-autor">
                                ${data.data}
                            </div>
                        </div>
                    </div>
        `
        mensagens.innerHTML += template
    })
}

function sendMessage(event){
    event.preventDefault();
    var input_mensagem = document.getElementById("mensagem-digitada")
    var mensagem = input_mensagem.value
    if (mensagem.trim() === "") return;
    socket.send(mensagem)
    input_mensagem.value = ""
    mensagem = ""
}
