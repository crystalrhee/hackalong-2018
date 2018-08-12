$(document).ready(function() {
    $('#github_url').on('change', function() {
        var value = $(this).val();
        console.log('Selected Value: ', value);
    });

});
