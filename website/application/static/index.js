$(function() {
          $('a#test').bind('click', function() {
            $.getJSON('/run',
                function(data) {
              //do nothing
            });
            return false;
          });
        });