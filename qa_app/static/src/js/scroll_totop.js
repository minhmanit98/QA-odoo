odoo.define('qa_app.scroll_totop', function (require) {
'use strict';

	var core = require('web.core');
	var _t = core._t;
	var QWeb = core.qweb;

	window.onscroll = function() {scrollFunction()};

	function scrollFunction() {
	    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
	    	$('#back-to-top').fadeIn();
	    	$('#top').addClass('o_header_affix affix affixed');
	    	$('#top').removeClass('o_affix_enabled');


	    } else {
	    	$('#back-to-top').fadeOut();
	    	$('#top').removeClass('o_header_affix affix affixed');
	    	$('#top').addClass('o_affix_enabled');
	    }
	}
	$('#back-to-top').click(function () {
			$('body,html').animate({
				scrollTop: 0
			}, 400);
			return false;
	});

});