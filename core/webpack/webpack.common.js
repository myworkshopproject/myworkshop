const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');

module.exports = {
    entry: {
        base: './src/base.js',
        signup: './src/signup.js',
    },
    plugins: [
        new CleanWebpackPlugin(),
        new MiniCssExtractPlugin({
            filename: 'css/[name].[contenthash].css',
        }),
        new BundleTracker({
            filename: 'webpack-stats.json',
        }),
        new WebpackManifestPlugin()
    ],
    output: {
        filename: 'js/[name].[contenthash].js',
        path: path.resolve(__dirname, '../dist/assets'),
        publicPath: '/assets/',
    },
    optimization: {
        moduleIds: 'deterministic',
        runtimeChunk: 'single',
        splitChunks: {
            cacheGroups: {
                vendor: {
                    test: /[\\/]node_modules[\\/]/,
                    name: 'vendors',
                    chunks: 'all',
                },
            },
        },
    },
    resolve: {
        alias: {
            svelte: path.resolve('node_modules', 'svelte')
        },
        extensions: ['.mjs', '.js', '.svelte'],
        mainFields: ['svelte', 'browser', 'module', 'main']
    },
    module: {
        rules: [{
                test: /\.(html|svelte)$/,
                use: 'svelte-loader'
            },
            {
                test: /node_modules\/svelte\/.*\.mjs$/,
                resolve: {
                    fullySpecified: false
                }
            },
            {
                test: /\.elm$/i,
                exclude: [/elm-stuff/, /node_modules/],
                use: {
                    loader: "elm-webpack-loader",
                    options: {}
                },
            },
            {
                test: /\.css$/i,
                use: [MiniCssExtractPlugin.loader, 'css-loader'],
            },
            {
                test: /\.s[ac]ss$/i,
                use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader'],
            },
            {
                test: /\.(png|svg|jpg|jpeg|gif)$/i,
                type: 'asset/resource',
                generator: {
                    filename: 'img/[contenthash][ext][query]',
                },
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/i,
                type: 'asset/resource',
                generator: {
                    filename: 'fonts/[contenthash][ext][query]',
                },
            },
        ],
    },
};
