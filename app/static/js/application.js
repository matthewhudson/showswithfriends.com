$(function () {

  var body_height = 0, first_event;

  var $intro = $('#overview .container .intro');

  _.templateSettings.variable = "rc";


  var hero_template = _.template($("script.hero-template").html());

  var modal = function () {
    var my = {}, that = {};
    my.el = $('#overlay');
    
    my.template = _.template($("script.modal-template").html());

    my.el.click(function (e) {
      if (_.indexOf(['container-inner', 'container-middle', 'container-outer', 'container'], e.target.className) >= 0) {
        that.hide();
      }
    });

    $(document).keydown(function (evt) {
      evt = evt || window.event;
      var charCode = evt.which || evt.keyCode;
      var charStr = String.fromCharCode(charCode);

      // BACKSPACE
      if (charCode === 8) {
        evt.preventDefault();
        that.hide();
      }

      // ENTER
      if (charCode === 13) {
        that.hide();
      }

      // ESCAPE
      if (charCode === 27) {
        that.hide();
      }
    });


    that.show = function () {

      $('body').css('overflow', 'hidden');
      my.el.show();
    };

    that.hide = function () {
      $('body').css('overflow', 'auto');
      my.el.hide();
    };

    that.addContent = function(data) {
      my.el.html(my.template({
        title : data.title,
        url : data.url,
        venue_name : data.venue_name,
        venue_city : data.venue_city,
        image : data.image,
        datetime : data.datetime
      }));
      $('.artist-bg').html('<img src="' + data.image + '" />');
    };
    return that;
  };

  $('.event').livequery(function () {
      if (!first_event) first_event = $(this).find('.id').html()
    $(this).find('.datetime').html(Date.parse($(this).find('.datetime').html()).toString("dddd, MMMM d, yyyy @ h:mm tt"));
  });

  var $overview = $('#overview')
  var $hero = $('#overview .container .info');
  $('.event').livequery(function () {
    $(this).waypoint(function (direction) {
      if (direction === 'down') {
        $intro.hide();
        $hero.show();
        $(this).stop(true, true).animate({ opacity: 0 }, { queue : false }, 'fast');
      } else {
        $(this).stop(true, true).animate({ opacity: 1 }, { queue : false }, 'fast');

        // Reset the hero unit if scrolling to top from bottom
        if ($(this).find('.id').html() === first_event) {
          $hero.hide();
          $intro.show();
        }
      }
      $hero.html(hero_template({
        title : ellipsis($(this).find('.title b').text()),
        url : $(this).find('.url').html(),
        venue_name : $(this).find('.venue-name').text(),
        venue_city : $(this).find('.venue-city').html(),
        image : $(this).find('.image').attr('src'),
        datetime : $(this).find('.datetime').html(),
        performers_id : $(this).find('.performers-id').html()
      }));
      $hero.find('.image').hide().fadeIn(250);
      $overview.stop(true, true).fadeTo('slow', 0.95).fadeTo('fast', 1.0);
      // HACK
      body_height = $('body').height()
    }, {
      offset: 280
    });
  });
  
  $('.line').livequery(function () {
    $(this).css('height', body_height);
  });

  $('.box .image').livequery(function () {
    $(this).waypoint(function (direction) {
      if (direction === 'down') {
        $(this).stop(true, true).fadeOut(250).animate({ width: 250, height: 250, borderRadius: 125, left: -200 }, { queue : false }, 'slow');
      } else {
        $(this).stop(true, true).fadeIn(250).animate({ width: 120, height: 120, borderRadius: 60, left: -136 }, { queue : false }, 'slow');
      }
    }, {
      offset: 300
    });
  });

  function ellipsis (string) {
    if (string.length > 45) {
      return string = string.substring(0, 44) + "...";
    }
    return string
  }
  modal = modal();
  
  var data = null;
  $('.info .btn').livequery(function () {
    $(this).click(function (ev) {

      ev.preventDefault();
      data = $(this).parent().parent().parent();
      modal.addContent({
        title : data.find('.title').text(),
        url : data.find('.url').html(),
        venue_name : data.find('.venue-name').html(),
        venue_city : data.find('.venue-city').html(),
        image : data.find('.image').attr('src'),
        datetime : data.find('.datetime').html(),
        spotify : 'spotify:user:erebore:playlist:788MOXyTfcUb1tdw4oC7KJ'
      })
      modal.show();

      // Load Spotify if performers.links.provider === spotify
      seatgeek.performers({ 'id': data.find('.performers-id').html() }, function (performer) {
        if (performer.performers[0].links.length)
        _.each(performer.performers[0].links, function (v, k) {
          if (v.provider === "spotify") {
            $('.spotify').html('<iframe src="https://embed.spotify.com/?uri=' + v.id + '" width="450" height="100" frameborder="0" allowtransparency="true"></iframe>')
          }
        })
      });
      return false;
    });
  });

  $('#footer').css('marginTop', $(window).height() - 450);
});