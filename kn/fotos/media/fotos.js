'use strict';
(function(){
  function KNF(data){
    this.foto = null;
    this.fotos = {};
    this.read_fotos(this.get_url_path(), data);
  }

  KNF.prototype.change_path = function(path) {
    // Clear out the old
    $('#fotos').empty();
    // Update state
    this.path = path; // it is important we set path before changing location
    if (this.get_url_path() != path)
      this.pushState(path);

    // Update breadcrumbs
    $('#breadcrumbs').empty();
    var cur = '';
    $.each((path ? '/'+path : '').split('/'), function(k, component) {
      if (component !== '') {
        $('#breadcrumbs').append(document.createTextNode(' / '));
        if (!cur) {
          cur = component;
        } else {
          cur += '/' + component;
        }
      }

      var a = $('<a></a>').text(
        component ? component : 'fotos').appendTo('#breadcrumbs');
      var p = cur;
      a.attr('href', fotos_root+cur)
       .click(function(e) {
        if (e.ctrlKey || e.shiftKey || e.metaKey || e.button != 0) {
          return;
        }
        this.change_path(p);
        return false;
      }.bind(this))
    }.bind(this));

    if (!(path in this.fotos)) {
      // Fetch fotos
      this.fetch_fotos();
    } else {
      this.display_fotos();
    }
  };

  KNF.prototype.display_fotos = function() {
    if (!this.fotos[this.path])
      return;

    for (var name in this.fotos[this.path]) {
      (function(name) {
        var c = this.fotos[this.path][name];
        var srcset = c.thumbnail + " 1x, " +
                     c.thumbnail2x + " 2x";
        var thumb = $('<li><a><img class="lazy" /></a></li>');
        $('img', thumb)
            .attr('data-srcset', srcset)
            .attr('data-src', c.thumbnail);
        if (c.thumbnailSize)
          $('img', thumb)
              .attr('width', c.thumbnailSize[0])
              .attr('height', c.thumbnailSize[1]);
        var title = c.title;
        if (!title && c.type == 'album')
          title = c.name;
        if (title)
          $('<span></span>').text(title).appendTo(thumb);
        if (c.type == 'album') {
          $('> a', thumb)
            .attr('href', fotos_root + c.path)
            .click(function(e) {
              if (e.ctrlKey || e.shiftKey || e.metaKey || e.button != 0) {
                return;
              }
              this.change_path(c.path);
              return false;
            }.bind(this));
        }
        if (c.type == 'foto') {
          $('> a', thumb).attr('href', '#'+c.name);
        }
        thumb.appendTo('#fotos');
      }).call(this, name);
    }

    $(window).lazyLoadXT();

    if (this.get_hash() && this.foto === null) {
      this.change_foto(this.fotos[this.path][this.get_hash()]);
    }
  };

  KNF.prototype.cache_url = function(cache, path) {
    return "/foto/" + cache + "/" + encodeURI(path);
  };

  KNF.prototype.fetch_fotos = function() {
    var path = this.path;
    if (this.fotos[path] === null) {
      // fetch in progress
      return;
    }
    this.fotos[path] = null;
    this.api({action: 'list',
              path: path},
      function(data) {
        if(data.error) {
          $('#fotos').text(data.error);
          return;
        }

        this.read_fotos(path, data);

        this.display_fotos();
      }.bind(this));
  };

  KNF.prototype.read_fotos = function(path, data) {
    this.fotos[path] = {};

    var prev = null;
    $.each(data.children, function(i, c) {
      if (c.type == 'album') {
        c.thumbnail = this.cache_url('thumb', c.thumbnailPath);
        c.thumbnail2x = this.cache_url('thumb2x', c.thumbnailPath);
      } else {
        c.thumbnail = this.cache_url('thumb', c.path);
        c.thumbnail2x = this.cache_url('thumb2x', c.path);
      }
      if (c.type == 'foto') {
        c.full = this.cache_url('full', c.path);
        c.large = this.cache_url('large', c.path);
        c.large2x = this.cache_url('large2x', c.path);
      }
      this.fotos[path][c.name] = c;

      if (prev !== null) {
        prev.next = c;
        c.prev = prev;
      }

      prev = c;
    }.bind(this));
  }

  KNF.prototype.pushState = function (path) {
    history.pushState(undefined, '', fotos_root + path);
  }

  // Returns the path according to the current URL
  KNF.prototype.get_url_path = function() {
    return location.pathname.substr(fotos_root.length);
  };

  KNF.prototype.onpopstate = function() {
    var new_path = this.get_url_path();
    if (new_path === this.path)
      return;
    this.change_path(new_path);
  };

  // Returns the current photo name
  KNF.prototype.get_hash = function() {
    var hash = location.hash;
    if (hash.length < 1) {
      return '';
    }

    return hash.substr(1);
  }

  KNF.prototype.onhashchange = function() {
    this.change_foto(this.fotos[this.path][this.get_hash()]);
  }

  KNF.prototype.api = function(data, cb) {
    $.post(fotos_api_url, {
      csrfmiddlewaretoken: csrf_token,
      data: JSON.stringify(data),
    }, cb, "json");
  };

  KNF.prototype.change_foto = function(foto) {
    if (this.foto) {
      $('#foto').hide();
      $('html').removeClass('noscroll');
    }
    foto = foto || null;
    this.foto = foto;
    if (!foto) {
      this.pushState(this.get_url_path());
      return;
    }
    if (this.get_hash() != foto.name) {
      location.hash = '#' + foto.name;
    }
    $('html').addClass('noscroll');
    var fotoDiv = $('#foto > div');
    fotoDiv.empty()
    var srcset = foto.large + " 1x, " +
                 foto.large2x + " 2x"; 
    var navHead = $('<div></div>').appendTo(fotoDiv);
    if (foto.prev)
      $('<a class="prev">vorige</a>')
              .attr('href', '#'+foto.prev.name)
              .appendTo(navHead);
    $('<span></span>')
              .text(foto.title ? foto.title : foto.name)
              .appendTo(navHead);
    if (foto.next)
      $('<a class="next">volgende</a>')
              .attr('href', '#'+foto.next.name)
              .appendTo(navHead);
    var img = $('<img/>')
            .attr('srcset', srcset)
            .attr('src', foto.large);
    if (foto.largeSize)
      img.attr('width', foto.largeSize[0])
         .attr('height', foto.largeSize[1]);
    img.appendTo(fotoDiv);
    var navFooter = $('<div></div>')
              .appendTo(fotoDiv);
    $('<a class="orig">origineel</a>')
            .attr('href', foto.full)
            .appendTo(navFooter);
    $('<div class="clear"></div>').appendTo(navFooter);
    if (foto.description)
      $('<p></p>')
            .text('foto.description')
            .appendTo(navFooter);
    $('#foto').show();
  };

  KNF.prototype.run = function() {
    this.onpopstate();
    $(window).bind('popstate', this.onpopstate.bind(this));
    $(window).bind('hashchange', this.onhashchange.bind(this));
    $('#foto').click(function(e) {
      if (e.target.nodeName == 'A') return;
      this.change_foto(null);
      return false;
    }.bind(this));
    $(document).keydown(function(e) {
      if (!this.foto)
        return;
      // Escape
      if (e.which == 27) {
        this.change_foto(null);
        return false;
      }
      // left arrow
      if (e.which == 37) {
        this.change_foto(this.foto.prev);
        return false;
      }
      // right arrow
      if (e.which == 39) {
        this.change_foto(this.foto.next);
        return false;
      }
    }.bind(this));
  };

  $(document).ready(function(){
    (new KNF(fotos)).run();
  });
})();

/* vim: set et sta bs=2 sw=2 : */
