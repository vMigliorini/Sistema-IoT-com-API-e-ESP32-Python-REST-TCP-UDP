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

    const saved_room_id = sessionStorage.getItem("room_id");
    if (saved_room_id) {
        await entrar_chatroom(parseInt(saved_room_id));
    }
}

async function refresh(){
    await fetch("/api/chat_rooms", {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json'
        }
    })
    window.location.reload();
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
    if (nome_sala == ""){
        document.getElementById("campo-retorno-erros").innerHTML = "Erro! sala sem nome"
        return
    }
    const response = await fetch("/api/chat_rooms", {
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
        await fechar_popup_add_chat()
        desconectar()
        await entrar_chatroom(sala.room_id)
        await inserir_chatroom()
    }
}

async function inserir_chatroom() {

    const response = await fetch("/api/chat_rooms")
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
                                <button onclick=entrar_chatroom(${users_conectados[i].id_sala})><i class="fa-solid fa-circle-arrow-right"></i></button>
                            </div>
                        </div>
                        
                    </div>
        `
        document.getElementById("container-multi-chats").innerHTML += template   
    }
}

async function entrar_chatroom(room_id){

    desconectar();

    sessionStorage.setItem("room_id", room_id);

    socket = io();

    socket.on("connect", function(){
        const saved_room_id = sessionStorage.getItem("room_id");
        if (saved_room_id) {
            socket.emit("join", parseInt(saved_room_id));
        }else{
            socket.emit("join", room_id)
        }
    })

    socket.on("disconnect", function(){
        desconectar()
    })

    socket.on("message", function(data) {
        var mensagens = document.getElementById("mensagem")
        template = `
                    <div class="mensagem">
                        <div class="icone-user">
                            <i class="fa-solid fa-circle-user"></i>
                        </div>
                        <div class="conteudo-mensagem">
                            <div class="nome-autor-mensagem">
                                ${sanitize(data.username)}
                            </div>
                            <div class="texto-autor">
                                ${sanitize(data.data)}
                            </div>
                        </div>
                    </div>
        `
        mensagens.innerHTML += template
        mensagens.scrollTop = mensagens.scrollHeight;
    })

    await usuarios_conectados(room_id)

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

async function desconectar() {
    if (socket) {
        socket.disconnect()
        socket = null
    }
    sessionStorage.removeItem("room_id")
    document.getElementById("mensagem").innerHTML = ""
}

async function usuarios_conectados(room_id) {

    document.getElementById("usuarios-conectados").innerHTML = ""
    
    const response = await fetch(`/api/chat_rooms/${room_id}`)
    const lista_nomes = await response.json()

    if (!lista_nomes.ok) {
        console.log(lista_nomes.ok)
        return
    }

    for (var i = 0; i < lista_nomes.usuarios.length; i++) {
        var template = `
                    <div class="container-users">
                        <div class="icone-user-conectados">
                            <i class="fa-solid fa-circle-user"></i>
                        </div>
                        <div class="conteudo-mensagem">
                            <div class="nome-autor">
                                ${lista_nomes.usuarios[i]}
                            </div>
                        </div>
                    </div>
        `
        document.getElementById("usuarios-conectados").innerHTML += template
    }


}

function sanitize(str) {
    const div = document.createElement("div");
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}
