$(document).ready(function() {
    $('#id_of_your_textarea').summernote({
        callbacks: {
            onBlur: function(contents, $editable) {
                var code = $(this).summernote('code');
                // Remove <p> tags
                code = code.replace(/<\/?p[^>]*>/g, '');
                $(this).summernote('code', code);
            }
        }
    });
});

$('#summernote').summernote('removeFormat');
