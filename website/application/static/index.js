$(function() {
          $('#sendBtn').bind('click', function() {
          var value = document.getElementById("msgText").value
          console.log(value)
            $.getJSON('/run',
            {val:value},
                function(data) {
              //do nothing
            });
            return false;
          });
        });

function validate(name){
	if (name.length >= 2){
		return true;
	}
	return false;
}