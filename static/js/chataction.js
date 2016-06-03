$(document).ready(function(){

	$('.msg_head').click(function(){
		$('.msg_wrap').slideToggle('slow');
	});

	$('.close').click(function(){
		$('.msg_box').hide();
	});

	$('.userchat').click(function(){
		$('.msg_wrap').show();
		$('.msg_box').show();
	});

	$('textarea').keypress(
    function(e){
        if (e.keyCode == 13) {
            var msg = $(this).val();
			$(this).val('');
			if(msg!='')
			$('<div class="msg_b">'+msg+'</div>').insertBefore('.msg_push');
			$('.msg_body').scrollTop($('.msg_body')[0].scrollHeight);
        }
    });

});