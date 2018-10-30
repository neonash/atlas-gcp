(function(){

    $('#parent').removeClass('hidden');
    $('#parent').addClass('active');
    //console.log(window.location.href)
    var request = window.urlUtils.getQueryParameter(window.location.href, 'request');
    //console.log(request);
        $('#summary').attr('href', '/summary/?request='+ encodeURI(request));
//    $('#analysis').attr('href', '/analysis/?request=' + encodeURI(request));
    $('#clustering').attr('href','/clustering/?request=' + encodeURI(request));
    $('#pivot').attr('href','/pivot/?request=' + encodeURI(request));
    $('#association').attr('href','/association/?request=' + encodeURI(request));
    $('#discover').attr('href','/discover/');

    google.load("visualization", "1", {packages:["corechart", "charteditor"]});
    $(function(){
        var derivers = $.pivotUtilities.derivers;
        var renderers = $.extend($.pivotUtilities.renderers,
            $.pivotUtilities.gchart_renderers);

//        Papa.parse("/services/mps.csv", {
//            download: true,
//            skipEmptyLines: true,
//            complete: function(parsed){
//                $("#output").pivotUI(parsed.data, {
//                    renderers: renderers,
//                    derivedAttributes: {
//                        "Age Bin": derivers.bin("Age", 10),
//                        "Gender Imbalance": function(mp) {
//                            return mp["Gender"] == "Male" ? 1 : -1;
//                        }
//                    },
//                    cols: ["Age Bin"], rows: ["Gender"],
//                    rendererName: "Area Chart"
//                });
//            }
//        });
        $.ajax({
           type: "GET",
           url: "/service/pivotparser/",
           data: { 'query': request },
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (mps) {
                $('#loading').addClass('d-none');
                $('#output').removeClass('d-none');
                //console.log(mps);
                if(typeof mps === 'object'){
                    //console.log("Inside mps");
                    if(mps.length > 0){

//                        console.log(mps[0]);
                        for (i = 0; i<mps.length; i++){
                            if (mps[i][" "] == " "){
                                delete mps[i][" "];
                            }
                        }
                    }
                    else{
                        $('#chartArea').empty();
                        $('#chartArea').html("Sorry, no records found!");
                    }
                    //console.log(mps);
                }

                $("#output").pivotUI(mps, {
                    renderers: renderers,
                    rows: ["YYYY"],
                    cols: ["Brand"],
//                    rendererName: "Area Chart",
                aggregatorName: "Count Unique Values",
                vals: ["Review ID"],
                rendererOptions: {
//                    gchart:{
//                        height:400,
//                        width:600,
//                    }
                }

            });


           },
           failure: function (response) {
               alert("failed");
           }
        });
//        $.getJSON("C:\\Users\\akshat.gupta/mps.json", function(mps) {
//            $("#output").pivotUI(mps, {
//                renderers: renderers,
//                derivedAttributes: {
//                    "Age Bin": derivers.bin("Age", 10),
//                    "Gender Imbalance": function(mp) {
//                        return mp["Gender"] == "Male" ? 1 : -1;
//                    }
//                },
//                cols: ["Age Bin"], rows: ["Gender"],
//                rendererName: "Area Chart",
//                rendererOptions: {
//                    gchart:{
//                        height:400,
//                        width:600,
//                    }
//                }
//
//            });
//        });
     });

})();