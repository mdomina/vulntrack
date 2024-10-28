<template><div></div></template>
<script>
export default {
    name: "Logout",
    mounted() {
            // Rimuove il token dal localStorage
            localStorage.removeItem('token');

            // Reindirizza l'utente alla pagina di login
            this.$router.push('/login');
    }
}


</script>