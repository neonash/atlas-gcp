(function(){

    $('#parent').removeClass('hidden');
    $('#parent').addClass('active');
//    $('.chartjs-hidden-iframe').css({'overflow':'auto'});
    //(window.location.href)

    var request = window.urlUtils.getQueryParameter(window.location.href, 'request');
    $('#summary').attr('href', '/summary/?request='+ encodeURI(request));
//    $('#analysis').attr('href', '/analysis/?request=' + encodeURI(request));
    $('#clustering').attr('href','/clustering/?request=' + encodeURI(request));
    $('#pivot').attr('href','/pivot/?request=' + encodeURI(request));
    $('#association').attr('href','/association/?request=' + encodeURI(request));
    $('#discover').attr('href','/discover/');

    is_first_load = true;

    var onDimChange = function(e) {
        //console.log("dim change detected");
//        load_levs($('#dims').val());  // to update levels filter
        load_assoc_map();  //reload map directly, when levels filter not there
    };

    var onLevChange = function (e){
//        console.log(e);

        load_assoc_map();
    };

    if (is_first_load == true){
        is_first_load = false;
        load_dims();
    }
    else{

    }

    function load_dims(){
        // console.log("dimension called");
       $.ajax({
           type: "GET",
           url: "/service/assoc_dims/",
           data: { 'query': request },
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
               //console.log("load dims response", response);
               if(response.length > 0){
                    $('#dims').off('change', onDimChange);

               var $dim = $('#dims');
//               console.log($dim);
               $("#dims").selectpicker();
//               $dim.find('option').remove();
               $dim.find('li').remove();
                var temp_flag = "";
               $.each(response, function (key, value) {
//               console.log("Key:", key)
//               console.log("Value:", value);

                   if (value != null)  {
                        if (temp_flag == ""){
                            temp_flag = value;
                            $('#dropdownMenu3').text(value);
                            $('<li class="dropdown-item"/>').text(value).appendTo($dim);
                        }
                        else{
                            $('<li class="dropdown-item"/>').text(value).appendTo($dim);
                        }
                    }


                });

                $('#dims').selectpicker('refresh');
//                $("#Chart1select").selectpicker("refresh");

                $("#dims li").click(function(){
                    $('#dropdownMenu3').text($(this).text());
                    //console.log($(this).text());
                    load_assoc_map();
                });
                var sel_dim = $("#dropdownMenu3").text();
                //console.log(sel_dim);
//                 load_levs(sel_dim);  // to lead levels filter
                load_assoc_map();
                 $('#dims').on('change', onDimChange);

               }
               else{
//                    $('.portlet-body').empty();
//                    $('.portlet-body').html("Sorry, no records found!");

               }
           },
           failure: function (response) {
               alert("failed");
           }
       });
    }

    function load_levs(sel_dim){
        // console.log("level called");

       $.ajax({
           type: "GET",
           url: "/service/assoc_levels/",
           data: { 'query': request, 'dim': sel_dim },
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
               //console.log(response);
                $('#levs').off('change', onLevChange);

               var $lev = $('#levs');
               $("#levs").selectpicker();
               $lev.find('option').remove();

               $.each(response, function (key, value) {
    //           console.log("Key:", key)
    //           console.log("Value:", value.pBrand)
                   if (value != null) {
                       $('<option/>').val(value).text(value).appendTo($lev);
                   }
               });
              $('#levs').selectpicker('refresh');
              //$("#Chart1select").selectpicker("refresh");

//                var sel_lev = $("#levs option:first").val();
//                $("#levs").val(sel_lev);

//                $("#marksChart").remove();
//                $('#chartjs-radar').append('<canvas id="marksChart"></canvas>');
                load_assoc_map();
                $('#levs').on('change', onLevChange);
           },
           failure: function (response) {
               alert("failed");
           }
       });
    }


    function load_assoc_map(){
        //console.log("loading assoc map");
        var dim = $('#dropdownMenu3').text();
        //console.log(dim);

//        var lev = $("#levs").val();
        $.ajax({
           type: "GET",
           url: "/service/association/",
//           data: { 'query': request, 'dim': dim, 'lev': lev },
           data: { 'query': request, 'dim': dim},
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {

                //console.log(response);
                try{
                    if(String(response[0]).indexOf("no records") == -1){
                        d3.select("#output").selectAll("*").remove();

                        mpld3.draw_figure("output", response['graph_data']);

                        var sourceObj = eval('(' + response.source_data + ')');


                        for (i in sourceObj) {
                            if (sourceObj.hasOwnProperty(i)) {
                                var feature_labels = Object.keys(sourceObj[i]);
                                break;
                            }
                        }

                        // Radar chart code starts here
        //                d3.select('#chartjs-radar > iframe').destroy();
                        try{

                            $("#myChart").remove();

                            $('#chartjs-radar').append('<canvas id="myChart"></canvas>');

                            var ctx = document.getElementById("myChart").getContext('2d');
//                            console.log("Chart=", Chart.defaults);
//                            Chart.defaults.results.global.defaultFontFamily = "Arial";
                            Chart.defaults.global.defaultFontFamily = "Arial";
//                            Chart.defaults.global.defaultFontSize = 16;
                //            console.log(sourceObj)

                            var sourceData = {
                                labels: feature_labels,
                                datasets: [],
                //              datasets: [{
                //                label: "Student A",
                //                backgroundColor: "transparent",
                //                borderColor: window.chartColors.red,
                //                fill: false,
                //                radius: 6,
                //                pointRadius: 6,
                //                pointBorderWidth: 3,
                //                pointBackgroundColor: "orange",
                //                pointBorderColor: "rgba(200,0,0,1)",
                //                pointHoverRadius: 10,
                //                data: [65, 75, 70, 80, 60, 80]
                //              }, {
                //                label: "Student B",
                //                backgroundColor: "transparent",
                //                borderColor: "rgba(0,0,200,1)",
                //                fill: false,
                //                radius: 6,
                //                pointRadius: 6,
                //                pointBorderWidth: 3,
                //                pointBackgroundColor: "cornflowerblue",
                //                pointBorderColor: "rgba(0,0,200,1)",
                //                pointHoverRadius: 10,
                //                data: [54, 65, 60, 70, 70, 75]
                //              }]
                            };

                             window.chartColors = {
                              red: 'rgba(255, 0, 0, 1)',
                              orange: 'rgba(255, 159, 64, 1)',
                              yellow: 'rgba(255, 205, 86, 1)',
                              green: 'rgba(75, 192, 192, 1)',
                              blue: 'rgba(0, 0, 200, 1)',
                              purple: 'rgba(153, 102, 255, 1)',
                              grey: 'rgba(231, 233, 237, 1)',
                              cornflowerblue: 'rgba(100, 149, 237, 1)',
                              deepblue: 'rgb(38, 51, 63, 1)',
                              cyan: 'rgb(70, 240, 240, 1)',
                              magenta: 'rgb(240, 50, 230, 1)',
                              lime: 'rgb(210, 245, 60, 1)',
                              pink: 'rgb(250, 190, 190, 1)',
                              teal: 'rgb(0, 128, 128, 1)',
                              lavender: 'rgb(230, 190, 255, 1)',
                              brown: 'rgb(170, 110, 40, 1)',
                              beige: 'rgb(255, 250, 200, 1)',
                              maroon: 'rgb(128, 0, 0, 1)',
                              mint: 'rgb(170, 255, 195, 1)',
                              olive: 'rgb(128, 128, 0, 1)',
                              coral: 'rgb(255, 215, 180, 1)',
                              navy: 'rgb(0, 0, 128, 1)',
                              white: 'rgb(255, 255, 255, 1)',
                              black: 'rgb(0, 0, 0, 1)',
                              darkgrey: 'rgb(192, 192, 192, 1)'
                            };

                            var combinations = [
                                {0: window.chartColors.red, 1:window.chartColors.orange},
                                {0: window.chartColors.purple, 1:window.chartColors.pink},
                                {0: window.chartColors.green, 1:window.chartColors.yellow},
                                {0: window.chartColors.orange, 1:window.chartColors.yellow},
                                {0: window.chartColors.teal, 1:window.chartColors.cyan},
                                {0: window.chartColors.navy, 1:window.chartColors.cornflowerblue},
                                {0: window.chartColors.maroon, 1:window.chartColors.brown},
                                {0: window.chartColors.olive, 1:window.chartColors.lime},
                                {0: window.chartColors.brown, 1:window.chartColors.beige},
                                {0: window.chartColors.darkgrey, 1:window.chartColors.black},
                                {0: window.chartColors.mint, 1:window.chartColors.grey},
                                {0: window.chartColors.black, 1:window.chartColors.grey},

                                {0: window.chartColors.red, 1:window.chartColors.pink},
                                {0: window.chartColors.purple, 1:window.chartColors.yellow},
                                {0: window.chartColors.green, 1:window.chartColors.maroon},
                                {0: window.chartColors.orange, 1:window.chartColors.darkgrey},
                                {0: window.chartColors.teal, 1:window.chartColors.lime},
                                {0: window.chartColors.navy, 1:window.chartColors.beige},
                                {0: window.chartColors.maroon, 1:window.chartColors.mint},
                                {0: window.chartColors.olive, 1:window.chartColors.red},
                                {0: window.chartColors.brown, 1:window.chartColors.blue},
                                {0: window.chartColors.darkgrey, 1:window.chartColors.cornflowerblue},
                                {0: window.chartColors.mint, 1:window.chartColors.darkgrey},
                                {0: window.chartColors.black, 1:window.chartColors.beige},

                                {0: window.chartColors.red, 1:window.chartColors.green},
                                {0: window.chartColors.purple, 1:window.chartColors.mint},
                                {0: window.chartColors.green, 1:window.chartColors.brown},
                                {0: window.chartColors.orange, 1:window.chartColors.black},
                                {0: window.chartColors.teal, 1:window.chartColors.brown},
                                {0: window.chartColors.navy, 1:window.chartColors.maroon},
                                {0: window.chartColors.maroon, 1:window.chartColors.deepblue},
                                {0: window.chartColors.olive, 1:window.chartColors.black},
                                {0: window.chartColors.brown, 1:window.chartColors.black},
                                {0: window.chartColors.darkgrey, 1:window.chartColors.mint},
                                {0: window.chartColors.mint, 1:window.chartColors.brown},
                                {0: window.chartColors.black, 1:window.chartColors.blue},
                            ];

                            var max = 0;

                            for(i in sourceObj){

                                var newObj = {};

                                newObj.label = i;

                                var data = new Array;

                                //console.log(sourceObj[i])
                                //break;
                                for(var o in sourceObj[i]) {

                                    data.push(sourceObj[i][o]);

            //                        console.log(sourceObj[i][o]);
                                    if(max<sourceObj[i][o])

                                        max = sourceObj[i][o];

                                }

                                newObj.data = data;

                                newObj.label = i;

                                newObj.backgroundColor = "transparent";

                                newObj.fill = false;

                                newObj.radius = 6;

                                newObj.pointRadius = 6;

                                newObj.pointBorderWidth = 3;

                                newObj.pointHoverRadius = 10;


                                var randomNumber = Math.floor(Math.random() * combinations.length);

                                newObj.borderColor = combinations[randomNumber][0];

                                newObj.pointBackgroundColor = combinations[randomNumber][1];

                                newObj.pointBorderColor = combinations[randomNumber][0];


                                combinations.splice(randomNumber,1);

                //                console.log(newObj)
                //                console.log(data)
                                //newObj.data = sourceObj[i];
                                //console.log(newObj)
                                sourceData.datasets.push(newObj);

                //                break;
                            }

                            //console.log("sourceData=", sourceData);

                            var chartOptions = {
    //                           responsive: false,
                               maintainAspectRatio: true,
    //                           scaleOverride: true,
                                scale: {
                                    gridLines: {
                                       color: "black",
                                       lineWidth: 2
                                    },
                                    angleLines: {
                                      display: true
                                    },
                                    ticks: {
                                        //Boolean - Show a backdrop to the scale label
                                        showLabelBackdrop: true,

                                        //String - The colour of the label backdrop
                                        backdropColor: "rgba(255,255,255,0.75)",

                                        //Number - The backdrop padding above & below the label in pixels
                                        backdropPaddingY: 2,

                                        //Number - The backdrop padding to the side of the label in pixels
                                        backdropPaddingX: 2,

                                        //Number - Limit the maximum number of ticks and gridlines
                                        maxTicksLimit: 11,
                                        beginAtZero: true,
    //                                    min: 0,
    //                                    max: Math.round(max / 50)*50,
    //                                    stepSize: Math.round(max/(Object.keys(sourceObj).length/2) / 100)*100
                                    },
                                    pointLabels: {
                                        fontSize: 14,
                                        fontColor: "green",
                                        defaultFontFamily: "Arial"
                                    }
                                },
                                legend: {
                                    position: 'left'
                                }
            //                    events: ['click'],
            //                    tooltips: {
            //                        mode: 'point'
            //                    }
                            };

                            var radarChart = new Chart(ctx, {
                                  type: 'radar',
                                  data: sourceData,
                                  options: chartOptions
                            });
            //                alert("radar chart loaded");

                            radarChart.update();

    //                        radarChart.reDraw();
                        }
                        catch(err){console.log(err);}
                    }
                    else{
                        $('#chartjs-radar').hide();
                        $('#chartjs-radar').parent().html('<div style="background-color:#f0f2f5">' + response + '</div>');
                    }
                }catch(err){console.log(err);}
          },
           failure: function (response) {
               alert("failed");
           }
        });
    }


    function update_assoc_map(dim, lev, chart){
        //console.log("reloading assoc map");
        $.ajax({
           type: "GET",
           url: "/service/association/",
           data: { 'query': request, 'dim': dim, 'lev': lev },
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
                //console.log("response = ", typeof(response))
                d3.select("#output").selectAll("*").remove();
                mpld3.draw_figure("output", response['graph_data']);
                var sourceObj = eval('(' + response.source_data + ')');
                //console.log((sourceObj));

                for (i in sourceObj) {
                    if (sourceObj.hasOwnProperty(i)) {
                        var feature_labels = Object.keys(sourceObj[i]);
                        break;
                    }
                }

                // Radar chart code starts here
//                $("#marksChart").destroy();
//                $('#chartjs-radar').append('<canvas id="marksChart"></canvas>');
                var marksCanvas = document.getElementById("marksChart");

                Chart.defaults.global.defaultFontFamily = "Arial";
                Chart.defaults.global.defaultFontSize = 16;
    //            console.log(sourceObj)

                var sourceData = {
                    labels: feature_labels,
                    datasets: [],
    //              datasets: [{
    //                label: "Student A",
    //                backgroundColor: "transparent",
    //                borderColor: window.chartColors.red,
    //                fill: false,
    //                radius: 6,
    //                pointRadius: 6,
    //                pointBorderWidth: 3,
    //                pointBackgroundColor: "orange",
    //                pointBorderColor: "rgba(200,0,0,1)",
    //                pointHoverRadius: 10,
    //                data: [65, 75, 70, 80, 60, 80]
    //              }, {
    //                label: "Student B",
    //                backgroundColor: "transparent",
    //                borderColor: "rgba(0,0,200,1)",
    //                fill: false,
    //                radius: 6,
    //                pointRadius: 6,
    //                pointBorderWidth: 3,
    //                pointBackgroundColor: "cornflowerblue",
    //                pointBorderColor: "rgba(0,0,200,1)",
    //                pointHoverRadius: 10,
    //                data: [54, 65, 60, 70, 70, 75]
    //              }]
                };

                 window.chartColors = {
                  red: 'rgba(255, 0, 0, 1)',
                  orange: 'rgba(255, 159, 64, 1)',
                  yellow: 'rgba(255, 205, 86, 1)',
                  green: 'rgba(75, 192, 192, 1)',
                  blue: 'rgba(0, 0, 200, 1)',
                  purple: 'rgba(153, 102, 255, 1)',
                  grey: 'rgba(231, 233, 237, 1)',
                  cornflowerblue: 'rgba(100, 149, 237, 1)',
                  deepblue: 'rgb(38, 51, 63, 1)',
                  cyan: 'rgb(70, 240, 240, 1)',
                  magenta: 'rgb(240, 50, 230, 1)',
                  lime: 'rgb(210, 245, 60, 1)',
                  pink: 'rgb(250, 190, 190, 1)',
                  teal: 'rgb(0, 128, 128, 1)',
                  lavender: 'rgb(230, 190, 255, 1)',
                  brown: 'rgb(170, 110, 40, 1)',
                  beige: 'rgb(255, 250, 200, 1)',
                  maroon: 'rgb(128, 0, 0, 1)',
                  mint: 'rgb(170, 255, 195, 1)',
                  olive: 'rgb(128, 128, 0, 1)',
                  coral: 'rgb(255, 215, 180, 1)',
                  navy: 'rgb(0, 0, 128, 1)',
                  white: 'rgb(255, 255, 255, 1)',
                  black: 'rgb(0, 0, 0, 1)',
                  darkgrey: 'rgb(192, 192, 192, 1)'
                };

                var combinations = [
                    {0: window.chartColors.red, 1:window.chartColors.orange},
                    {0: window.chartColors.purple, 1:window.chartColors.pink},
                    {0: window.chartColors.green, 1:window.chartColors.yellow},
                    {0: window.chartColors.orange, 1:window.chartColors.yellow},
                    {0: window.chartColors.teal, 1:window.chartColors.cyan},
                    {0: window.chartColors.navy, 1:window.chartColors.cornflowerblue},
                    {0: window.chartColors.maroon, 1:window.chartColors.brown},
                    {0: window.chartColors.olive, 1:window.chartColors.lime},
                    {0: window.chartColors.brown, 1:window.chartColors.beige},
                    {0: window.chartColors.darkgrey, 1:window.chartColors.black},
                    {0: window.chartColors.mint, 1:window.chartColors.grey},
                    {0: window.chartColors.black, 1:window.chartColors.grey},

                    {0: window.chartColors.red, 1:window.chartColors.pink},
                            {0: window.chartColors.purple, 1:window.chartColors.yellow},
                            {0: window.chartColors.green, 1:window.chartColors.maroon},
                            {0: window.chartColors.orange, 1:window.chartColors.darkgrey},
                            {0: window.chartColors.teal, 1:window.chartColors.lime},
                            {0: window.chartColors.navy, 1:window.chartColors.beige},
                            {0: window.chartColors.maroon, 1:window.chartColors.mint},
                            {0: window.chartColors.olive, 1:window.chartColors.red},
                            {0: window.chartColors.brown, 1:window.chartColors.blue},
                            {0: window.chartColors.darkgrey, 1:window.chartColors.cornflowerblue},
                            {0: window.chartColors.mint, 1:window.chartColors.darkgrey},
                            {0: window.chartColors.black, 1:window.chartColors.beige},

                            {0: window.chartColors.red, 1:window.chartColors.green},
                            {0: window.chartColors.purple, 1:window.chartColors.mint},
                            {0: window.chartColors.green, 1:window.chartColors.brown},
                            {0: window.chartColors.orange, 1:window.chartColors.black},
                            {0: window.chartColors.teal, 1:window.chartColors.brown},
                            {0: window.chartColors.navy, 1:window.chartColors.maroon},
                            {0: window.chartColors.maroon, 1:window.chartColors.deepblue},
                            {0: window.chartColors.olive, 1:window.chartColors.black},
                            {0: window.chartColors.brown, 1:window.chartColors.black},
                            {0: window.chartColors.darkgrey, 1:window.chartColors.mint},
                            {0: window.chartColors.mint, 1:window.chartColors.brown},
                            {0: window.chartColors.black, 1:window.chartColors.blue},
                ];

                var max = 0;

                for(i in sourceObj){
                    var newObj = {};
                    newObj.label = i;
                    var data = new Array;
                    //console.log(sourceObj[i])
                    //break;
                    for(var o in sourceObj[i]) {
                        data.push(sourceObj[i][o]);
//                        console.log(sourceObj[i][o]);
                        if(max<sourceObj[i][o])
                            max = sourceObj[i][o];
                    }
                    newObj.data = data;
                    newObj.label = i;
                    newObj.backgroundColor = "transparent";
                    newObj.fill = false;
                    newObj.radius = 6;
                    newObj.pointRadius = 6;
                    newObj.pointBorderWidth = 3;
                    newObj.pointHoverRadius = 10;

                    var randomNumber = Math.floor(Math.random() * combinations.length);

                    newObj.borderColor = combinations[randomNumber][0];
                    newObj.pointBackgroundColor = combinations[randomNumber][1];
                    newObj.pointBorderColor = combinations[randomNumber][0];

                    combinations.splice(randomNumber,1);
    //                console.log(newObj)
    //                console.log(data)
                    //newObj.data = sourceObj[i];
                    //console.log(newObj)
                    sourceData.datasets.push(newObj);
    //                break;
                }

                //console.log(sourceData);

                var chartOptions = {
//                   responsive: false,
//                   maintainAspectRatio: true,
//                   scaleOverride: true,
                    scale: {
                        gridLines: {
                           color: "black",
                           lineWidth: 3
                        },
                        angleLines: {
                          display: false
                        },
                        ticks: {
                            //Boolean - Show a backdrop to the scale label
                            showLabelBackdrop: true,

                            //String - The colour of the label backdrop
                            backdropColor: "rgba(255,255,255,0.75)",

                            //Number - The backdrop padding above & below the label in pixels
                            backdropPaddingY: 2,

                            //Number - The backdrop padding to the side of the label in pixels
                            backdropPaddingX: 2,

                            //Number - Limit the maximum number of ticks and gridlines
                            maxTicksLimit: 11,
                            beginAtZero: true,
                            min: 0,
                            max: Math.round(max / 50)*50,
                            stepSize: Math.round(max/(Object.keys(sourceObj).length/2) / 100)*100
                        },
                        pointLabels: {
                            fontSize: 14,
                            fontColor: "green",
                            defaultFontFamily: "Arial"
                        }
                    },
                    legend: {
                        position: 'left'
                    }
                };

                chart.data = sourceData;
                chart.options = chartOptions;

                chart.update();
                //console.log('Done');

          },
           failure: function (response) {
               alert("failed");
           }
        });
    }


})();