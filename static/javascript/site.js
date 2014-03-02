(function() {
  angular.module('app.controller', []).controller('NavigationController', [
    '$scope', '$injector', function($scope, $injector) {
      var $app, $state, $validator;
      $app = $injector.get('$app');
      $state = $injector.get('$state');
      $validator = $injector.get('$validator');
      $scope.user = $app.user;
      return $scope.showCreatePostModal = function($event) {
        $event.preventDefault();
        if (!$app.user.is_login) {
          $app.modal.loginRequired.show();
          return;
        }
        return $app.modal.post.show({
          submitCallback: function(model) {
            return $validator.validate(model.scope).success(function() {
              return $app.store.addPost(model.title, model.content).success(function() {
                $state.go($state.$current, null, {
                  reload: true
                });
                return $app.modal.post.hide();
              });
            });
          }
        });
      };
    }
  ]).controller('PostsController', [
    '$scope', '$injector', 'posts', function($scope, $injector, posts) {
      var $app, $state, $validator;
      $app = $injector.get('$app');
      $state = $injector.get('$state');
      $validator = $injector.get('$validator');
      $scope.posts = posts;
      $scope.deletePost = function($event, id) {
        $event.preventDefault();
        return $app.store.deletePost(id).success(function() {
          $state.go($state.$current, null, {
            reload: true
          });
          return $app.modal.post.hideCreate();
        });
      };
      return $scope.editPost = function($event, id) {
        var post, x, _i, _len, _ref;
        $event.preventDefault();
        _ref = posts.items;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          x = _ref[_i];
          if (x.id === id) {
            post = x;
          }
        }
        return $app.modal.post.show({
          title: post.title,
          content: post.content,
          submitCallback: function(model) {
            return $validator.validate(model.scope).success(function() {
              return $app.store.updatePost(id, model.title, model.content).success(function() {
                $state.go($state.$current, null, {
                  reload: true
                });
                return $app.modal.post.hide();
              });
            });
          }
        });
      };
    }
  ]);

}).call(this);

(function() {
  angular.module('app.directive', ['app.controller']).directive('appNavigation', function() {
    return {
      controller: 'NavigationController'
    };
  }).directive('appModalPost', [
    '$injector', function($injector) {
      return {
        scope: true,
        restrict: 'E',
        replace: true,
        templateUrl: '/static/view/modal/post.html',
        link: function(scope, element) {
          var $app, $timeout, $validator;
          $app = $injector.get('$app');
          $validator = $injector.get('$validator');
          $timeout = $injector.get('$timeout');
          scope.$on($app.broadcastChannel.showEditPost, function(self, object) {
            scope.title = object.title;
            scope.content = object.content;
            scope.submit = function($event) {
              $event.preventDefault();
              return object != null ? object.submitCallback({
                title: scope.title,
                content: scope.content,
                scope: scope
              }) : void 0;
            };
            $timeout(function() {
              return $validator.reset(scope);
            });
            return $(element).modal('show');
          });
          scope.$on($app.broadcastChannel.hideEditPost, function() {
            return $(element).modal('hide');
          });
          return $(element).on('shown.bs.modal', function() {
            return $(element).find('input:first').select();
          });
        }
      };
    }
  ]).directive('appModalLoginRequired', [
    '$injector', function($injector) {
      return {
        scope: true,
        restrict: 'E',
        replace: true,
        templateUrl: '/static/view/modal/login_required.html',
        link: function(scope, element) {
          var $app;
          $app = $injector.get('$app');
          scope.user = $app.user;
          scope.$on($app.broadcastChannel.showLoginRequired, function() {
            return $(element).modal('show');
          });
          return $(element).on('shown.bs.modal', function() {
            return $(element).find('.focus').focus();
          });
        }
      };
    }
  ]).directive('appPager', function() {
    return {
      scope: {
        pageList: '=appPager',
        urlTemplate: '@pagerUrlTemplate'
      },
      template: "<ul ng-if=\"pageList.total > 0\" class=\"pagination\">\n    <li ng-class=\"{disabled: !links.previous.enable}\">\n        <a ng-href=\"{{ links.previous.url }}\">&laquo;</a>\n    </li>\n\n    <li ng-repeat='item in links.numbers'\n        ng-if='item.show'\n        ng-class='{active: item.isCurrent}'>\n        <a ng-href=\"{{ item.url }}\">{{ item.pageNumber }}</a>\n    </li>\n\n    <li ng-class=\"{disabled: !links.next.enable}\">\n        <a ng-href=\"{{ links.next.url }}\">&raquo;</a>\n    </li>\n</ul>",
      link: function(scope) {
        var index, _i, _ref, _ref1, _results;
        scope.links = {
          previous: {
            enable: scope.pageList.has_previous_page,
            url: scope.urlTemplate.replace('#{index}', scope.pageList.index - 1)
          },
          numbers: [],
          next: {
            enable: scope.pageList.has_next_page,
            url: scope.urlTemplate.replace('#{index}', scope.pageList.index + 1)
          }
        };
        _results = [];
        for (index = _i = _ref = scope.pageList.index - 3, _ref1 = scope.pageList.index + 3; _i <= _ref1; index = _i += 1) {
          _results.push(scope.links.numbers.push({
            show: index >= 0 && index <= scope.pageList.max_index,
            isCurrent: index === scope.pageList.index,
            pageNumber: index + 1,
            url: scope.urlTemplate.replace('#{index}', index)
          }));
        }
        return _results;
      }
    };
  });

}).call(this);

(function() {
  angular.module('app', ['app.router', 'app.directive', 'app.validations']);

}).call(this);

(function() {
  angular.module('app.provider', []).provider('$app', function() {
    var $http, $injector, $rootScope;
    $injector = null;
    $http = null;
    $rootScope = null;
    this.setupProviders = function(injector) {

      /*
      Setup providers.
      @param injector: The $injector.
       */
      $injector = injector;
      $http = $injector.get('$http');
      return $rootScope = $injector.get('$rootScope');
    };
    this.broadcastChannel = {
      showEditPost: '$showEditPost',
      hideEditPost: '$hideEditPost',
      showLoginRequired: '$showLoginRequired'
    };

    /*
    is_login: yes / no
    id: 0
    permission: 0: anonymous, 1: root, 2: normal
    name: 'Guest'
    email: 'user@email.com'
    login_url: 'url'
    logout_url: 'url'
     */
    this.user = window.user;
    this.modal = {
      post: {

        /*
        Modals about post functions.
         */
        show: (function(_this) {
          return function(object) {
            if (object == null) {
              object = {};
            }

            /*
            @params object:
                title: ''
                content: ''
                submitCallback: ({title: '', content: '', scope: {}})->
             */
            return $rootScope.$broadcast(_this.broadcastChannel.showEditPost, object);
          };
        })(this),
        hide: (function(_this) {
          return function() {
            return $rootScope.$broadcast(_this.broadcastChannel.hideEditPost);
          };
        })(this)
      },
      loginRequired: {
        show: (function(_this) {
          return function() {
            return $rootScope.$broadcast(_this.broadcastChannel.showLoginRequired);
          };
        })(this)
      }
    };
    this.http = (function(_this) {
      return function(model) {
        return $http(model).error(function(data, status) {
          return _this.popMessage.error(status);
        });
      };
    })(this);
    this.store = {

      /*
      The data sotre provider.
       */
      getPosts: (function(_this) {
        return function(index) {
          if (index == null) {
            index = 0;
          }

          /*
          Get paged posts.
          @param index: The page index.
          @return:
              index: The page index.
              size: The page size.
              total: The total data.
              has_next_page: Has next page?
              has_previous_page: Has previous page?
              max_index: The max page index.
              items: [
                  id: The post id.
                  title: The post title.
                  content: The post content.
                  author: The author.
                  create_time: The create time.
                  deletable: Is this post coulde be deleted?
              ]
           */
          return _this.http({
            method: 'get',
            url: '/posts',
            params: {
              index: index
            }
          }).then(function(data) {
            var post, _i, _len, _ref;
            _ref = data.data.items;
            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
              post = _ref[_i];
              if (_this.user.permission === 1) {
                post.deletable = true;
              } else if (post.author.id === _this.user.id) {
                post.deletable = true;
              } else {
                post.deletable = false;
              }
            }
            return data.data;
          });
        };
      })(this),
      addPost: (function(_this) {
        return function(title, content) {
          return _this.http({
            method: 'post',
            url: '/posts',
            data: {
              title: title,
              content: content
            }
          });
        };
      })(this),
      deletePost: (function(_this) {
        return function(id) {
          return _this.http({
            method: 'delete',
            url: "/posts/" + id
          });
        };
      })(this),
      updatePost: (function(_this) {
        return function(id, title, content) {
          return _this.http({
            method: 'put',
            url: "/posts/" + id,
            data: {
              title: title,
              content: content
            }
          });
        };
      })(this)
    };
    this.popMessage = {
      error: function(status) {

        /*
        pop error message.
         */
        switch (status) {
          case 400:
            return $.av.pop({
              title: 'Input Failed',
              message: 'Please check input values.',
              template: 'error'
            });
          case 403:
            return $.av.pop({
              title: 'Permission denied',
              message: 'Please check your permission.',
              template: 'error'
            });
          default:
            return $.av.pop({
              title: 'Error',
              message: 'Loading failed, please try again later.',
              template: 'error'
            });
        }
      }
    };
    this.$get = [
      '$injector', (function(_this) {
        return function($injector) {
          _this.setupProviders($injector);
          return {
            broadcastChannel: _this.broadcastChannel,
            user: _this.user,
            modal: _this.modal,
            http: _this.http,
            store: _this.store,
            popMessage: _this.popMessage
          };
        };
      })(this)
    ];
  });

}).call(this);

(function() {
  angular.module('app.router', ['app.provider', 'app.controller', 'ui.router']).config([
    '$stateProvider', '$urlRouterProvider', '$locationProvider', function($stateProvider, $urlRouterProvider, $locationProvider) {
      $locationProvider.html5Mode(true);
      $urlRouterProvider.otherwise('/');
      $stateProvider.state('index', {
        url: '/',
        resolve: {
          posts: [
            '$app', function($app) {
              return $app.store.getPosts();
            }
          ]
        },
        views: {
          content: {
            templateUrl: '/static/view/content/posts.html',
            controller: 'PostsController'
          }
        }
      });
      return $stateProvider.state('posts', {
        url: '/posts?index',
        resolve: {
          posts: [
            '$app', '$stateParams', function($app, $stateParams) {
              return $app.store.getPosts($stateParams.index);
            }
          ]
        },
        views: {
          content: {
            templateUrl: '/static/view/content/posts.html',
            controller: 'PostsController'
          }
        }
      });
    }
  ]).run([
    '$injector', function($injector) {
      var $rootScope;
      $rootScope = $injector.get('$rootScope');
      NProgress.configure({
        showSpinner: false
      });
      $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState) {
        return NProgress.start();
      });
      $rootScope.$on('$stateChangeSuccess', function() {
        return NProgress.done();
      });
      return $rootScope.$on('$stateChangeError', function() {
        return NProgress.done();
      });
    }
  ]);

}).call(this);

(function() {
  angular.module('app.validations', ['validator']).config([
    '$validatorProvider', function($validatorProvider) {
      return $validatorProvider.register('required', {
        validator: /.+/,
        error: 'This field is required.'
      });
    }
  ]);

}).call(this);
