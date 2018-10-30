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

    $('#loading').addClass('d-none');
    $('#output').removeClass('d-none');
//    document.getElementById("ifr").innerHTML='<object type="type/html" data="http://172.16.15.4:8080/#/notebook/2DTP82UXX';

//    window.open("http://172.16.15.4:8080/#/notebook/2DTP82UXX");

    $('#link-anchor').on('click', function(){
        $(this).attr({'href':'http://172.16.15.4:8080/#/notebook/2DTP82UXX', 'target':'_blank'});
    });
    $('#link-anchor')[0].click();



//    $.ajax({
//       type: "GET",
//       headers: { 'Access-Control-Allow-Origin': '*', 'X-Frame-Options': 'ALLOW-FROM http://172.16.15.4' },
//       url: "/service/discover_service/",
//       data: {'query': request},
//       contentType: "text/html",
//       success: function (response) {
////            console.log(response);
////            console.log(JSON.parse(response)[0]);
//
//
//
//            $('#loading').addClass('d-none');
//            $('#output').removeClass('d-none');
//            $('#ifr').load('http://172.16.15.4:8080/#/notebook/2DTP82UXX', function(){
//                console.log($('#ifr').text());
//            });
//            var el = document.getElementById('output');
////            el.innerHTML = JSON.parse(response)[0];
////            console.log(el.innerHTML);



//       },
//       failure: function (response) {
//           alert("failed");
//       }
//    });

})();