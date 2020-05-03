odoo.define('qa_app.scroll_totop', function (require) {
'use strict';

	var core = require('web.core');
	var _t = core._t;
	var QWeb = core.qweb;

	window.onscroll = function() {scrollFunction()};

	function scrollFunction() {
	    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
	    	$('#back-to-top').fadeIn();
	        // document.getElementById("back-to-top").style.display = "block";
	    } else {
	    	$('#back-to-top').fadeOut();
	        // document.getElementById("back-to-top").style.display = "none";
	    }
	}
	function topFunction() {
	    $('body,html').animate({
				scrollTop: 0
			}, 400);
			return false;
	}
	$('#back-to-top').click(function () {
			$('body,html').animate({
				scrollTop: 0
			}, 400);
			return false;
	});

});