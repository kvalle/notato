$('.note-form .save-note').click(function(e){
    e.preventDefault(); // Stall form submit
    $('.note-form #target_state').val($(this).data('target-state'));
    $(this).parents('form:first').submit(); // Submit form
});
