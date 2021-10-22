const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');
const HtmlWebpackPlugin = require('html-webpack-plugin');
var path = require('path');

module.exports = merge(common, {
    mode: 'development',
    devtool: 'inline-source-map',
    devServer: {
        static: {
            directory: path.join(__dirname, 'assets'),
        },
        host: '0.0.0.0',
        port: 3000,
    },
    plugins: [
        new HtmlWebpackPlugin({
            title: 'Diagho (dev)',
        }),
    ],
});
