(async function load() {

    const BASE_URL = window.location.protocol + "//" + window.location.host + "/adminchat/";


    //Solicita y devuelve una lista
    async function getUrl(url) {
        const list = await axios.get(`${BASE_URL}${url}`);
        return list;
    }

    //Template lista de docentes
    function listUsuario1Template(data) {
        return `
        <option value="${data.id_user1}">${data.name}</option>
          `;
    }

    //Template lista de alumnos o tutores
    function listUsuario2Template(data, user1) {
        const sp = "/static/images/no_avatar.jpeg"

        return `
        <div class="user" data-user1="${user1}" data-user2="${data.id}">
            <div class="avatar">
                <img src="${data.avatar ? data.avatar : sp}" alt="${data.display_name}">
                </div>
            <div class="name">${data.display_name}</div>
            <div class="mood">${String(data.tipo_usuario).toLowerCase()}</div>
         </div>
        `
    }

    //Template de chat
    function MensajeTemplate(data) {
        const sp = "/static/images/no_avatar.jpeg"

        let orientacion = "right"
        let link = ""
        if (data.user.tipo_usuario == "DOCENTE") {
            orientacion = "left"
        }
        if (data.archivo) {
            link = `<a <a style="color: #141415;"
            href="${data.archivo}" download >
            ${String(data.archivo).replace("/media/clases/mensajes/archivos/", "")}
            </a>`
        }
        return `
        <div class="answer ${orientacion}">
            <div class="avatar">
                <img src="${data.user.avatar ? data.user.avatar : sp}" alt="${data.user.display_name}"/>
            </div>
                <div class="name">${data.user.display_name}</div>
            <div class="text">
                ${data.texto}<br>
                <strong><u>${link}</u></strong>
            </div>
            
                <div class="time">${data.date_formatting}</div>
        </div>

        `

    }

    //Convierte String a html
    function txtToHtml(txt) {
        const html = document.implementation.createHTMLDocument();
        html.body.innerHTML = txt;
        return html.body.firstElementChild;
    }

    const listUser1 = await getUrl("list_docentes/");

    //Pinta lista de docentes
    listUser1.data.forEach((element) => {
        const HTMLString = listUsuario1Template(element);
        const selectOption = document.getElementById("list-docentes");
        selectOption.innerHTML += HTMLString;
    });


    const cuerpoChat = document.getElementById("cuerpo-chat")

    //Pinta chats
    function mostrarChat(element) {
        element.addEventListener("click", async () => {
            const user1 = element.dataset.user1
            const user2 = element.dataset.user2
            cuerpoChat.innerHTML = ""
            const listMensajes = await getUrl(`all_chat/${user1}/${user2}/`)
            listMensajes.data.mensajes.reverse().forEach((element) => {
                const HTMLString = MensajeTemplate(element)
                cuerpoChat.innerHTML += HTMLString;
            })
            cuerpoChat.innerHTML += `<div class="answer-add"></div>`
        })
    }

    const listUser2 = document.getElementById("list-user2");

    //Pinta alumnos o tutores
    const selectOption = document.getElementById("list-docentes");
    selectOption.addEventListener("change", async () => {
        let value = parseInt(selectOption.value)
        listUser2.innerHTML = ""
        const listaUsuarios2 = await getUrl(`list_chat/${value}/`)
        listaUsuarios2.data.forEach((element) => {
            const HTMLString = listUsuario2Template(element.user2, value)
            const html = txtToHtml(HTMLString)
            mostrarChat(html)
            listUser2.append(html);
        })
    })
})();