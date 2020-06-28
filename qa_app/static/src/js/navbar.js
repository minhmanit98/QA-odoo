odoo.define('qa_app.navbar', function (require) {
'use strict';
	$(window).scroll(function() {
		if ($(document).scrollTop() > 100) {
			$('#nav-min').addClass('o_header_affix fixed-top');
		} else {
			$('#nav-min').removeClass('o_header_affix fixed-top');
		}
	});
	$('.navTrigger').click(function () {
    $(this).toggleClass('active');
    console.log("Clicked menu");
    $("#top_menu_collapse").toggleClass("show_list");
    $("#top_menu_collapse").fadeIn();

});


});