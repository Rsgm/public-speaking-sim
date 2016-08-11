var path = require('path');

module.exports = {
  entry: {
    a: path.resolve(__dirname, 'speakeazy/web/vue/groupadmin/app.js')
  },

  output: {
    path: path.resolve(__dirname, 'speakeazy/static/js'),
    filename: '[name].build.js'
  },

  module: {
    loaders: [
      {
        test: /\.vue$/, // a regex for matching all files that end in `.vue`
        exclude: /node_modules/,
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
