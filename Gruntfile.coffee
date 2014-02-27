module.exports = (grunt) ->
    # -----------------------------------
    # Options
    # -----------------------------------
    grunt.config.init
        compass:
            source:
                options:
                    sassDir: './static/scss'
                    cssDir: './static/css'
                    outputStyle: 'compressed'

        coffee:
            source:
                files:
                    './static/javascript/site.js': ['./static/coffeescript/*.coffee']

        watch:
            compass:
                files: ['./static/scss/*.scss']
                tasks: ['compass']
                options:
                    spawn: no
            coffee:
                files: ['./static/coffeescript/*.coffee']
                tasks: ['coffee']
                options:
                    spawn: no

    # -----------------------------------
    # register task
    # -----------------------------------
    grunt.registerTask 'dev', ['watch']

    # -----------------------------------
    # Plugins
    # -----------------------------------
    grunt.loadNpmTasks 'grunt-contrib-compass'
    grunt.loadNpmTasks 'grunt-contrib-coffee'
    grunt.loadNpmTasks 'grunt-contrib-watch'