odoo.define('qa_app.navbar', function (require) {
'use strict';
	$(window).scroll(function() {
		if ($(document).scrollTop() > 100) {
			$('#nav').addClass('affix');
			$('#top').addClass('o_header_affix affix affixed');
	    	$('#top').removeClass('o_affix_enabled');
		} else {
			$('#nav').removeClass('affix');
			$('#top').removeClass('o_header_affix affix affixed');
			$('#top').addClass('o_affix_enabled');
		}
	});
	$('.navTrigger').click(function () {
    $(this).toggleClass('active');
    console.log("Clicked menu");
    $("#top_menu_collapse").toggleClass("show_list");
    $("#top_menu_collapse").fadeIn();

});


});