(function() {

$('#parent').removeClass('hidden');
$('#parent').addClass('active');

//$('.selectpicker').selectpicker({
//  size: 4
//});
//
//$('.selectpicker').selectpicker('selectAll');
//console.log(window.location.href);
var query = window.urlUtils.getQueryParameter(window.location.href, 'request');

//console.log(query);
$('#summary').attr('href', '/summary/?request='+ encodeURI(query));
//$('#analysis').attr('href', '/analysis/?request='+ encodeURI(query));
$('#clustering').attr('href', '/clustering/?request='+ encodeURI(query));
$('#pivot').attr('href','/pivot/?request=' + encodeURI(query));
$('#association').attr('href','/association/?request=' + encodeURI(query));
$('#discover').attr('href','/discover/');

//$('#comparison a').attr('href', '/compare/?request='+ encodeURI(query));


//console.log("Changed analysis href");
//console.log("Inside brand summary")
var is_first_load = true;
var flag1;  // True if query string contains '.csv', else False
//console.log(query);
if(query.indexOf('.csv')!=-1){
        flag1 = true;
    }
    else{
        flag1 = false;
    }

var top_pos_neg_resp = [];
var selStartDate = "2011-01-01";
var today = new Date();
var selEndDate = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
//console.log("selenddate=", selEndDate);
//init_sel_date();

function init_sel_date(){
    var init_date = $('input[name="daterange"]').val();
    //code to parse date from init_date and initialize selStartDate and selEndDate
}

if(flag1 == true){ //contains .csv
        //console.log($('#summary-filters-wrapper'));
        $('#summary-filters-wrapper').addClass('d-none');

        load_count_cards();
        load_all_charts();
    }
    else{  // flag1 == false
        $('#summary-filters-wrapper').removeClass('d-none');

        load_brand1();
    }


function load_count_cards()
{

    if (flag1 == false){
        //console.log(selStartDate,selEndDate);
        var brand = [];
        $('#brand1 .selected .text').each(function(index){
//            console.log($(this).text());
            brand.push($(this).text());
        });
        //console.log(brand);

        var source = [];
        $('#source1 .selected .text').each(function(index){
            source.push($(this).text());
        });
        //console.log(source);

        var sku = [];
        $('#sku1 .selected .text').each(function(index){
            sku.push($(this).text());
        });
        //console.log(sku);

        $.ajax({
           type: "GET",
           url: "/service/summary_countRevCards/",

           data: { 'query': query , 'brand': JSON.stringify(brand), 'source': JSON.stringify(source),
           'sku': JSON.stringify(sku), 'fromDate': JSON.stringify(selStartDate), 'toDate': JSON.stringify(selEndDate) },

           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
                //console.log(response);
                $('#totalbox').text("(" + response[0] + ")");
                $('#positivebox').text("(" + response[1] + ")");
                $('#negativebox').text("(" + response[2] + ")");

           },
           failure: function (response) {
//               alert("failed");
               $('#totalbox').text("0");
               $('#positivebox').text("0");
               $('#negativebox').text("0");
           }
        });
     }
     else{  // if flag1 is true
//        console.log(" inside countcards");
         $.ajax({
           type: "GET",
           url: "/service/summary_countRevCardsOverall/",

           data: { 'query': query  },

           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
                //console.log(response);
                $('#totalbox').append("(" + response[0] + ")");
                $('#positivebox').text("(" + response[1] + ")");
                $('#negativebox').text("(" + response[2] + ")");

           },
           failure: function (response) {
//               alert("failed");
               $('#totalbox').text("0");
               $('#positivebox').text("0");
                $('#negativebox').text("0");

           }
        });
     }
}


function load_all_charts()
    {
        load_categ_chart();
        load_chart1();
        //load_chart2();
        //load_chart3();
        if(flag1 == false){
            $('#brandsummaryChartDiv').removeClass('d-none');
            load_brandsummary_chart();
        }
        else{
            $('#brandsummaryChartDiv').addClass('d-none');
        }
        load_pie_chart();
        load_top_pos_neg();
        load_pos_posts();
        load_neg_posts();
        load_senti_charts();
        load_trigdriv_charts();
        load_wc_filter();
        load_wordcloud();
    }


$("#pos_posts").change(function(){
    load_pos_posts();
});

$("#neg_posts").change(function(){
    load_neg_posts();
});

function load_top_pos_neg(){
    if (flag1 == false){

        //console.log(selStartDate,selEndDate);
        var brand = [];
        $('#brand1 .selected .text').each(function(index){
//            console.log($(this).text());
            brand.push($(this).text());
        });
        //console.log(brand);

        var source = [];
        $('#source1 .selected .text').each(function(index){
            source.push($(this).text());
        });
        //console.log(source);

        var sku = [];
        $('#sku1 .selected .text').each(function(index){
            sku.push($(this).text());
        });
        //console.log(sku);


        $.ajax({
           type: "GET",
           url: "/service/summary_topposneg/",

           data: { 'query': query , 'brand': JSON.stringify(brand), 'source': JSON.stringify(source),
           'sku': JSON.stringify(sku), 'fromDate': JSON.stringify(selStartDate)
           , 'toDate': JSON.stringify(selEndDate) },

           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
                //standard response includes a set of 4 records. 1st 2 being top 2 positive reviews in order,
                //and next 2 being top negative reviews in order
                parsed_resp = JSON.parse(response);
                //console.log(parsed_resp);
                top_pos_neg_resp = parsed_resp;
                //to populate default positive post 1 and negative post 1
                if(parsed_resp.length == 4){ // if 4 records found, 2 are positive 2 are negative
                    $('#rPosTitle').text(parsed_resp[0]['fields']['rTitle']);
                    $('#rPosText').text(parsed_resp[0]['fields']['rText']);
                    $('#rNegTitle').text(parsed_resp[2]['fields']['rTitle']);
                    $('#rNegText').text(parsed_resp[2]['fields']['rText']);
                }
                else if(parsed_resp.length == 3){ //1st record is anyway 1st positive post
                    $('#rPosTitle').text(parsed_resp[0]['fields']['rTitle']);
                    $('#rPosText').text(parsed_resp[0]['fields']['rText']);
                    if(parseInt(parsed_resp[1]['fields']['rRating']) > 2){ //if second record is positive, then third record is 1st negative post
                        $('#rNegTitle').text(parsed_resp[2]['fields']['rTitle']);
                        $('#rNegText').text(parsed_resp[2]['fields']['rText']);
                    }
                    else { // if second record is negative, then that is the 1st negative post
                        $('#rPosTitle').text("No records available");
                        $('#rPosText').text(" ");
                        $('#rNegTitle').text(parsed_resp[1]['fields']['rTitle']);
                        $('#rNegText').text(parsed_resp[1]['fields']['rText']);
                    }
                }
                else if (parsed_resp.length == 2){ //if 2 records found
                    if(parseInt(parsed_resp[0]['fields']['rRating']) > 2){ //if 1st record is positive, then it is 1st positive post
                        $('#rPosTitle').text(parsed_resp[0]['fields']['rTitle']);
                        $('#rPosText').text(parsed_resp[0]['fields']['rTitle']);
                        if(parseInt(parsed_resp[1]['fields']['rRating']) > 2){ //if second record is also positive,
                        //then there are no negative records
                            $('#rNegTitle').text("No records available");
                            $('#rNegText').text(" ");
                        }
                        else{ //if second record is negative, then that is the 1st negative post
                            $('#rNegTitle').text(parsed_resp[1]['fields']['rTitle']);
                            $('#rNegText').text(parsed_resp[1]['fields']['rText']);
                        }
                    }
                    else{ //if first record itself is negative,
                    //then that is the 1st negative post, and there are no positive records to show
                        $('#rPosTitle').text("No records available");
                        $('#rPosText').text(" ");
                        $('#rNegTitle').text(parsed_resp[0]['fields']['rTitle']);
                        $('#rNegText').text(parsed_resp[0]['fields']['rText']);
                    }
                }
                else if(parsed_resp.length == 1){ //if 1 record found
                    if(parseInt(parsed_resp[0]['fields']['rRating']) > 2){ //if record is positive,
                    //then there are no negative records to show (even pos post 2 will be empty)
                        $('#rPosTitle').text(parsed_resp[0]['fields']['rTitle']);
                        $('#rPosText').text(parsed_resp[0]['fields']['rTitle']);
                        $('#rNegTitle').text("No records available");
                        $('#rNegText').text(" ");
                    }
                    else{ // if record is negative, then that is the 1st negative post (even neg post 2 will be empty)
                    //also there are no positive records to show
                        $('#rPosTitle').text("No records available");
                        $('#rPosText').text(" ");
                        $('#rNegTitle').text(parsed_resp[0]['fields']['rTitle']);
                        $('#rNegText').text(parsed_resp[0]['fields']['rText']);
                    }
                }
                else{ //if no records retrieved
                    $('#rPosTitle').text("No records available");
                    $('#rPosText').text(" ");
                    $('#rNegTitle').text("No records available");
                    $('#rNegText').text(" ");
                }
           },
           failure: function (response) {
               alert("failed");
                $('#rPosTitle').text("Failed to retrieve data!");
                $('#rPosText').text("Please reload the page");
                $('#rNegTitle').text("Failed to retrieve data!");
                $('#rNegText').text("Please reload the page");
           }
        });
     }
     else{  // if flag1 is true
         $.ajax({
           type: "GET",
           url: "/service/summary_topposnegOverall/",

           data: { 'query': query  },

           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
                parsed_resp = JSON.parse(response);
                //console.log(parsed_resp);
                top_pos_neg_resp = parsed_resp;
                //to populate default positive post 1 and negative post 1
                if(parsed_resp.length == 4){ // if 4 records found, 2 are positive 2 are negative
                    $('#rPosTitle').text(parsed_resp[0]['fields']['rTitle']);
                    $('#rPosText').text(parsed_resp[0]['fields']['rText']);
                    $('#rNegTitle').text(parsed_resp[2]['fields']['rTitle']);
                    $('#rNegText').text(parsed_resp[2]['fields']['rText']);
                }
                else if(parsed_resp.length == 3){ //1st record is anyway 1st positive post
                    $('#rPosTitle').text(parsed_resp[0]['fields']['rTitle']);
                    $('#rPosText').text(parsed_resp[0]['fields']['rText']);
                    if(parseInt(parsed_resp[1]['fields']['rRating']) > 2){ //if second record is positive, then third record is 1st negative post
                        $('#rNegTitle').text(parsed_resp[2]['fields']['rTitle']);
                        $('#rNegText').text(parsed_resp[2]['fields']['rText']);
                    }
                    else { // if second record is negative, then that is the 1st negative post
                        $('#rPosTitle').text("No records available");
                        $('#rPosText').text(" ");
                        $('#rNegTitle').text(parsed_resp[1]['fields']['rTitle']);
                        $('#rNegText').text(parsed_resp[1]['fields']['rText']);
                    }
                }
                else if (parsed_resp.length == 2){ //if 2 records found
                    if(parseInt(parsed_resp[0]['fields']['rRating']) > 2){ //if 1st record is positive, then it is 1st positive post
                        $('#rPosTitle').text(parsed_resp[0]['fields']['rTitle']);
                        $('#rPosText').text(parsed_resp[0]['fields']['rTitle']);
                        if(parseInt(parsed_resp[1]['fields']['rRating']) > 2){ //if second record is also positive,
                        //then there are no negative records
                            $('#rNegTitle').text("No records available");
                            $('#rNegText').text(" ");
                        }
                        else{ //if second record is negative, then that is the 1st negative post
                            $('#rNegTitle').text(parsed_resp[1]['fields']['rTitle']);
                            $('#rNegText').text(parsed_resp[1]['fields']['rText']);
                        }
                    }
                    else{ //if first record itself is negative,
                    //then that is the 1st negative post, and there are no positive records to show
                        $('#rPosTitle').text("No records available");
                        $('#rPosText').text(" ");
                        $('#rNegTitle').text(parsed_resp[0]['fields']['rTitle']);
                        $('#rNegText').text(parsed_resp[0]['fields']['rText']);
                    }
                }
                else if(parsed_resp.length == 1){ //if 1 record found
                    if(parseInt(parsed_resp[0]['fields']['rRating']) > 2){ //if record is positive,
                    //then there are no negative records to show (even pos post 2 will be empty)
                        $('#rPosTitle').text(parsed_resp[0]['fields']['rTitle']);
                        $('#rPosText').text(parsed_resp[0]['fields']['rTitle']);
                        $('#rNegTitle').text("No records available");
                        $('#rNegText').text(" ");
                    }
                    else{ // if record is negative, then that is the 1st negative post (even neg post 2 will be empty)
                    //also there are no positive records to show
                        $('#rPosTitle').text("No records available");
                        $('#rPosText').text(" ");
                        $('#rNegTitle').text(parsed_resp[0]['fields']['rTitle']);
                        $('#rNegText').text(parsed_resp[0]['fields']['rText']);
                    }
                }
                else{ //if no records retrieved
                    $('#rPosTitle').text("No records available");
                    $('#rPosText').text(" ");
                    $('#rNegTitle').text("No records available");
                    $('#rNegText').text(" ");
                }
           },
           failure: function (response) {
               alert("failed");
               $('#rPosTitle').text("Failed to retrieve data!");
                $('#rPosText').text("Please reload the page");
                $('#rNegTitle').text("Failed to retrieve data!");
                $('#rNegText').text("Please reload the page");
           }
        });
     }
}

//
//var onBrandChange = function(e) {
//    console.log(e);
//    load_source1();
//    load_count_cards();
//    load_all_charts();
//};
//
//var onSourceChange = function (e) {
//    console.log(e);
//    load_sku1();
//    load_count_cards();
//    load_all_charts();
//};
//
//var onSkuChange = function (e){
//    console.log(e);
//    load_count_cards();
//    load_all_charts();
//};



function load_brand1() {
   // console.log("Brand called");
   var data1 = "";
   $.ajax({
       type: "GET",
       url: "/service/summary_brand1/",
       data: { 'query': query },
       contentType: "application/json; charset=utf-8",
       dataType: "json",
       success: function (response) {
//           console.log(response)
//            $('#brand1 ul').off('change', onBrandChange);

           var $brand = $('#brand1 ul');
//           $("#Chart1select .selectpicker").selectpicker();
           $brand.find('#brand1 .list-items').remove();

           $.each(response, function (key, value) {
//           console.log("Key:", key)
//           console.log("Value:", value.pBrand)
               if (value.pBrand != null) {
//                   $('<li class="list-items selected"/>').appendTo($brand);
//                   var $li_el = $('#brand1 .list-items:last-of-type');
//                   $('<a/>').appendTo($li_el);
//                   var $li_a_el = $('#brand1 .list-items:last-of-type a');
//                   $('<span class="text"/>').val(value.pBrand).text(value.pBrand).appendTo($li_a_el);
//                   $('<span class="check-mark"/>').val("✔").text("✔").appendTo($li_a_el);
                    data1 = data1 + '"' + value.pBrand + '":"' + value.pBrand + '",' ;
               }
           });
            try{
            data1 = data1.replace(/.$/g,"}");
            data1 = data1.replace(/\n/g," ");
            data1 = "{" + data1;
            data1 = JSON.parse(data1);
//            console.log(data1);
             $('.multi').multi_select({
                //   selectColor: '#0077b5',
                  selectSize: 'small',
                  selectText: 'Select Brand',
                  duration: 300,
                  easing: 'slide',
                  listMaxHeight: 300,
                  selectedCount: 2,

//                  selectedValues:[{"Amazon":"Amazon","AmazonBasics":"AmazonBasics"}],
                  sortByText: true,
                  fillButton: true,
                  data: data1,
                  onSelect: function(values) {
                        //console.log("brand changed");

                            //console.log('return values: ', values);

//                        console.log('data1 length: ', Object.keys(data1).length);

//                        $('#brand1').multi_select({'selectText':data1.length});

                        reload_source1(values);
                        load_count_cards();
                        load_all_charts();

                  }
            });
            }catch(err){}
            var $span_el = $('#brand1 li a span.text');
//            console.log($span_el);
            $span_el.parent().parent().addClass('selected');
            $('#brand1 span.button-text').text("Selected (" + Object.keys(data1).length + ")");
            $('#brand1 li.control a').text('Deselect All');

//            $('#brand1').multi_select('getSelectedValues');
//            $('.multi').multi_select({'selectText':data1.length});

//          $('#brand1').selectpicker('refresh');
          //$("#Chart1select").selectpicker("refresh");
//          $('#brand1').selectpicker('selectAll');

          load_source1(data1);
//          $('#brand1').on('change', onBrandChange);
       },
       failure: function (response) {
           alert("failed");
       }
   });
}


function load_source1(data1) {
//    console.log($('#brand1').val());
//    var brand = JSON.stringify($('#brand1').val());
//    console.log(brand);
        var brand = Object.values(data1);
//        console.log(brand);
    var data2 = "";
    $.ajax({
       type: "GET",
       url: "/service/summary_source1/",
       data: { 'query': query , 'brand': JSON.stringify(brand) },
       contentType: "application/json; charset=utf-8",
       dataType: "json",
       success: function (response) {
//           $('#source1 ul').off('change', onSourceChange);

//           console.log(response);
           var $source = $('#source1 ul');
           $source.find('#source1 .list-items').remove();

           $.each(response, function (key, value) {
//           console.log("Key:", key);
//           console.log("Value:", value);

               if (value != null) {
                    data2 = data2 + '"' + value + '":"' + value + '",' ;

               }
           });
           try{
           data2 = data2.replace(/.$/g,"}");
            data2 = data2.replace(/\n/g," ");
            data2 = "{" + data2;
            data2 = JSON.parse(data2);
//            console.log(data2);

            $('.multi2').multi_select({
                //   selectColor: '#0077b5',
                  selectSize: 'small',
                  selectText: 'Select Source',
                  duration: 300,
                  easing: 'slide',
                  listMaxHeight: 300,
                  selectedCount: 2,
                  sortByText: true,
                  fillButton: true,
                  data: data2,
                  onSelect: function(values) {
//                    console.log('return values: ', values);
                        reload_sku1(data1, values);
                        load_count_cards();
                        load_all_charts();
                  }
              });
            }
            catch(err){}
            var $span_el = $('#source1 li a span.text');
//            console.log($span_el);
            $span_el.parent().parent().addClass('selected');
            $('#source1 span.button-text').text("Selected (" + Object.keys(data2).length + ")");
            $('#source1 li.control a').text('Deselect All');



//          $("#source1").selectpicker("refresh");
//          $('#source1').selectpicker('selectAll');

          load_sku1(data1, data2);
//          $('#source1').on('change', onSourceChange);

       },
       failure: function (response) {
           alert("failed");
       }
    });
}

function reload_source1(data1) {
//    console.log($('#brand1').val());
//    var brand = JSON.stringify($('#brand1').val());
//    console.log(brand);
        var brand = Object.values(data1);
        //console.log(brand);
    var data2 = "";
    $.ajax({
       type: "GET",
       url: "/service/summary_source1/",
       data: { 'query': query , 'brand': JSON.stringify(brand) },
       contentType: "application/json; charset=utf-8",
       dataType: "json",
       success: function (response) {
//           $('#source1 ul').off('change', onSourceChange);

//           console.log(response);
           var $source = $('#source1 ul');
           $source.find('#source1 .list-items').remove();

           $.each(response, function (key, value) {
//           console.log("Key:", key);
//           console.log("Value:", value);

               if (value != null) {
                    data2 = data2 + '"' + value + '":"' + value + '",' ;

               }
           });
           try{
           data2 = data2.replace(/.$/g,"}");
            data2 = data2.replace(/\n/g," ");
            data2 = "{" + data2;
            data2 = JSON.parse(data2);
//            console.log(data2);


            $('.multi2').multi_select({
                //   selectColor: '#0077b5',
                  selectSize: 'small',
                  selectText: 'Select Source',
                  duration: 300,
                  easing: 'slide',
                  listMaxHeight: 300,
                  selectedCount: 2,
                  sortByText: true,
                  fillButton: true,
                  data: data2,
                  onSelect: function(values) {
//                    console.log('return values: ', values);
                        reload_sku1(data1, values);
                        load_count_cards();
                        load_all_charts();
                  }
              });
              }catch(err){}
            var $span_el = $('#source1 li a span.text');
//            console.log($span_el);
            $span_el.parent().parent().addClass('selected');
            $('#source1 span.button-text').text("Selected (" + Object.keys(data2).length + ")");
            $('#source1 li.control a').text('Deselect All');



//          $("#source1").selectpicker("refresh");
//          $('#source1').selectpicker('selectAll');

          reload_sku1(data1, data2);
//          $('#source1').on('change', onSourceChange);

       },
       failure: function (response) {
           alert("failed");
       }
    });
}


function load_sku1(data1, data2) { //resp is source list in full name
    var brand = Object.values(data1);
//    console.log(brand);

    var source = Object.values(data2);
//    console.log(source);

    var data3 = "";

    $.ajax({
       type: "GET",
       url: "/service/summary_sku1/",
       data: { 'query': query , 'brand': JSON.stringify(brand), 'source': JSON.stringify(source)},
       //data: { 'query': query , 'brand': JSON.stringify($('#brand1').val()), 'source': JSON.stringify(source_vals)},
       contentType: "application/json; charset=utf-8",
       dataType: "json",
       success: function (response) {
//          $('#sku1').off('change', onSkuChange);
//           console.log(response);
           var $sku = $('#sku1 ul');
           $sku.find('#sku1 .list-items').remove();

           $.each(response, function (key, value) {
//           console.log("Key:", key)
//           console.log("Value:", value.pModel)
               if (value.pModel != null) {
                   data3 = data3 + '"' + value.pModel + '":"' + value.pModel + '",' ;
               }
           });
//           $("#sku1").selectpicker("refresh");
//           $('#sku1').selectpicker('selectAll');
            try{
            data3 = data3.replace(/.$/g,"}");
            data3 = data3.replace(/\n/g," ");
            data3 = "{" + data3;
            data3 = JSON.parse(data3);
//            console.log(data3);

            $('.multi3').multi_select({
                //   selectColor: '#0077b5',
                  selectSize: 'small',
                  selectText: 'Select SKU',
                  duration: 300,
                  easing: 'slide',
                  listMaxHeight: 300,
                  selectedCount: 2,
                  sortByText: true,
                  fillButton: true,
                  data: data3,
                  onSelect: function(values) {
//                    console.log('return values: ', values);
                        load_count_cards();
                        load_all_charts();
                  }
            });
            }catch(err){}
            var $span_el = $('#sku1 li a span.text');
//            console.log($span_el);
            $span_el.parent().parent().addClass('selected');
            $('#sku1 span.button-text').text("Selected (" + Object.keys(data3).length + ")");
            $('#sku1 li.control a').text('Deselect All');

           if(1){
                load_count_cards();
                load_all_charts();
           }
//           $('#sku1').on('change', onSkuChange);
       },
       failure: function (response) {
           alert("failed");
       }
    });
}

function reload_sku1(data1, data2) { //resp is source list in full name
    var brand = Object.values(data1);
//    console.log(brand);
    //console.log(data1, data2);
    var source = Object.values(data2);
//    console.log(source);

    var data3 = "";

    $.ajax({
       type: "GET",
       url: "/service/summary_sku1/",
       data: { 'query': query , 'brand': JSON.stringify(brand), 'source': JSON.stringify(source)},
       //data: { 'query': query , 'brand': JSON.stringify($('#brand1').val()), 'source': JSON.stringify(source_vals)},
       contentType: "application/json; charset=utf-8",
       dataType: "json",
       success: function (response) {
//          $('#sku1').off('change', onSkuChange);
//           console.log(response);
           var $sku = $('#sku1 ul');
           $sku.find('#sku1 .list-items').remove();

           $.each(response, function (key, value) {
//           console.log("Key:", key)
//           console.log("Value:", value.pModel)
               if (value.pModel != null) {
                   data3 = data3 + '"' + value.pModel + '":"' + value.pModel + '",' ;
               }
           });
//           $("#sku1").selectpicker("refresh");
//           $('#sku1').selectpicker('selectAll');
            try{
            data3 = data3.replace(/.$/g,"}");
            data3 = data3.replace(/\n/g," ");
            data3 = "{" + data3;
            data3 = JSON.parse(data3);

//            console.log(data3);

            $('.multi3').multi_select({
                //   selectColor: '#0077b5',
                  selectSize: 'small',
                  selectText: 'Select SKU',
                  duration: 300,
                  easing: 'slide',
                  listMaxHeight: 300,
                  selectedCount: 2,
                  sortByText: true,
                  fillButton: true,
                  data: data3,
                  onSelect: function(values) {
//                    console.log('return values: ', values);
                  }
            });
            }
            catch(err){}
            var $span_el = $('#sku1 li a span.text');
//            console.log($span_el);
            $span_el.parent().parent().addClass('selected');
            $('#sku1 span.button-text').text("Selected (" + Object.keys(data3).length + ")");
            $('#sku1 li.control a').text('Deselect All');

           if(1){
                load_count_cards();
                load_all_charts();
           }
//           $('#sku1').on('change', onSkuChange);
       },
       failure: function (response) {
           alert("failed");
       }
    });
}

function load_chart1() {

    if (flag1 == false){  //does not contain .csv

//        console.log(selStartDate,selEndDate);
        var brand = [];
        $('#brand1 .selected .text').each(function(index){
//            console.log($(this).text());
            brand.push($(this).text());
        });
//        console.log(brand);

        var source = [];
        $('#source1 .selected .text').each(function(index){
            source.push($(this).text());
        });
//        console.log(source);

        var sku = [];
        $('#sku1 .selected .text').each(function(index){
            sku.push($(this).text());
        });
//        console.log(sku);

        $.ajax({
           type: "GET",
           url: "/service/summary_chart1/",

           data: { 'query': query , 'brand': JSON.stringify(brand), 'source': JSON.stringify(source),
           'sku': JSON.stringify(sku), 'fromDate': JSON.stringify(selStartDate)
           , 'toDate': JSON.stringify(selEndDate) },

           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
               //console.log(response);
               $.each(response, function (key, value) {
    //           console.log("Key:", key)
    //           console.log("Value:", Date.UTC(parseInt(value[0].split('-'))))
               //value[0] = Date.UTC(parseInt(value[0].split('-')))
                //console.log(((value[0]).split('T'))[0])
                //console.log(Date.UTC(parseInt(((value[0]).split('T'))[0])))
               });
               //console.log(data1)
                   Highcharts.chart('reviewcountChart', {
                        chart: {
                            zoomType: 'x',
                            style: {
                                fontFamily: 'Arial'
                            },
                            spacingLeft:5,
                            spacingRight:5
                        },

                        title: {
                            text: 'Review Frequency over Time'
                        },
                        subtitle: {
                            text: document.ontouchstart === undefined ?
                                    'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                        },
                        xAxis: {
                            type: 'datetime'
                        },
                        yAxis: {
                            title: {
                                text: 'Frequency'
                            }
                        },
                        legend: {
                            enabled: false
                        },

                        plotOptions: {
                            area: {
                                fillColor: {
                                    linearGradient: {
                                        x1: 0,
                                        y1: 0,
                                        x2: 0,
                                        y2: 1
                                    },
                                    stops: [
                                        [0, Highcharts.getOptions().colors[0]],
                                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                                    ]
                                },
                                marker: {
                                    radius: 2
                                },
                                lineWidth: 1,
                                states: {
                                    hover: {
                                        lineWidth: 1
                                    }
                                },
                                threshold: null
                            }
                        },

                        series: [{
                            type: 'area',
                            name: 'Count',
                            data: response
                        }]
                    });

               //console.log(response)
           },
           failure: function (response) {
               alert("failed");
           }
        });
     }
     else{  // if flag1 is true
         $.ajax({
           type: "GET",
           url: "/service/summary_common_reviewcount_chart/",

           data: { 'query': query },

           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
               //console.log(response)
               $.each(response, function (key, value) {
    //           console.log("Key:", key)
    //           console.log("Value:", Date.UTC(parseInt(value[0].split('-'))))
               //value[0] = Date.UTC(parseInt(value[0].split('-')))
                //console.log(((value[0]).split('T'))[0])
                //console.log(Date.UTC(parseInt(((value[0]).split('T'))[0])))
               });
               //console.log(data1)
                   Highcharts.chart('reviewcountChart', {
                        chart: {
                            zoomType: 'x',
                            style: {
                                fontFamily: 'Arial'
                            }
                        },
                        title: {
                            text: 'Overall Review Frequency over Time'
                        },
                        subtitle: {
                            text: document.ontouchstart === undefined ?
                                    'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                        },
                        xAxis: {
                            type: 'datetime'
                        },
                        yAxis: {
                            title: {
                                text: 'Frequency'
                            }
                        },
                        legend: {
                            enabled: false
                        },

                        plotOptions: {
                            area: {
                                fillColor: {
                                    linearGradient: {
                                        x1: 0,
                                        y1: 0,
                                        x2: 0,
                                        y2: 1
                                    },
                                    stops: [
                                        [0, Highcharts.getOptions().colors[0]],
                                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                                    ]
                                },
                                marker: {
                                    radius: 2
                                },
                                lineWidth: 1,
                                states: {
                                    hover: {
                                        lineWidth: 1
                                    }
                                },
                                threshold: null
                            }
                        },

                        series: [{
                            type: 'area',
                            name: 'Count',
                            data: response
                        }]
                    });

               //console.log(response)
           },
           failure: function (response) {
               alert("failed");
           }
        });
     }
}


function load_logos(resp)
{
    //console.log("inside load_logos()");
    //console.log(resp);
    var column = [];
   for(var i=0; i<resp.length; i++){
      column.push(resp[i]['name']);
   }
   $("#piechartDiv > div:first").empty();
    var new_div_row = document.createElement("div");
    new_div_row.classList.add("row") ;
    for (c=0; c<column.length; c++){
        //console.log(column.length);
        var new_div = document.createElement("div");
         switch(column.length){
            case 3:
                new_div.className = "col-lg-4";
                break;
            case 2:
                new_div.className = "col-lg-6";
                break;
            case 1:
            default:
                break;
            }

        new_div.height="100%" ;

        var div_para1 = document.createElement("p");

        var para1_anchor = document.createElement("a");
        para1_anchor.target = "_blank";

        var anchor_logo = document.createElement("img");
//        anchor_logo.src = "/static/atlas/images/icons/" + column[c].toString().toLowerCase() + "_logo.png";
        anchor_logo.src = "/static/atlas/images/icons/" + column[c].toString().toLowerCase() + "_logo.png";

        anchor_logo.alt = column[c];


        if(column[c].toString().toLowerCase() == "homedepot"){
            para1_anchor.href = "https://www." + column[c].toString().toLowerCase() + ".com/s/" + query;
        }
        else if(column[c].toString().toLowerCase() == "walmart") {
            para1_anchor.href = "https://www." + column[c].toString().toLowerCase() + ".com/search/?query=" + query;
        }
        else if(column[c].toString().toLowerCase() == "amazon") {
            para1_anchor.href = "https://www." + column[c].toString().toLowerCase() + ".com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=" + query;
        }
        para1_anchor.append(anchor_logo);

        var anchor_span = document.createElement("span");
        anchor_span.innerHTML = "<b>" + column[c] + "</b>";
        para1_anchor.append(anchor_span);

        div_para1.append(para1_anchor);

        new_div.append(div_para1);

        new_div_row.append(new_div);
    }

    $("#piechartDiv > div:first").append(new_div_row);
}

function load_pie_chart(){
    if(flag1 == false){
        //console.log("inside piechart");
        $('#piechartDivContainer').removeClass('hidden');

//        console.log(selStartDate,selEndDate);
        var brand = [];
        $('#brand1 .selected .text').each(function(index){
//            console.log($(this).text());
            brand.push($(this).text());
        });
//        console.log(brand);

        var source = [];
        $('#source1 .selected .text').each(function(index){
            source.push($(this).text());
        });
//        console.log(source);

        var sku = [];
        $('#sku1 .selected .text').each(function(index){
            sku.push($(this).text());
        });
//        console.log(sku);

        $.ajax({
           type: "GET",
           url: "/service/summary_piechart/",

           data: { 'query': query , 'brand': JSON.stringify(brand), 'source': JSON.stringify(source),
               'sku': JSON.stringify(sku), 'fromDate': JSON.stringify(selStartDate), 'toDate': JSON.stringify(selEndDate) },
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
           //console.log(response);
           load_logos(response);

            // Make monochrome colors
            var pieColors = (function () {
                var colors = [],
                    base = Highcharts.getOptions().colors[0],
                    i;

                for (i = 0; i < 10; i += 1) {
                    // Start out with a darkened base color (negative brighten), and end
                    // up with a much brighter color
                    colors.push(Highcharts.Color(base).brighten((i - 3) / 7).get());
                }
                return colors;
            }());

            Highcharts.chart('myPieChart', {
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie',
                    style: {
                         fontFamily: 'Arial'
                    }
                },
                title: {
                    text: 'Reviews By Platform'
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
//                legend: {
//                      enabled: true
//                  },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        colors: pieColors,
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b><br>{point.percentage:.1f} %',
                        }
                    }
                },
                series: [{
                    name: 'Platform',
                    data: response
                }]
            });

           },
           failure: function (response) {
               alert("failed");
           }
        });
    }
    else{
        $('#piechartDivContainer').addClass('hidden');
    }
}

    function load_pos_posts(){
        if(query.indexOf(".csv") == -1){  //if ".csv" not present in kw
//            console.log(selStartDate,selEndDate);
            var brand = [];
            $('#brand1 .selected .text').each(function(index){
    //            console.log($(this).text());
                brand.push($(this).text());
            });
//            console.log(brand);

            var source = [];
            $('#source1 .selected .text').each(function(index){
                source.push($(this).text());
            });
//            console.log(source);

            var sku = [];
            $('#sku1 .selected .text').each(function(index){
                sku.push($(this).text());
            });
//            console.log(sku);


            $.ajax({
               type: "GET",
               url: "/service/summary_toppos_posts/",
               data: { 'query': query , 'brand': JSON.stringify(brand), 'source': JSON.stringify(source),
               'sku': JSON.stringify(sku), 'fromDate': JSON.stringify(selStartDate), 'toDate': JSON.stringify(selEndDate),
               'topn': JSON.stringify($("#pos_posts").val()) },
               contentType: "application/json; charset=utf-8",
               dataType: "json",
               success: function (response) {
                    //standard response includes a set of 2 positive records.
                    parsed_resp = JSON.parse(response);
                    //console.log("this is top pos posts");
                    $('#toppos').empty();
                    //top_pos_neg_resp = parsed_resp;
                    //to populate default positive post 1 and negative post 1
                    if (parsed_resp.length > 0){
                        for(i = 0; i<parsed_resp.length; i++){
                            //console.log(i);
                            var new_item_div = document.createElement("div");
                            new_item_div.className = "list-group-item";
                            new_item_div.style = "color:dimgrey;";

                            var new_item_head = document.createElement("h5");
                            new_item_head.className = "list-group-item-heading";
                            new_item_head.style = "font-weight:bold;";
                            new_item_head.innerHTML = parsed_resp[i]['fields']['rTitle']

                            var new_item_text = document.createElement("p");
                            new_item_text.className = "list-group-item-text";
                            new_item_text.innerHTML = parsed_resp[i]['fields']['rText']

                            new_item_div.append(new_item_head);
                            new_item_div.append(new_item_text);

                            $('#toppos').append(new_item_div);
                        }
                    }
                    else{ //if no records retrieved
                        var new_item_div = document.createElement("div");
                        new_item_div.className = "list-group-item";
                        new_item_div.style = "color:dimgrey;";

                        var new_item_head = document.createElement("h5");
                        new_item_head.className = "list-group-item-heading";
                        new_item_head.style = "font-weight:bold;";
                        new_item_head.value = "No records found!";

                        new_item_div.append(new_item_head);
                        $('#toppos').append(new_item_div);
                    }
               },
               failure: function (response) {
                    var new_item_div = document.createElement("div");
                    new_item_div.className = "list-group-item";
                    new_item_div.style = "color:dimgrey;";

                    var new_item_head = document.createElement("h5");
                    new_item_head.className = "list-group-item-heading";
                    new_item_head.style = "font-weight:bold;";
                    new_item_head.value = "No records found!";

                    new_item_div.append(new_item_head);
                    $('#toppos').append(new_item_div);
               }
            });
        }
        else{
            $.ajax({
               type: "GET",
               url: "/service/summary_topposposts_overall/",

               data: { 'query': query, 'topn': JSON.stringify($("#pos_posts").val()) },

               contentType: "application/json; charset=utf-8",
               dataType: "json",
               success: function (response) {
                    //standard response includes a set of 2 positive records.
                    parsed_resp = JSON.parse(response);
                    //("this is top pos posts");
                    $('#toppos').empty();
                    //top_pos_neg_resp = parsed_resp;
                    //to populate default positive post 1 and negative post 1
                    if (parsed_resp.length > 0){
                        for(i = 0; i<parsed_resp.length; i++){
                            //console.log(i);
                            var new_item_div = document.createElement("div");
                            new_item_div.className = "list-group-item";
                            new_item_div.style = "color:dimgrey;";

                            var new_item_head = document.createElement("h5");
                            new_item_head.className = "list-group-item-heading";
                            new_item_head.style = "font-weight:bold;";
                            if((parsed_resp[i]['fields']['rTitle']).toString() == 'nan'){
                                new_item_head.innerHTML = "";
                            }
                            else{
                                new_item_head.innerHTML = parsed_resp[i]['fields']['rTitle'];
                            }

                            var new_item_text = document.createElement("p");
                            new_item_text.className = "list-group-item-text";
                            new_item_text.innerHTML = parsed_resp[i]['fields']['rText']

                            new_item_div.append(new_item_head);
                            new_item_div.append(new_item_text);

                            $('#toppos').append(new_item_div);
                        }
                    }
                    else{ //if no records retrieved
                        var new_item_div = document.createElement("div");
                        new_item_div.className = "list-group-item";
                        new_item_div.style = "color:dimgrey;";

                        var new_item_head = document.createElement("h5");
                        new_item_head.className = "list-group-item-heading";
                        new_item_head.style = "font-weight:bold;";
                        new_item_head.value = "No records found!";

                        new_item_div.append(new_item_head);
                        $('#toppos').append(new_item_div);
                    }
               },
               failure: function (response) {
                    var new_item_div = document.createElement("div");
                    new_item_div.className = "list-group-item";
                    new_item_div.style = "color:dimgrey;";

                    var new_item_head = document.createElement("h5");
                    new_item_head.className = "list-group-item-heading";
                    new_item_head.style = "font-weight:bold;";
                    new_item_head.value = "No records found!";

                    new_item_div.append(new_item_head);
                    $('#toppos').append(new_item_div);
               }
            });
        }
    }

    function load_neg_posts(){
        if(query.indexOf(".csv") == -1){
//            console.log(selStartDate,selEndDate);
            var brand = [];
            $('#brand1 .selected .text').each(function(index){
    //            console.log($(this).text());
                brand.push($(this).text());
            });
//            console.log(brand);

            var source = [];
            $('#source1 .selected .text').each(function(index){
                source.push($(this).text());
            });
//            console.log(source);

            var sku = [];
            $('#sku1 .selected .text').each(function(index){
                sku.push($(this).text());
            });
//            console.log(sku);

            $.ajax({
               type: "GET",
               url: "/service/summary_topneg_posts/",

               data: { 'query': query , 'brand': JSON.stringify(brand), 'source': JSON.stringify(source),
               'sku': JSON.stringify(sku), 'fromDate': JSON.stringify(selStartDate), 'toDate': JSON.stringify(selEndDate),
               'topn': JSON.stringify($("#neg_posts").val()) },

               contentType: "application/json; charset=utf-8",
               dataType: "json",
               success: function (response) {
                    //standard response includes a set of 2 positive records.
                    parsed_resp = JSON.parse(response);
                    //console.log("this is top pos posts");
                    $('#topneg').empty();
                    //top_pos_neg_resp = parsed_resp;
                    //to populate default positive post 1 and negative post 1
                    if (parsed_resp.length > 0){
                        for(i = 0; i<parsed_resp.length; i++){
    //                        console.log(i);
                            var new_item_div = document.createElement("div");
                            new_item_div.className = "list-group-item";
                            new_item_div.style = "color:dimgrey;";

                            var new_item_head = document.createElement("h5");
                            new_item_head.className = "list-group-item-heading";
                            new_item_head.style = "font-weight:bold;";
                            if((parsed_resp[i]['fields']['rTitle']).toString == 'nan'){
                                new_item_head.innerHTML = "";
                            }
                            else{
                                new_item_head.innerHTML = parsed_resp[i]['fields']['rTitle'];
                            }

                            var new_item_text = document.createElement("p");
                            new_item_text.className = "list-group-item-text";
                            new_item_text.innerHTML = parsed_resp[i]['fields']['rText']

                            new_item_div.append(new_item_head);
                            new_item_div.append(new_item_text);

                            $('#topneg').append(new_item_div);
                        }
                    }
                    else{ //if no records retrieved
                        var new_item_div = document.createElement("div");
                        new_item_div.className = "list-group-item";
                        new_item_div.style = "color:dimgrey;";

                        var new_item_head = document.createElement("h5");
                        new_item_head.className = "list-group-item-heading";
                        new_item_head.style = "font-weight:bold;";
                        new_item_head.value = "No records found!";

                        new_item_div.append(new_item_head);
                        $('#topneg').append(new_item_div);
                    }
               },
               failure: function (response) {
                    var new_item_div = document.createElement("div");
                    new_item_div.className = "list-group-item";
                    new_item_div.style = "color:dimgrey;";

                    var new_item_head = document.createElement("h5");
                    new_item_head.className = "list-group-item-heading";
                    new_item_head.style = "font-weight:bold;";
                    new_item_head.value = "No records found!";

                    new_item_div.append(new_item_head);
                    $('#topneg').append(new_item_div);
               }
            });
         }
         else{
            $.ajax({
               type: "GET",
               url: "/service/summary_topnegposts_overall/",

               data: { 'query': query, 'topn': JSON.stringify($("#neg_posts").val()) },

               contentType: "application/json; charset=utf-8",
               dataType: "json",
               success: function (response) {
                    //standard response includes a set of 2 positive records.
                    parsed_resp = JSON.parse(response);
                    //console.log("this is top pos posts");
                    $('#topneg').empty();
                    //top_pos_neg_resp = parsed_resp;
                    //to populate default positive post 1 and negative post 1
                    if (parsed_resp.length > 0){
                        for(i = 0; i<parsed_resp.length; i++){
    //                        console.log(i);
                            var new_item_div = document.createElement("div");
                            new_item_div.className = "list-group-item";
                            new_item_div.style = "color:dimgrey;";

                            var new_item_head = document.createElement("h5");
                            new_item_head.className = "list-group-item-heading";
                            new_item_head.style = "font-weight:bold;";
                            new_item_head.innerHTML = parsed_resp[i]['fields']['rTitle']

                            var new_item_text = document.createElement("p");
                            new_item_text.className = "list-group-item-text";
                            new_item_text.innerHTML = parsed_resp[i]['fields']['rText']

                            new_item_div.append(new_item_head);
                            new_item_div.append(new_item_text);

                            $('#topneg').append(new_item_div);
                        }
                    }
                    else{ //if no records retrieved
                        var new_item_div = document.createElement("div");
                        new_item_div.className = "list-group-item";
                        new_item_div.style = "color:dimgrey;";

                        var new_item_head = document.createElement("h5");
                        new_item_head.className = "list-group-item-heading";
                        new_item_head.style = "font-weight:bold;";
                        new_item_head.value = "No records found!";

                        new_item_div.append(new_item_head);
                        $('#topneg').append(new_item_div);
                    }
               },
               failure: function (response) {
                    var new_item_div = document.createElement("div");
                    new_item_div.className = "list-group-item";
                    new_item_div.style = "color:dimgrey;";

                    var new_item_head = document.createElement("h5");
                    new_item_head.className = "list-group-item-heading";
                    new_item_head.style = "font-weight:bold;";
                    new_item_head.value = "No records found!";

                    new_item_div.append(new_item_head);
                    $('#topneg').append(new_item_div);
               }
            });
         }
    }

$("#pospost1").click(function(){  //for populating positive post 1
        if(top_pos_neg_resp){
            //if 4 records found, then first record is 1st positive,
            if((top_pos_neg_resp.length == 4) ||

                //if 3 records found, then its implied that first record is 1st positive
                ( (top_pos_neg_resp.length == 3) &&
                    (parseInt(top_pos_neg_resp[0]['fields']['rRating']) > 2) ) ||

                    //if 2 records found, only if first record's rating is high , then its 1st positive
                ( (top_pos_neg_resp.length == 2) &&
                    (parseInt(top_pos_neg_resp[0]['fields']['rRating']) > 2) ) ||

                //if only 1 record found and its rating is high, then it is 1st positive
                ( (top_pos_neg_resp.length == 1) &&
                    (parseInt(top_pos_neg_resp[0]['fields']['rRating']) > 2) )
                    ){

                $('#rPosTitle').text(top_pos_neg_resp[0]['fields']['rTitle']);
                $('#rPosText').text(top_pos_neg_resp[0]['fields']['rText']);
            }

            else{  //for any other condition
                $('#rPosTitle').text("No records available");
                $('#rPosText').text("No records available");
            }
        }
        else{  //if no records found
            $('#rPosTitle').text("No records available");
            $('#rPosText').text("No records available");
        }
    });

$("#pospost2").click(function(){//for populating positive post 2, (only if 2 positive records are there)
        if(top_pos_neg_resp){
            //if 4 records found, then second record is 2nd positive,
            if((top_pos_neg_resp.length == 4) ||

                //if 3 records found, then its implied that first record is 1st positive,
                  //but only if second record's rating is high, then second record is 2nd positive (and third record is negative)
                ( ( (top_pos_neg_resp.length == 3) || (top_pos_neg_resp.length == 2) ) &&
                    (parseInt(top_pos_neg_resp[0]['fields']['rRating']) > 2) &&
                    (parseInt(top_pos_neg_resp[1]['fields']['rRating']) > 2) )

                    //if 2 records found, only if both  record's rating is high , then second record is 2nd positive
               ){

                $('#rPosTitle').text(top_pos_neg_resp[1]['fields']['rTitle']);
                $('#rPosText').text(top_pos_neg_resp[1]['fields']['rText']);
            }

            else{  //for any other condition
                $('#rPosTitle').text("No records available");
                $('#rPosText').text("No records available");
            }
        }
        else{  //if no records found
            $('#rPosTitle').text("No records available");
            $('#rPosText').text("No records available");
        }
    });

$("#negpost1").click(function(){  // for populating negative post 1
        if(top_pos_neg_resp){
            //if 4 records found, then third record is 1st negative,
            if(top_pos_neg_resp.length == 4){
                $('#rNegTitle').text(top_pos_neg_resp[2]['fields']['rTitle']);
                $('#rNegText').text(top_pos_neg_resp[2]['fields']['rText']);
            }

            //if 3 or 2 records found, then its implied that first record is 1st positive anyway,
              //but only if second record's rating is low, then second record is 1st positive
           else if ( ( (top_pos_neg_resp.length == 3) || (top_pos_neg_resp.length == 2) ) &&
                (parseInt(top_pos_neg_resp[1]['fields']['rRating']) <= 2) ){
                    $('#rNegTitle').text(top_pos_neg_resp[1]['fields']['rTitle']);
                    $('#rNegText').text(top_pos_neg_resp[1]['fields']['rText']);
                }

            //if 2 or 1 record(s) found, only if either  record's rating is low , then that record is 1st negative
            else if ( ( (top_pos_neg_resp.length == 2) || (top_pos_neg_resp.length == 1) ) &&
                        (parseInt(top_pos_neg_resp[0]['fields']['rRating']) <= 2) )  {

                    $('#rNegTitle').text(top_pos_neg_resp[0]['fields']['rTitle']);
                    $('#rNegText').text(top_pos_neg_resp[0]['fields']['rText']);
                }
            else{  //for any other condition
                $('#rNegTitle').text("No records available");
                $('#rNegText').text("No records available");
            }
        }
        else{  //if no records found
            $('#rNegTitle').text("No records available");
            $('#rNegText').text("No records available");
        }
    });

$("#negpost2").click(function(){
        if(top_pos_neg_resp){
            // if 4 records found, then 4th record is 2nd negative
            if(top_pos_neg_resp.length == 4){
                $('#rNegTitle').text(top_pos_neg_resp[3]['fields']['rTitle']);
                $('#rNegText').text(top_pos_neg_resp[3]['fields']['rText']);
            }
            //if 3 records found, 1st record is anyway 1st positive
            //but only if second record is 1st negative, the third record will be 2nd negative
            else if( (top_pos_neg_resp.length == 3) &&
                        ( (parseInt(top_pos_neg_resp[1]['fields']['rRating']) <= 2) &&
                        (parseInt(top_pos_neg_resp[2]['fields']['rRating']) <= 2) ) ){
                $('#rNegTitle').text(top_pos_neg_resp[2]['fields']['rTitle']);
                $('#rNegText').text(top_pos_neg_resp[2]['fields']['rText']);
            }
            //if 2 records found, only if both records are negative, second record will be the 2nd negative
            else if( (top_pos_neg_resp.length == 2) &&
                        ( (parseInt(top_pos_neg_resp[0]['fields']['rRating']) <= 2) &&
                        (parseInt(top_pos_neg_resp[1]['fields']['rRating']) <= 2) ) ){
                $('#rNegTitle').text(top_pos_neg_resp[1]['fields']['rTitle']);
                $('#rNegText').text(top_pos_neg_resp[1]['fields']['rText']);
            }
            else {//for any other condition
                $('#rNegTitle').text("No records available");
                $('#rNegText').text("No records available");
            }
        }
        else{ //if no records found
            $('#rNegTitle').text("No records available");
            $('#rNegText').text("No records available");
        }

    });

//
// $('#source1').on('change', function(e){
//     console.log(e);
//     //console.log(brand,source,sku); //You get the multiple values selected in your array
//     load_sku1();
//
// });
// $('#sku1').on('change', function(e){
//     console.log(e);
//     var selected = [];
//     brand = $('#brand1').val();
//     source = $('#source1').val();
//     sku = $('#sku1').val();
//     load_chart1();
//     load_chart2();
//     load_chart3();
//
// });


$('input[name="daterange"]').daterangepicker({
    opens: 'left'
}, function (start, end, label) {
    //console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
    selStartDate = start.format('YYYY-MM-DD');
    selEndDate = end.format('YYYY-MM-DD');
    //console.log(selStartDate, selEndDate);
    load_count_cards();
    load_all_charts();
});


$.get('/service/request/').then(function (successResponse) {

}, function (errorResponse) {

        console.log("errorResponse", errorResponse)
});


function load_brandsummary_chart(){
//        console.log(selStartDate,selEndDate);
        var brand = [];
        $('#brand1 .selected .text').each(function(index){
//            //console.log($(this).text());
            brand.push($(this).text());
        });
//        console.log(brand);

        var source = [];
        $('#source1 .selected .text').each(function(index){
            source.push($(this).text());
        });
//        console.log(source);

        var sku = [];
        $('#sku1 .selected .text').each(function(index){
            sku.push($(this).text());
        });
//        console.log(sku);

        $.ajax({
           type: "GET",
           url: "/service/analysis_brandsummary_chart/",
           data: { 'query': query , 'brand': JSON.stringify(brand), 'source': JSON.stringify(source),
               'sku': JSON.stringify(sku), 'fromDate': JSON.stringify(selStartDate)
               , 'toDate': JSON.stringify(selEndDate) },       contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
                //               console.log(response['response1'])
                //console.log("brand summary response");
                //console.log(response);
               Highcharts.chart('brandsummaryChart', {
                    chart: {
                        type: 'column',
                        style: {
                                fontFamily: 'Arial'
                            }
                    },
                    title: {
                        text: 'Average Rating by Brand'
                    },
                    subtitle: {
                        text: 'Click the columns to view SKU level data. '
                    },
                    xAxis: {
                        type: 'category'
                    },
                    yAxis: {
                        title: {
                            text: 'Average Rating'
                        }
                    },
                    legend: {
                        enabled: false
                    },
                    plotOptions: {
                        series: {
                            borderWidth: 0,
                            dataLabels: {
                                enabled: true,
                                format: '{point.y:.1f}'
                            }
                        }
                    },

                    tooltip: {
                        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}'
                    },
                    series: [{
                            name: 'Brands',
                            colorByPoint: true,
                            data : response['response1']
                    }],

                    drilldown: response['dict2']
                });

           },
           failure: function (response) {
               alert("failed");
           }
        });
}


function load_senti_charts()
    {
        if(flag1 == true) { //if query contains '.csv'
            $('#linechartDiv').addClass('d-none');
            load_common_senti_chart();
        }
        else
        {
            $('#linechartDiv').removeClass('d-none');
            load_chart11();
            load_chart22();
        }
    }

function load_common_senti_chart(){
//        console.log("Loading common sentiment chart");

        $.ajax({
           type: "GET",
           url: "/service/analysis_common_senti_chart/",
           data: { 'query': query },
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
//               console.log(response);

            Highcharts.chart('bar-chart', {
                chart: {
                    type: 'bar',
                    style: {
                                fontFamily: 'Arial'
                            }
                },
                title: {
                    text: 'Overall Sentiments'
                },
                xAxis: {
                    categories: ['Positive', 'Negative', 'Neutral']
                },
                yAxis: {
                    title: {
                        text: ''
                    },
                    labels: {
                        overflow: 'justify'
                    }
                },
                 plotOptions: {
                    series: {
                        colorByPoint: true
                    }
                },
                credits: {
                    enabled: true
                },
                legend: {
                    enabled: false
                },
                series: response
            });

       },
       failure: function (response) {
           alert("failed");
       }
    });
    }

function load_chart11() {

//        console.log(selStartDate,selEndDate);
        var brand = [];
        $('#brand1 .selected .text').each(function(index){
//            console.log($(this).text());
            brand.push($(this).text());
        });
//        console.log(brand);

        var source = [];
        $('#source1 .selected .text').each(function(index){
            source.push($(this).text());
        });
//        console.log(source);

        var sku = [];
        $('#sku1 .selected .text').each(function(index){
            sku.push($(this).text());
        });
//        console.log(sku);

        $.ajax({
           type: "GET",
           url: "/service/analysis_chart1/",
           data: { 'query': query , 'brand': JSON.stringify(brand), 'source': JSON.stringify(source),
           'sku': JSON.stringify(sku), 'fromDate': JSON.stringify(selStartDate), 'toDate': JSON.stringify(selEndDate)},
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
               //console.log(response);

                Highcharts.chart('line-chart', {
                    chart: {
                        type: 'column',
                        style: {
                                fontFamily: 'Arial'
                            }
                    },
                    title: {
                        text: ' Overall Sentiments by Brand'
                    },
                    subtitle: {
                        text: 'Click the columns for sentiments at SKU level'
                    },
                    xAxis: {
                        type: 'category'
                    },
                    yAxis: {
                        title: {
                            text: 'Brand Positivity (%)'
                        }
                    },
                    legend: {
                        enabled: false
                    },
                    plotOptions: {
                        series: {
                            //borderWidth: 0,
                            dataLabels: {
                                enabled: true,
                                format: '{point.y:.1f}'
                            }
                        }
                    },

                    tooltip: {
                        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b><br/>'
                    },

                    series: [{
                        name: 'Brands',
                        colorByPoint: true,
                        data: response[0]
                    }],
                    drilldown: {
                        series: response[1]
                    }
                });
              //console.log(response);
       },
       failure: function (response) {
           alert("failed");
       }
    });
}


function load_chart22() {

//         console.log(selStartDate,selEndDate);
        var brand = [];
        $('#brand1 .selected .text').each(function(index){
//            console.log($(this).text());
            brand.push($(this).text());
        });
//        console.log(brand);

        var source = [];
        $('#source1 .selected .text').each(function(index){
            source.push($(this).text());
        });
//        console.log(source);

        var sku = [];
        $('#sku1 .selected .text').each(function(index){
            sku.push($(this).text());
        });
//        console.log(sku);


        $.ajax({
           type: "GET",
           url: "/service/analysis_chart2/",
           data: { 'query': query , 'brand': JSON.stringify(brand), 'source': JSON.stringify(source),
           'sku': JSON.stringify(sku), 'fromDate': JSON.stringify(selStartDate), 'toDate': JSON.stringify(selEndDate)},
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
               //console.log(response);

            Highcharts.chart('bar-chart', {
                chart: {
                    type: 'bar',
                    style: {
                                fontFamily: 'Arial'
                            }
                },
                title: {
                    text: 'Overall Sentiments by Source'
                },
                xAxis: {
                    categories: ['Positive', 'Negative', 'Neutral']
                },
                yAxis: {
                    title: {
                        text: ''
                    },
                    labels: {
                        overflow: 'justify'
                    }
                },
                credits: {
                    enabled: true
                },
                legend: {
                    enabled: true
                },
                series: response
            });
           //console.log(response);
       },
       failure: function (response) {
           alert("failed");
       }
    });
}

function load_trigdriv_charts()
    {
            load_chart44();
    }

function load_chart44() {
    if(flag1 == false){  //if '.csv' NOT present in query string

//          console.log(selStartDate,selEndDate);
        var brand = [];
        $('#brand1 .selected .text').each(function(index){
//            console.log($(this).text());
            brand.push($(this).text());
        });
//        console.log(brand);

        var source = [];
        $('#source1 .selected .text').each(function(index){
            source.push($(this).text());
        });
//        console.log(source);

        var sku = [];
        $('#sku1 .selected .text').each(function(index){
            sku.push($(this).text());
        });
//        console.log(sku);

        $.ajax({
           type: "GET",
           url: "/service/analysis_chart4/",
           data: { 'query': query , 'brand': JSON.stringify(brand), 'source': JSON.stringify(source),
           'sku': JSON.stringify(sku), 'fromDate': JSON.stringify(selStartDate), 'toDate': JSON.stringify(selEndDate)},
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
               //console.log(response[1].toString());

               var data1 = response[0];

                var data2 = response[1];

                Highcharts.chart('donut-chart2', {
                       credits: {
                            enabled: true
                        },
                        chart: {
                            type: 'pie',
                            style: {
                                fontFamily: 'Arial'
                            }
                        },
                        title: {
                            text: 'Drivers of Purchase',
                            //style: { fontSize: '12px' },
                        },
                        subtitle: {
                        text: 'Click the highlighted labels to view sub-drivers '
                    },
                        plotOptions: {
                            pie:{
                                dataLabels: {
                                    enabled: true,
                                    format: '<b>{point.name}</b><br>{point.percentage:.1f} %'
                                },
                                showInLegend: false
                            }
                        },
                        tooltip: {
                            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.1f}%</b> <br/>'
                        },
                        series: [{
                            name: 'Drivers',
                            colorByPoint: true,
                            data: data1
                        }],
                        drilldown: {
                            series: data2
                        }
                    });

               //console.log(response)
           },
           failure: function (response) {
               alert("failed");
           }
        });
    }
    else{  // if '.csv' present in query string
        $.ajax({
           type: "GET",
           url: "/service/analysis_common_driv_chart/",
           data: { 'query': query },
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
               //console.log(response[1].toString());

               var data1 = response[0];
               var data2 = response[1];

                Highcharts.chart('donut-chart2', {
                       credits: {
                            enabled: true
                        },
                        chart: {
                            type: 'pie',
                            style: {
                                fontFamily: 'Arial'
                            }
                        },
                        title: {
                            text: 'Drivers of Purchase',
                            //style: { fontSize: '12px' },
                        },
                        subtitle: {
                        text: 'Click the highlighted labels to view subdrivers '
                    },
                        plotOptions: {
                            pie:{
                                dataLabels: {
                                    enabled: true,
                                    format: '<b>{point.name}</b><br>{point.percentage:.1f} %'
                                },
                                showInLegend: false
                            }
                        },
                        tooltip: {
                            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.1f}%</b> <br/>'
                        },
                        series: [{
                            name: 'Drivers',
                            colorByPoint: true,
                            data: data1
                        }],
                        drilldown: {
                            series: data2
                        }
                    });

               //console.log(response)
           },
           failure: function (response) {
               alert("failed");
           }
        });
    }
}


function load_categ_chart() {
    if(flag1 == false){  //if '.csv' NOT present in query string

//          console.log(selStartDate,selEndDate);
        var brand = [];
        $('#brand1 .selected .text').each(function(index){
//            console.log($(this).text());
            brand.push($(this).text());
        });
//        console.log(brand);

        var source = [];
        $('#source1 .selected .text').each(function(index){
            source.push($(this).text());
        });
//        console.log(source);

        var sku = [];
        $('#sku1 .selected .text').each(function(index){
            sku.push($(this).text());
        });
//        console.log(sku);

        $.ajax({
           type: "GET",
           url: "/service/summary_categchart_rev/",
           data: { 'query': query , 'brand': JSON.stringify(brand), 'source': JSON.stringify(source),
           'sku': JSON.stringify(sku), 'fromDate': JSON.stringify(selStartDate), 'toDate': JSON.stringify(selEndDate)},
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
//               console.log(JSON.stringify(response[0]));
//               console.log(JSON.stringify(response[1]));

               // Create the chart
                Highcharts.chart('categDonutChart', {
                    chart: {
                        type: 'pie',
                        style: {
                                fontFamily: 'Arial'
                            }
                    },
                    title: {
                        text: 'Content Categories Distribution'
                    },
                    subtitle: {
                        text: 'Drill down to see secondary and tertiary categories'
                    },
                    plotOptions: {
                        series: {
                            dataLabels: {
                                enabled: true,
                                format: '{point.name}: {point.y:.1f}%'
                            }
                        }
                    },
                    tooltip: {
                        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
                    },
                    // response = [seriesData, drilldownData]
                    "series":
                    [
                        {
                            "name": "Primary Categories",
                            "colorByPoint": true,
                            "data": response[0] //[
//                                {
//                                    "name": "/Arts & Entertainment",
//                                    "y": 62.74,
//                                    "drilldown": "arts"
//                                },
//                                {
//                                    "name": "/Computers & Electronics",
//                                    "y": 10.57,
//                                    "drilldown": "computers"
//                                },
//                                {
//                                    "name": "/Home & Garden",
//                                    "y": 7.23,
//                                    "drilldown": "home"
//                                }
//                            ] //data
                        } //series
                    ], //series


                    "drilldown": {
                        "series": response[1]
                        //[
//                            {
//                                "name": "/Arts & Entertainment",
//                                "id": "arts",
//                                "data": [
//                                    {
//                                        "name": "/Movies",
//                                        "y": 36
////                                        "drilldown": "arts-movies"
//                                    },
//                                    {
//                                        "name": "/Music & Audio",
//                                        "y": 30
////                                        "drilldown": "arts-music"
//                                    },
//                                    {
//                                        "name": "/TV & Video",
//                                        "y": 33
////                                        "drilldown": "arts-tv"
//                                    }
//                                ]
//                            },
//                            {
//                                "name": "/Computers & Electronics",
//                                "id": "computers",
//                                "data": [
//                                    {
//                                        "name": "/Computer Hardware",
//                                        "y": 36
////                                        "drilldown": "computers-hardware"
//                                    },
//                                    {
//                                        "name": "/Enterprise Technology",
//                                        "y": 30
////                                        "drilldown": "arts-technology"
//                                    },
//                                    {
//                                        "name": "/Computer Security",
//                                        "y": 33
////                                        "drilldown": "arts-security"
//                                    }
//                                    /* backup for 1st drilldown
//                                    [
//                                        "v58.0",
//                                        33
//                                    ],
//                                    [
//                                        "v57.0",
//                                        33
//                                    ],
//                                    [
//                                        "v56.0",
//                                        33
//                                    ]
//                                    */
//                                ]
//                            },
//                            {
//                                "name": "/Home & Garden",
//                                "id": "home",
//                                "data": [
//                                    {
//                                        "name": "/Equipments",
//                                        "y": 36
////                                        "drilldown": "home-equipments"
//                                    },
//                                    {
//                                        "name": "/Decor",
//                                        "y": 30,
//                                        "drilldown": "home-decor"
//                                    },
//                                    {
//                                        "name": "/Renovation",
//                                        "y": 33,
//                                        "drilldown": "home-renovation"
//                                    }
//                                ]
//                            },
//                            {
//                                "name": "/Home/Decor",
//                                "id": "home-decor",
//                                "data": [
//                                    ["/Curtains", 33],
//                                    ["/Rooms", 77]
//                                ]
//                            },
//                            {
//                                "name": "/Home/Renovation",
//                                "id": "home-renovation",
//                                "data": [
//                                    ["/Outdoors", 36],
//                                    ["/Rooms", 74]
//                                ]
//                            }
//                        ], // drilldown > series
                    } //drilldown
                });
           },
           failure: function (response) {
               alert("failed");
           }
        });
    }
    else{  // if '.csv' present in query string
        $.ajax({
           type: "GET",
           url: "/service/summary_categchart/",
           data: { 'query': query },
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
//               console.log(JSON.stringify(response[0]));
//               console.log(JSON.stringify(response[1]));

               // Create the chart
                Highcharts.chart('categDonutChart', {
                    chart: {
                        type: 'pie',
                        style: {
                                fontFamily: 'Arial'
                            }
                    },
                    title: {
                        text: 'Primary Content Categories'
                    },
                    subtitle: {
                        text: 'Drill down to see secondary and tertiary categories'
                    },
                    plotOptions: {
                        series: {
                            dataLabels: {
                                enabled: true,
                                format: '{point.name}: {point.y:.1f}%'
                            }
                        }
                    },
                    tooltip: {
                        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
                    },
                    // response = [seriesData, drilldownData]
                    "series":
                    [
                        {
                            "name": "Primary Categories",
                            "colorByPoint": true,
                            "data": response[0]
                        } //series
                    ], //series


                    "drilldown": {
                        "series": response[1]
                    } //drilldown
                });
           },
           failure: function (response) {
               alert("failed");
           }
        });
    }
}


function load_wc_filter() {
   // console.log("Brand called");
   var data1 = "";

     $('.multi4').multi_select({
        //   selectColor: '#0077b5',
          selectSize: 'small',
          selectText: 'Select Data',
          duration: 300,
          easing: 'slide',
          listMaxHeight: 300,
          selectedCount: 2,
          sortByText: true,
          fillButton: true,
          data: {
            "CC": "Content categories",
            "NG": "N-grams"
          },
          onSelect: function(values) {
                reload_wordcloud("");
          }
    });

}

$("#wc_data li").click(function(){
    $('#dropdownMenu4').text($(this).text());
    //console.log($(this).text());
    reload_wordcloud("");
});

function load_wordcloud() {
    if(flag1 == false){  //if '.csv' NOT present in query string
//        console.log("loading wordcloud");
//          console.log(selStartDate,selEndDate);
        var brand = [];
        $('#brand1 .selected .text').each(function(index){
//            console.log($(this).text());
            brand.push($(this).text());
        });
//        console.log(brand);

        var source = [];
        $('#source1 .selected .text').each(function(index){
            source.push($(this).text());
        });
//        console.log(source);

        var sku = [];
        $('#sku1 .selected .text').each(function(index){
            sku.push($(this).text());
        });
//        console.log(sku);

        $.ajax({
           type: "GET",
           url: "/service/summary_wordcloud_rev/",
           data: { 'query': query , 'brand': JSON.stringify(brand), 'source': JSON.stringify(source),
           'sku': JSON.stringify(sku), 'fromDate': JSON.stringify(selStartDate), 'toDate': JSON.stringify(selEndDate)},
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
               //console.log(response);
//               console.log(JSON.parse(response));

//               var text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean bibendum erat ac justo sollicitudin, quis lacinia ligula fringilla. Pellentesque hendrerit, nisi vitae posuere condimentum, lectus urna accumsan libero, rutrum commodo mi lacus pretium erat. Phasellus pretium ultrices mi sed semper. Praesent ut tristique magna. Donec nisl tellus, sagittis ut tempus sit amet, consectetur eget erat. Sed ornare gravida lacinia. Curabitur iaculis metus purus, eget pretium est laoreet ut. Quisque tristique augue ac eros malesuada, vitae facilisis mauris sollicitudin. Mauris ac molestie nulla, vitae facilisis quam. Curabitur placerat ornare sem, in mattis purus posuere eget. Praesent non condimentum odio. Nunc aliquet, odio nec auctor congue, sapien justo dictum massa, nec fermentum massa sapien non tellus. Praesent luctus eros et nunc pretium hendrerit. In consequat et eros nec interdum. Ut neque dui, maximus id elit ac, consequat pretium tellus. Nullam vel accumsan lorem.';
//                var lines = text.split(/[,\. ]+/g),
//                    data = Highcharts.reduce(lines, function (arr, word) {
//                        //console.log("Arr", arr)
//                        //console.log("Word", word)
//                        var obj = Highcharts.find(arr, function (obj) {
//                            return obj.name === word;
//                        });
//                        if (obj) {
//                            obj.weight += 1;
//                        } else {
//                            obj = {
//                                name: word,
//                                weight: 1
//                            };
//                            arr.push(obj);
//                        }
//                        return arr;
//                    }, []);
//                //console.log(data);
                Highcharts.chart('wordcloudChart', {
                    series: [{
                        type: 'wordcloud',
                        data: response,
                        name: 'Occurrences',
                        style: {
                                fontFamily: 'Arial'
                            }
                    }],
                    title: {
                        text: 'Primary Content Categories'
                    }
                });

               //console.log(response)
           },
           failure: function (response) {
               alert("failed");
           }
        });
    }
    else{  // if '.csv' present in query string
        $.ajax({
           type: "GET",
           url: "/service/summary_wordcloud/",
           data: { 'query': query },
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
               //console.log(response[1].toString());

               var text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean bibendum erat ac justo sollicitudin, quis lacinia ligula fringilla. Pellentesque hendrerit, nisi vitae posuere condimentum, lectus urna accumsan libero, rutrum commodo mi lacus pretium erat. Phasellus pretium ultrices mi sed semper. Praesent ut tristique magna. Donec nisl tellus, sagittis ut tempus sit amet, consectetur eget erat. Sed ornare gravida lacinia. Curabitur iaculis metus purus, eget pretium est laoreet ut. Quisque tristique augue ac eros malesuada, vitae facilisis mauris sollicitudin. Mauris ac molestie nulla, vitae facilisis quam. Curabitur placerat ornare sem, in mattis purus posuere eget. Praesent non condimentum odio. Nunc aliquet, odio nec auctor congue, sapien justo dictum massa, nec fermentum massa sapien non tellus. Praesent luctus eros et nunc pretium hendrerit. In consequat et eros nec interdum. Ut neque dui, maximus id elit ac, consequat pretium tellus. Nullam vel accumsan lorem.';
                var lines = text.split(/[,\. ]+/g),
                    data = Highcharts.reduce(lines, function (arr, word) {
                        var obj = Highcharts.find(arr, function (obj) {
                            return obj.name === word;
                        });
                        if (obj) {
                            obj.weight += 1;
                        } else {
                            obj = {
                                name: word,
                                weight: 1
                            };
                            arr.push(obj);
                        }
                        return arr;
                    }, []);

                Highcharts.chart('container', {
                    series: [{
                        type: 'wordcloud',
                        data: data,
                        name: 'Occurrences',
                        style: {
                                fontFamily: 'Arial'
                            }
                    }],
                    title: {
                        text: 'Primary Content Categories'
                    }
                });
            }
        });
    }
}

function reload_wordcloud(data) {
    if(flag1 == false){  //if '.csv' NOT present in query string

//          console.log(selStartDate,selEndDate);
        var brand = [];
        $('#brand1 .selected .text').each(function(index){
//            console.log($(this).text());
            brand.push($(this).text());
        });
//        console.log(brand);

        var source = [];
        $('#source1 .selected .text').each(function(index){
            source.push($(this).text());
        });
//        console.log(source);

        var sku = [];
        $('#sku1 .selected .text').each(function(index){
            sku.push($(this).text());
        });
//        console.log(sku);

        $.ajax({
           type: "GET",
           url: "/service/summary_wordcloud_rev/",
           data: { 'query': query , 'brand': JSON.stringify(brand), 'source': JSON.stringify(source),
           'sku': JSON.stringify(sku), 'fromDate': JSON.stringify(selStartDate), 'toDate': JSON.stringify(selEndDate)},
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
               //console.log(response[1].toString());

               var text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean bibendum erat ac justo sollicitudin, quis lacinia ligula fringilla. Pellentesque hendrerit, nisi vitae posuere condimentum, lectus urna accumsan libero, rutrum commodo mi lacus pretium erat. Phasellus pretium ultrices mi sed semper. Praesent ut tristique magna. Donec nisl tellus, sagittis ut tempus sit amet, consectetur eget erat. Sed ornare gravida lacinia. Curabitur iaculis metus purus, eget pretium est laoreet ut. Quisque tristique augue ac eros malesuada, vitae facilisis mauris sollicitudin. Mauris ac molestie nulla, vitae facilisis quam. Curabitur placerat ornare sem, in mattis purus posuere eget. Praesent non condimentum odio. Nunc aliquet, odio nec auctor congue, sapien justo dictum massa, nec fermentum massa sapien non tellus. Praesent luctus eros et nunc pretium hendrerit. In consequat et eros nec interdum. Ut neque dui, maximus id elit ac, consequat pretium tellus. Nullam vel accumsan lorem.';
                var lines = text.split(/[,\. ]+/g),
                    data = Highcharts.reduce(lines, function (arr, word) {
                        //console.log("Arr", arr)
                        //console.log("Word", word)
                        var obj = Highcharts.find(arr, function (obj) {
                            return obj.name === word;
                        });
                        if (obj) {
                            obj.weight += 1;
                        } else {
                            obj = {
                                name: word,
                                weight: 1
                            };
                            arr.push(obj);
                        }
                        return arr;
                    }, []);
                //console.log(data);
                Highcharts.chart('wordcloudChart', {
                    series: [{
                        type: 'wordcloud',
                        data: data,
                        name: 'Occurrences'
                    }],
                    title: {
                        text: 'Primary Content Categories'
                    }
                });

               //console.log(response)
           },
           failure: function (response) {
               alert("failed");
           }
        });
    }
    else{  // if '.csv' present in query string
        $.ajax({
           type: "GET",
           url: "/service/summary_wordcloud/",
           data: { 'query': query },
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
               //console.log(response[1].toString());

               var text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean bibendum erat ac justo sollicitudin, quis lacinia ligula fringilla. Pellentesque hendrerit, nisi vitae posuere condimentum, lectus urna accumsan libero, rutrum commodo mi lacus pretium erat. Phasellus pretium ultrices mi sed semper. Praesent ut tristique magna. Donec nisl tellus, sagittis ut tempus sit amet, consectetur eget erat. Sed ornare gravida lacinia. Curabitur iaculis metus purus, eget pretium est laoreet ut. Quisque tristique augue ac eros malesuada, vitae facilisis mauris sollicitudin. Mauris ac molestie nulla, vitae facilisis quam. Curabitur placerat ornare sem, in mattis purus posuere eget. Praesent non condimentum odio. Nunc aliquet, odio nec auctor congue, sapien justo dictum massa, nec fermentum massa sapien non tellus. Praesent luctus eros et nunc pretium hendrerit. In consequat et eros nec interdum. Ut neque dui, maximus id elit ac, consequat pretium tellus. Nullam vel accumsan lorem.';
                var lines = text.split(/[,\. ]+/g),
                    data = Highcharts.reduce(lines, function (arr, word) {
                        var obj = Highcharts.find(arr, function (obj) {
                            return obj.name === word;
                        });
                        if (obj) {
                            obj.weight += 1;
                        } else {
                            obj = {
                                name: word,
                                weight: 1
                            };
                            arr.push(obj);
                        }
                        return arr;
                    }, []);

                Highcharts.chart('container', {
                    series: [{
                        type: 'wordcloud',
                        data: data,
                        name: 'Occurrences'
                    }],
                    title: {
                        text: 'Primary Content Categories'
                    }
                });
            }
        });
    }
}

})();