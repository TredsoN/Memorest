import {ApolloClient} from 'apollo-client'
import VueApollo from 'vue-apollo'
import Vue from "vue";


Vue.use(VueApollo);


const apolloClient = new ApolloClient({
    uri: 'http://106.13.41.151:8000/graphql'
});

const apolloProvider = new VueApollo({
    defaultClient: apolloClient,
});

export default apolloProvider