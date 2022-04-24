const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');

var config = {
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
        new WebpackManifestPlugin(),
    ],
    output: {
        filename: 'js/[name].[contenthash].js',
        path: path.resolve(__dirname, './dist/assets'),
        publicPath: '/static/assets/',
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
            test: /node_modules\/svelte\/.*\.mjs$/,
            resolve: {
                fullySpecified: false
            }
        },
        {
            test: /\.elm$/,
            exclude: [/elm-stuff/, /node_modules/],
            use: {
                loader: "elm-webpack-loader",
                options: {
                    verbose: true,
                }
            },
        },
        {
            test: /\.css$/i,
            use: [
                MiniCssExtractPlugin.loader,
                'css-loader',
            ],
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

module.exports = (env, argv) => {
    if (argv.mode === 'development') {
        config.devtool = 'inline-source-map';

        config.output.publicPath = 'http://localhost:3000/assets/';

        config.devServer = {
            host: '0.0.0.0',
            port: 3000,
            headers: { 'Access-Control-Allow-Origin': '*' },
        };

        config.module.rules.push({
            test: /\.(html|svelte)$/,
            use: {
                loader: 'svelte-loader',
                options: {
                    compilerOptions: {
                        // NOTE Svelte's dev mode MUST be enabled for HMR to work
                        dev: true, // Default: false
                    },
                    // NOTE emitCss: true is currently not supported with HMR
                    // Enable it for production to output separate css file
                    emitCss: false, // Default: false
                    hotReload: true, // Default: false
                },
            },
        });

        config.module.rules.push({
            test: /\.s[ac]ss$/i,
            use: [
                'style-loader',
                'css-loader',
                'sass-loader'
            ],
        });
    }

    if (argv.mode === 'production') {
        config.module.rules.push({
            test: /\.(html|svelte)$/,
            use: {
                loader: 'svelte-loader',
                options: {
                    // NOTE emitCss: true is currently not supported with HMR
                    // Enable it for production to output separate css file
                    emitCss: true, // Default: false
                },
            },
        });

        config.module.rules.push({
            test: /\.s[ac]ss$/i,
            use: [
                MiniCssExtractPlugin.loader,
                'css-loader',
                'sass-loader'
            ],
        });
    }

    return config;
};
