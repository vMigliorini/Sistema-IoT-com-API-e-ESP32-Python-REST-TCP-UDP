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
}



async function abrir_popup_add_chat(){
    const dialog = document.getElementById('pop_up_adiocionar_chat');
    dialog.showModal()
}

async function fechar_popup_add_chat(params) {
    const dialog = document.getElementById('pop_up_adiocionar_chat');
    dialog.close()
}