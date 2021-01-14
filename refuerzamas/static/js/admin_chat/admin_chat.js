new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    

    data:{
        list_user: [],   
        display_name: '', 
        list_chats:[],
        conversaciones:null,
    },

    mounted(){
        const BASE_URL = window.location.protocol + "//" + window.location.host + "/adminchat/";
        var url = `${BASE_URL}list_users/`
        axios
            .get(url)
            .then(response=>(this.list_user = response.data))
    },
    computed:{
        buscarUsuario: function(){
            return this.list_user.filter((i)=>i.display_name.includes(this.display_name));
        }
    },
        
    methods:{
        
        getListChats(id_user){
            const BASE_URL = window.location.protocol + "//" + window.location.host + "/adminchat/";
            var url = `${BASE_URL}list_chat/${id_user}/`
            axios
            .get(url)
            .then(response=>(this.list_chats = response.data))
        },
        getConversaciones(id_chat){
            const BASE_URL = window.location.protocol + "//" + window.location.host + "/adminchat/";
            var url = `${BASE_URL}conversacion/${id_chat}/`
            axios
            .get(url)
            .then(response=>(this.conversaciones = response.data.reverse()))
        }

    },
    
})