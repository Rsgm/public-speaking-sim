module.exports = function (grunt) {

  var appConfig = grunt.file.readJSON('package.json');

  // Load grunt tasks automatically
  // see: https://github.com/sindresorhus/load-grunt-tasks
  require('load-grunt-tasks')(grunt);

  // Time how long tasks take. Can help when optimizing build times
  // see: https://npmjs.org/package/time-grunt
  require('time-grunt')(grunt);

  require("webpack");
  var webpackConfig = require("./webpack.config.js");

  var pathsConfig = function (appName) {
    this.app = appName || appConfig.name;

    return {
      app: this.app,
      css: this.app + '/static/css',
      images: this.app + '/static/images',

      sass: this.app + '/web/sass',
      js: this.app + '/web/js',
      vue: this.app + '/web/vue',

      manage: 'manage.py',
      venv: 'venv/bin/activate'
    }
  };

  grunt.initConfig({
    paths: pathsConfig(),
    pkg: appConfig,

    // see: https://github.com/gruntjs/grunt-contrib-watch
    watch: {
      gruntfile: {
        files: ['Gruntfile.js']
      },

      css: {
        files: ['<%= paths.sass %>/**/*.{scss,sass}'],
        tasks: ['sass:dev', 'postcss:dev'],
        options: {
          atBegin: true
        }
      },

      vue: {
        files: ['<%= paths.vue %>/**/*.{js,vue}'],
        tasks: ['webpack:dev'],
        options: {
          atBegin: true
        }
      },

      urls: {
        files: ['speakeazy/**/urls.py', 'config/urls.py'],
        tasks: ['bgShell:collectUrls'],
        options: {
          atBegin: true
        }
      }
    },

    // see: https://github.com/sindresorhus/grunt-sass
    sass: {
      dev: {
        options: {
          sourceMapEmbed: true,
          precision: 10
        },
        files: {
          '<%= paths.css %>/build.css': '<%= paths.sass %>/main.scss'
        }
      },
      dist: {
        options: {
          outputStyle: 'compressed',
          precision: 10
        },
        files: {
          '<%= paths.css %>/build.css': '<%= paths.sass %>/main.scss'
        }
      }
    },

    //see https://github.com/nDmitry/grunt-postcss
    postcss: {
      dev: {
        options: {
          map: true // inline sourcemaps
        },
        dist: {
          src: '<%= paths.css %>/*.css'
        }
      },
      dist: {
        options: {
          processors: [
            require('pixrem')(), // add fallbacks for rem units
            require('autoprefixer')({
              browsers: [
                'Android 2.3',
                'Android >= 4',
                'Chrome >= 20',
                'Firefox >= 24',
                'Explorer >= 8',
                'iOS >= 6',
                'Opera >= 12',
                'Safari >= 6'
              ]
            }), // add vendor prefixes
            require('cssnano')({mergeRules: false}) // minify the result
          ]
        },
        dist: {
          src: '<%= paths.css %>/*.css'
        }
      }
    },

    // https://github.com/webpack/grunt-webpack
    webpack: {
      options: webpackConfig,
      build: {},
      dev: {
        progress: false,
        debug: true,
        devtool: 'source-map',
        failOnError: false
      }
    },

    // see: https://npmjs.org/package/grunt-bg-shell
    bgShell: {
      _defaults: {
        bg: true
      },
      collectUrls: {
        cmd: '. <%= paths.venv %> && python <%= paths.manage %> collectstatic_js_reverse'
      },
      runDjango: {
        cmd: '. <%= paths.venv %> && python <%= paths.manage %> runserver'
      },
      runCelery: {
        cmd: '. <%= paths.venv %> && celery -A speakeazy.taskapp worker -l info'
      }
    }
  });

  grunt.registerTask('serve', [
    'bgShell:runDjango',
    'bgShell:runCelery',
    'watch'
  ]);

  grunt.registerTask('build', [
    'sass:dist',
    'postcss:dist',
    'webpack:build'
  ]);

  grunt.registerTask('default', [
    'build'
  ]);
};
