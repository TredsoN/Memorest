module.exports = {
    // webpack 链接 API，用于生成和修改 webapck 配置
    // https://github.com/mozilla-neutrino/webpack-chain
    chainWebpack: (config) => {
        //graphql
        config.module
            .rule('graphql')
            .test(/(\.gql|\.graphql)$/)
            .use('graphql-tag/loader')
            .loader('graphql-tag/loader')
            .end()
    },
    devServer : {
        port: 8080,
        proxy : {
            '/api': {
                target: 'http://106.13.41.151',
                changeOrigin: true,
                pathRewrite:{
                    '^/api':''
                }
            }
        }
    }
};
