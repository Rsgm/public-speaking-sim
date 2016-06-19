module.exports = {
  entry: './web/vue/app.js',

  devtool: "source-map",

  output: {
    path: __dirname + '/speakeazy/static/',
    filename: 'build.js'
  },

  module: {
    loaders: [
      {
        test: /\.vue$/, // a regex for matching all files that end in `.vue`
        loader: 'vue'   // loader to use for matched files
      },

      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel'
      }
    ]
  },

  babel: {
    presets: ['es2015'],
    plugins: ['transform-runtime']
  }
};
