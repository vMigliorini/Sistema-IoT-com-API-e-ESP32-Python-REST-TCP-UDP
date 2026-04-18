window.onload = async function() {

    const dados_user = await fetch("/me")
    const user = await dados_user.json()
    if (!user.ok){
        window.location.href = "/"
    }

    document.getElementById("nome-user-perfil").innerHTML = user.nome
    document.getElementById("cargo-user-perfil").innerHTML = user.cargo
}