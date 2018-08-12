function checkStatus() {
	$('#username').on('click', function() {
		$('.field-box').addClass('focus'); 
	});
	$('#username').focusin(function() {
		$('.field-box').addClass('focus'); 
	});
	$(document).on('click', function(e) {
		if ($(e.target).is('#username') === false) {
			$('.field-box').removeClass('focus'); 
			checkForInput();
		}
	});
}

function checkForInput() {
	if ($('#username').val().length > 0) {
		$('.field-box').addClass('focus');
	} else {
		$('.field-box').removeClass('focus');
	}
}

$(document).ready(function() {
	checkStatus();
});

$('#username').on('change keyup', function() {
	checkStatus();
});