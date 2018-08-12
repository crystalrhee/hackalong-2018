function checkStatus() {
	$('#project').on('click', function() {
		$('.field-box').addClass('focus'); 
	});
	$('#project').focusin(function() {
		$('.field-box').addClass('focus'); 
	});
	$(document).on('click', function(e) {
		if ($(e.target).is('#project') === false) {
			$('.field-box').removeClass('focus'); 
			checkForInput();
		}
	});
}

function checkForInput() {
	if ($('#project').val().length > 0) {
		$('.field-box').addClass('focus');
	} else {
		$('.field-box').removeClass('focus');
	}
}

$(document).ready(function() {
	checkStatus();
});

$('#project').on('change keyup', function() {
	checkStatus();
});

$('.submit-btn').click(function(){
	$('form').addClass('hidden');
	$('.loading-container').removeClass('hidden');
});