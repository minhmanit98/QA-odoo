odoo.define('qa_app.sidebar', function (require) {
'use strict';
	var core = require('web.core');
		var fullHeight = function() {

			$('.js-fullheight').css('height', $(window).height());
			$(window).resize(function(){
				$('.js-fullheight').css('height', $(window).height());
			});

		};
		fullHeight();

		$('#sidebarCollapse').on('click', function () {
		  $('main #sidebar').toggleClass('active');
	  });

});