$('.note-form .save-note').click(function(e){
    e.preventDefault(); // Stall form submit
    $('.note-form #next_state').val($(this).data('next-state'));
    $(this).parents('form:first').submit(); // Submit form
});
