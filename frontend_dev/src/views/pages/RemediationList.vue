<template>
    <v-container fluid class="down-top-padding">
        <v-row>
            <TableRemediation :dataRemediation="dataRemediation"></TableRemediation>
        </v-row>
    </v-container>
</template>
<script>
import TableRemediation from '../dashboard/components/TableRemediation';
import axios from 'axios';
import { mapActions } from 'vuex';

export default {
    components: {
        TableRemediation
    },
    data: () => ({
        dataRemediation: [],
    }),
    methods: {
        getDataRemediation() {
            axios.get("/remediadion/data").then(res => {
                this.dataRemediation = res.data
            })
        },
        ...mapActions(
            ['checkAuth']
        )
    },
    beforeMount() {
        this.checkAuth();
        this.getDataRemediation();
    }
}

</script>