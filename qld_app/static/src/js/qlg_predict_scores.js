odoo.define('qld_app.qld_predict_scores', function (require) {
'use strict';
    var id_show;

    $('#button_create').on('click', function () {
         $('#create_predict_score').toggleClass('show');
    });
    $('.button_cancel').on('click', function () {
         $('.bg-lock').removeClass('show');
    });

    $('.button-option').on('click', function () {
        var form_id = '#form-'+$(this).attr("id")
         id_show = form_id;

         $(form_id).toggleClass('show');
    });

    $('.add-predict-subject').on('click', function () {
        var form_id = '#form-'+$(this).attr("id")
         id_show = form_id;
         $(form_id).toggleClass('show');
    });

    //  $('html:not(.button-option)').on('click', function () {
    //      console.log($(this))
    //     if($(id_show).hasClass('show')){
    //         $(id_show).removeClass('show');
    //     }
    // });





});