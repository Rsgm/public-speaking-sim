module.exports = function (grunt) {

    var appConfig = grunt.file.readJSON('package.json');

    // Load grunt tasks automatically
    // see: https://github.com/sindresorhus/load-grunt-tasks
    require('load-grunt-tasks')(grunt);

    // Time how long tasks take. Can help when optimizing build times
    // see: https://npmjs.org/package/time-grunt
    require('time-grunt')(grunt);

    var pathsConfig = function (appName) {
        this.app = appName || appConfig.name;

        return {
            app: this.app,
            templates: this.app + '/templates',
            css: this.app + '/static/css',
            sass: this.app + '/static/sass',
            fonts: this.app + '/static/fonts',
            images: this.app + '/static/images',
            js: this.app + '/static/js',

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
                tasks: ['sass:dev', 'postcss'],
                options: {
                    atBegin: true
                }
            },

            urls: {
                files: ['<%= paths.app %>/**/urls.py', '<%= paths.app %>/config/urls.py'],
                tasks: ['bgShell:collectUrls'],
                options: {
                    atBegin: true
                }
            }

            // celery: {
            //     files: ['<%= paths.app %>/**/tasks.py', '<%= paths.app %>/taskapp/**/*.py'],
            //     tasks: ['bgShell:runCelery'],
            //     options: {
            //         atBegin: true
            //     }
            // }
        },

        // see: https://github.com/sindresorhus/grunt-sass
        sass: {
            dev: {
                options: {
                    sourceMap: true,
                    precision: 10,
                    outFile: '<%= paths.css %>/build.map.css'
                },
                files: {
                    '<%= paths.css %>/build.css': '<%= paths.sass %>/main.scss'
                }
            },
            dist: {
                options: {
                    outputStyle: 'compressed',
                    sourceMap: true,
                    precision: 10,
                    outFile: '<%= paths.css %>/build.map.css'
                },
                files: {
                    '<%= paths.css %>/build.css': '<%= paths.sass %>/main.scss'
                }
            }
        },

        //see https://github.com/nDmitry/grunt-postcss
        postcss: {
            options: {
                map: true, // inline sourcemaps

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
                cmd: '. <%= paths.venv %> && python <%= paths.manage %> runserver 0.0.0.0:8000'
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
        'postcss'
    ]);

    grunt.registerTask('default', [
        'build'
    ]);
};
