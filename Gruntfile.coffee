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

        shell:
            pythonServer:
                options:
                    stdin: no
                    stdout: yes
                    stderr: yes
                command: 'python manage.py runserver 0.0.0.0:8000'

        concurrent:
            dev:
                tasks: ['shell:pythonServer', 'watch']
                options:
                    logConcurrentOutput: yes
                    limit: @tasks.length

    # -----------------------------------
    # register task
    # -----------------------------------
    grunt.registerTask 'dev', ['concurrent:dev']

    # -----------------------------------
    # Plugins
    # -----------------------------------
    grunt.loadNpmTasks 'grunt-contrib-compass'
    grunt.loadNpmTasks 'grunt-contrib-coffee'
    grunt.loadNpmTasks 'grunt-contrib-watch'
    grunt.loadNpmTasks 'grunt-shell'
    grunt.loadNpmTasks 'grunt-concurrent'
