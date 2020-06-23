odoo.define('qa_app.sidebar', function (require) {
'use strict';

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

		$().on('click', function () {
		   $('main #sidebar').toggleClass('active');
	  	});

		window.onscroll = function() {scrollFunction()};
		function scrollFunction() {
			if(document.documentElement.scrollTop == 0){
				if ($('main #sidebar').hasClass('active')){

				}else{
					$('main #sidebar').toggleClass('active');
				}

			}
		}

});