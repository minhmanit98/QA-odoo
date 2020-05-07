odoo.define('qa_app.navbar', function (require) {
'use strict';

	var core = require('web.core');
	var _t = core._t;
	var QWeb = core.qweb;

	$(window).scroll(function() {
		if ($(document).scrollTop() > 50) {
			$('#nav').addClass('affix');
			console.log("OK");
		} else {
			$('#nav').removeClass('affix');
		}
	});

	window.onscroll = function() {scrollFunction()};

	function scrollFunction() {
	    if ($(document).scrollTop() > 50) {
               	$('#top').addClass('o_header_affix affix affixed');
	    		$('#top').removeClass('o_affix_enabled');

            } else {
	    		$('#top').removeClass('o_header_affix affix affixed');
	    		$('#top').addClass('o_affix_enabled');
            }
	}

	$('.navTrigger').click(function () {
    $(this).toggleClass('active');
    console.log("Clicked menu");
    $("#top_menu_collapse").toggleClass("show_list");
    $("#top_menu_collapse").fadeIn();

});


});