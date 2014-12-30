function IBLBadgesEdit(runtime, element) {
    $('.save-button', element).bind('click', function() {
        var data = {
            'bg_id': $('#edit_badge_id').val(),
            'debug_mode': $('#debug_mode').val(),
            'bg_provider': $('#bg_provider').val(),
	    'form_text':$('#edit_form_id').val(),
	    'congratulations_text':$('#congratulations_text').val(),
	    'enough_text':$('#enough_text').val(),
	    'required_score':$('#required_score').val(),
	    'badge_pro_user':$('#edit_badge_pro_user').val(),
	    'badge_pro_pwd':$('#edit_badge_pro_pwd').val(),
        };
        var handlerUrl = runtime.handlerUrl(element, 'studio_save');
        $.post(handlerUrl, JSON.stringify(data)).complete(function() {
            window.location.reload(false);
        });
    });

    $('.cancel-button', element).bind('click', function() {
        runtime.notify('cancel', {});
    });
}
