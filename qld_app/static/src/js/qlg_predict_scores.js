odoo.define('qld_app.qld_predict_scores', function (require) {
'use strict';
    var id_show;
    var array_input = [];
    var rpc = require('web.rpc');


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

    function checkInputSame(obj) {
        var check = false;
        for (var i = 0; i < array_input.length; i++) {
            if (array_input[i].id === obj.id) {
                array_input[i] = obj;
                check = true;
            }
        }
        if (!check){
            array_input.push(obj);
        }
    }
    function loadDataInput() {
         $('#input_scores_custom').empty();
         for (var i = 0; i < array_input.length; i++) {
             var data_id = array_input[i].id;
             var data_value = array_input[i].value;
             $('#input_scores_custom').append('<input type=\"hidden\" ' +
                'name=\"custom'+i+'\" value=\"'+data_id+'/'+data_value+'\" readonly=\"True\"/>');
             rpc.query({
                model: 'utc2.qld.predict.scores',
                method: 'search_read',
                args: [[['id','=',data_id]],['id','subject_name','scores_4custom']],
                }).then(function(res) {
                   $('#input_scores_custom').append('<input type=\"text\" class=\"input-text text-line color-text text-tt width-100\" ' +
                 'value=\"'+res[0].subject_name+': '+res[0].scores_4custom+' -> '+data_value+'\" readonly=\"True\"/>');
            });
         }
    }

    $('input').on('input', function() {
        if($(this).attr('name') === 'scores_4custom'){
            var id = String($(this).attr('id'));
            var value = String($(this).val());
            var input_change = '{"id" : "'+id+'", "value" : "'+value+'"}';
            var obj = JSON.parse(input_change)
            if(array_input.length === 0){
                array_input.push(obj);
            }else{
                checkInputSame(obj);
            }
        }
        loadDataInput();
    });

    //  $('html:not(.button-option)').on('click', function () {
    //      console.log($(this))
    //     if($(id_show).hasClass('show')){
    //         $(id_show).removeClass('show');
    //     }
    // });





});