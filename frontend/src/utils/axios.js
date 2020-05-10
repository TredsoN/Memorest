import axios from 'axios'

const instance = axios.create({
    baseURL: process.env.NODE_ENV === 'production'?'http://106.13.41.151' : '/api'
})

export default instance