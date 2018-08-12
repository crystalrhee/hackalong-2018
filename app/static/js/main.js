function checkStatus() {
	$('#github_url').on('click', function() {
	    $('.field-box').addClass('focus'); 
	});
	$('#github_url').focusin(function() {
	    $('.field-box').addClass('focus'); 
	});
	$(document).on('click', function(e) {
		if ($(e.target).is('#github_url') === false) {
			$('.field-box').removeClass('focus'); 
			checkForInput();
		}
	});
}

function checkForInput() {
    if ($('#github_url').val().length > 0) {
        $('.field-box').addClass('focus');
    } else {
        $('.field-box').removeClass('focus');
    }
}

$('#github_url').on('change keyup', function() {
    checkStatus();
});

