import Vue from 'vue'
import VueApollo from 'vue-apollo'
import { ApolloClient } from 'apollo-client'
import { createHttpLink } from 'apollo-link-http'
import { InMemoryCache } from 'apollo-cache-inmemory'
import { ApolloLink } from 'apollo-link'

const apiLink = new createHttpLink({
    uri: 'http://106.13.41.151/graphql/',
})

///请求头添加token
const middlewareLink = new ApolloLink((operation, forward) => {
    const token = localStorage.getItem('token');
    operation.setContext({
        headers: {
            Authorization: token? "JWT " + token : null
        }
    })
    return forward(operation)
})
  
///普通Apollo连接
const clientBase = new ApolloClient({
    link: apiLink,
    cache: new InMemoryCache()
})
  
///添加token的Apollo连接
const clientWithHeader = new ApolloClient({
    link: middlewareLink.concat(apiLink),
    cache: new InMemoryCache()
})
  
Vue.use(VueApollo)
  
const apolloProvider = new VueApollo({
    clients: {
        withtoken: clientWithHeader,
        base: clientBase
    },
    defaultClient: clientBase
})

export default apolloProvider;