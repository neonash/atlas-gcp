(function() {
//    $("#main-panel").addClass('hidden');
//    $('#refresh-data').addClass('hidden');
//    $('#search').addClass('active');
//$('#create-request').addClass('hidden');
//$('#request-notification').addClass('hidden');

    var searchQuery = null;

//    //Read the requests from the request queue
//    $.get('/service/request/').then(function (successResponse) {
//
//        //console.log('Stringify successResponse', JSON.stringify(successResponse,null, 2));
//        console.log('Parsed successResponse', JSON.parse(successResponse));
////        var clients = [
////            { "Request ID": "001", "Product": "TV", "Time": "16:54 Feb 20th 2016" , "Status": "Completed"},
////            { "Request ID": "002", "Product": "iMac", "Time": "20:01 April 10th 2016" ,"Status": "Completed"},
////            { "Request ID": "003", "Product": "iPad", "Time": "15:41 January 31st 2017" ,"Status": "Processing"},
////            { "Request ID": "004", "Product": "iPhone", "Time": "13:09 February 15th " ,"Status": "Pending"},
////            { "Request ID": "005", "Product": "Chrome Book" , "Time": "00:45 February 21st" ,"Status": "Pending"}
////        ];
//
//        //This function is used to populate jsGrid div to load contents of requests queue from DB
//    function JSONToCSVConvertor(JSONData, ReportTitle, ShowLabel) {
//
//        //If JSONData is not an object then JSON.parse will parse the JSON string in an Object
//        var arrData = typeof JSONData != 'object' ? JSON.parse(JSONData) : JSONData;
//        var CSV = '';
//        //This condition will generate the Label/Header
//        if (ShowLabel) {
//            var row = "";
//
//            //This loop will extract the label from 1st index of on array
//            for (var index in arrData[0]) {
//                //Now convert each value to string and comma-seprated
//                row += index + ',';
//            }
//            row = row.slice(0, -1);
//            //append Label row with line break
//            CSV += row + '\r\n';
//        }
//
//        //1st loop is to extract each row
//        for (var i = 0; i < arrData.length; i++) {
//            var row = "";
//            //2nd loop will extract each column and convert it in string comma-seprated
//            for (var index in arrData[i]) {
//                row += '"' + arrData[i][index] + '",';
//            }
//            row.slice(0, row.length - 1);
//            //add a line break after each row
//            CSV += row + '\r\n';
//        }
//
//        if (CSV == '') {
//            alert("Invalid data while downloading");
//            return;
//        }
//        else{
//            return(CSV);
//        }
//    }
//
//        $("#jsGrid").jsGrid({
//            width: "100%",
//            height: "400px",
//
//            inserting: false,
//            editing: false,
//            sorting: true,
//            paging: true,
//            autoload: true,
//            selecting:true,
//            pageLoading: true,
//            loadIndication: true,
//            loadMessage: "Please, wait...",
//
//            data: JSON.parse(successResponse),
//
//            fields: [
//                { name: "id", type: "text", width: 40, title:"ID" },
//                { name: "reqKw", type: "text", width: 200, title: "Product" },
//                { name: "reqTime", type: "text", width: 150, title: "Time" },
//                { name: "reqStatus", type: "text", width: 100, title: "Status" },
//                { name: "downloadraw", itemTemplate: function(value) {
//                            return $("<a>").attr({href: "#", class: "rawdata-download-link"}).text("Download");
//                        }, width: 100, title: "Raw data" },
//                { name: "downloadngram", itemTemplate: function(value) {
//                            return $("<a>").attr({href: "#", class: "ngram-download-link"}).text("Download");
//                        }, width: 100, title: "Ngrams" },
//                { name: "downloadtagged", itemTemplate: function(value) {
//                            return $("<a>").attr({href: "#", class: "tagdata-download-link"}).text("Download");
//                        }, width: 100, title: "Tagged data" },
//            ],
//            rowClick: function(args) {
////                console.log($(args.event.target).closest("a"));
//                // save selected item
//                selectedItem = args.item;
//                // save selected row
//                $selectedRow = $(args.event.target).closest("tr");
//                $selectedCell = $(args.event.target).closest("a");
//                $selectedCellClass = $(args.event.target).closest("a").attr("class");
////                console.log($selectedCell);
//                // add class to highlight row
//                $selectedRow.addClass("selected-row");
////                console.log(selectedItem);
////                console.log(selectedItem.reqKw);
//
//                try{
//
//                    if($selectedCellClass == 'ngram-download-link'){
////                        console.log("ngram-download-link click");
//                        var query = selectedItem.reqKw;
//                        $.ajax({
//                            type: 'GET',
//                            url: '/service/download_ngrams',
//                            headers: {
//                                'X-CSRFToken': $.cookie('X-CSRFToken')
//                            },
//                            data:  {'name': query , },
//                            success: function(response) {
//                                try{
//                                    parsed_data= JSONToCSVConvertor(JSON.parse(response), "Ngrams", true);
//    //                                console.log(parsed_data);
//                                    var mime_type = mime_type || "text/csv";
//
//                                    var blob = new Blob([parsed_data], {type: mime_type});
//
//                                    var dlink = document.createElement('a');
//                                    dlink.download = name;
//                                    dlink.href = window.URL.createObjectURL(blob);
//                                    dlink.onclick = function(e) {
//                                        // revokeObjectURL needs a delay to work properly
//                                        var that = this;
//                                        setTimeout(function() {
//                                            window.URL.revokeObjectURL(that.href);
//                                        }, 1500);
//                                    };
//
//                                    dlink.click();
//                                    dlink.remove();
//
//
//
//    //                                if(typeof(response).toString() == "string"){
//    //                                    response = JSON.parse(response);
//    //                                }
//    //                                console.log(typeof(response));
//    ////                                .constructor);
//    //                                if(!typeof(response).toString() == "object"){
//    //                                    console.log($selectedCell);
//    //                                    console.log(typeof($selectedCell));
//    //                                    $selectedCell.attr("disabled", true);
//    //                                }
//    //                                else{
//    ////                                 console.log($selectedCell);
//    ////                                    console.log(typeof($selectedCell))
//    //                                    $selectedCell.attr("disabled", false);
//
//
//    //                                    // Get the snackbar DIV
//    //                                    var x = document.getElementById("snackbar");
//    //                                    x.innerText = "Download complete";
//    //                                    // Add the "show" class to DIV
//    //                                    x.className = "show";
//    //
//    //                                    // After 3 seconds, remove the show class from DIV
//    //                                    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
//    //                                    console.log("Download complete.");
//    //                    //                alert('Download complete');
//    //
//    //                                }
//                                }
//                                catch(err){
//                                    console.log(err);
//                                }
//                            },
//                            failure: function(response) {
//                                alert("Failure");
//                            }
//                        });
//                    }
//                    else if($selectedCellClass == 'tagdata-download-link'){
//                        console.log("tagdata-download-link click");
//                        var query = selectedItem.reqKw;
//                        $.ajax({
//                            type: 'GET',
//                            url: '/service/download_tagdata',
//                            headers: {
//                                'X-CSRFToken': $.cookie('X-CSRFToken')
//                            },
//                            data:  {'name': query , },
//                            success: function(response) {
//                                try{
//                                parsed_data= JSONToCSVConvertor(JSON.parse(response), "Tagged data", true);
////                                console.log(parsed_data);
//                                var mime_type = mime_type || "text/csv";
//
//                                var blob = new Blob([parsed_data], {type: mime_type});
//
//                                var dlink = document.createElement('a');
//                                dlink.download = name;
//                                dlink.href = window.URL.createObjectURL(blob);
//                                dlink.onclick = function(e) {
//                                    // revokeObjectURL needs a delay to work properly
//                                    var that = this;
//                                    setTimeout(function() {
//                                        window.URL.revokeObjectURL(that.href);
//                                    }, 1500);
//                                };
//
//                                dlink.click();
//                                dlink.remove();
//
////                                // Get the snackbar DIV
////                                var x = document.getElementById("snackbar");
////                                x.innerText = "Download complete";
////                                // Add the "show" class to DIV
////                                x.className = "show";
////
////                                // After 3 seconds, remove the show class from DIV
////                                setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
////                                console.log("Download complete.");
////                //                alert('Download complete');
//
//                                }catch(err){
//                                    console.log(err);
//                                }
//                            },
//                            failure: function(response) {
//                                alert("Failure");
//                            }
//                        });
//                    }
//                    else if($selectedCellClass == 'rawdata-download-link'){
//                        console.log("rawdata-download-link click");
//                        var query = selectedItem.reqKw;
//
//                        $.ajax({
//                            type: 'GET',
//                            url: '/service/download_rawdata',
//                            headers: {
//                                'X-CSRFToken': $.cookie('X-CSRFToken')
//                            },
//                            data:  {'name': query , },
//                            success: function(response) {
//                                parsed_data= JSONToCSVConvertor(JSON.parse(response), "Raw data", true);
////                                console.log(parsed_data);
//                                var mime_type = mime_type || "text/csv";
//
//                                var blob = new Blob([parsed_data], {type: mime_type});
//
//                                var dlink = document.createElement('a');
//                                dlink.download = name;
//                                dlink.href = window.URL.createObjectURL(blob);
//                                dlink.onclick = function(e) {
//                                    // revokeObjectURL needs a delay to work properly
//                                    var that = this;
//                                    setTimeout(function() {
//                                        window.URL.revokeObjectURL(that.href);
//                                    }, 1500);
//                                };
//
//                                dlink.click();
//                                dlink.remove();
//
//
////                                // Get the snackbar DIV
////                                var x = document.getElementById("snackbar");
////                                x.innerText = "Download complete";
////                                // Add the "show" class to DIV
////                                x.className = "show";
////
////                                // After 3 seconds, remove the show class from DIV
////                                setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
////                                console.log("Download complete.");
////                //                alert('Download complete');
//
//                            },
//                            failure: function(response) {
//                                alert("Failure");
//                            }
//                        });
//                    }
//                    else{
//                        window.location = "../summary/?request=" + encodeURI(selectedItem.reqKw);
//                    }
//                }catch(err){
//                    console.log("row click ");
//                    window.location = "../summary/?request=" + encodeURI(selectedItem.reqKw);
//                }
//            },
//        });
//    }, function (errorResponse) {
//            console.log("errorResponse", errorResponse)
//    });

    /* //FUNCTION TO LOAD REQUESTS QUEUE FROM CSV
    $("#jsGrid").jsGrid({
            width: "100%",
            height: "400px",

            inserting: false,
            editing: false,
            sorting: true,
            paging: true,
            autoload: true,
            pageLoading: true,
            loadIndication: true,
            loadMessage: "Please, wait...",

            data: JSON.parse(successResponse),

            fields: [
                { name: "reqId", type: "text", width: 100, title:"Request ID" },
                { name: "reqKw", type: "text", width: 150, title: "Product" },
                { name: "reqTime", type: "text", width: 150, title: "Time" },
                { name: "reqStatus", type: "text", width: 150, title: "Status" },
                { name: "downloadngram", itemTemplate: function(value) {
                            return $("<a>").attr({href: "#", class: "ngram-download-link"}).text("Download");
                        }, width: 150, title: "Download ngram" },
                { name: "downloadtagged", itemTemplate: function(value) {
                            return $("<a>").attr({href: "#", class: "tagdata-download-link"}).text("Download");
                        }, width: 150, title: "Download tagged file" },
            ],
            rowClick: function(args) {
                console.log($(args.event.target).closest("a"));
                // save selected item
                selectedItem = args.item;
                // save selected row
                $selectedRow = $(args.event.target).closest("tr");
                $selectedCell = $(args.event.target).closest("a");
                $selectedCellClass = $(args.event.target).closest("a").attr("class");
                console.log($selectedCell);
                // add class to highlight row
                $selectedRow.addClass("selected-row");
                console.log(selectedItem);
                console.log(selectedItem.reqKw);

                try{

                    if($selectedCellClass == 'ngram-download-link'){
                        console.log("ngram-download-link click");
                        var query = selectedItem.reqKw;
                        $.ajax({
                            type: 'GET',
                            url: '/service/request3',
                            headers: {
                                'X-CSRFToken': $.cookie('X-CSRFToken')
                            },
                            data:  {'name': query , },
                            success: function(response) {
                                var myWindow = window.open('');
                                myWindow.document.write(response);
                                if(typeof(response).toString() == "string"){
                                    response = JSON.parse(response);
                                }
                                console.log(typeof(response));
//                                .constructor);
                                if(!typeof(response).toString() == "object"){
                                    console.log($selectedCell);
                                    console.log(typeof($selectedCell));
                                    $selectedCell.attr("disabled", true);
                                }
                                else{
//                                 console.log($selectedCell);
//                                    console.log(typeof($selectedCell))
                                    $selectedCell.attr("disabled", false);
                                    // Get the snackbar DIV
                                    var x = document.getElementById("snackbar");
                                    x.innerText = "Download complete";
                                    // Add the "show" class to DIV
                                    x.className = "show";

                                    // After 3 seconds, remove the show class from DIV
                                    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
                                    console.log("Download complete.");
                    //                alert('Download complete');

                                }

                            },
                            failure: function(response) {
                                alert("Failure")
                            }
                        });
                    }
                    else if($selectedCellClass == 'tagdata-download-link'){
                        console.log("tagdata-download-link click");
                        var query = selectedItem.reqKw;
                        $.ajax({
                            type: 'GET',
                            url: '/service/request2',
                            headers: {
                                'X-CSRFToken': $.cookie('X-CSRFToken')
                            },
                            data:  {'name': query , },
                            success: function(response) {
                                var myWindow = window.open('');
                                myWindow.document.open();
                                myWindow.document.write(response);
                                myWindow.document.close();
                                // Get the snackbar DIV
                                var x = document.getElementById("snackbar");
                                x.innerText = "Download complete";
                                // Add the "show" class to DIV
                                x.className = "show";

                                // After 3 seconds, remove the show class from DIV
                                setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
                                console.log("Download complete.");
                //                alert('Download complete');

                            },
                            failure: function(response) {
                                alert("Failure")
                            }
                        });
                    }
                    else{
                        window.location = "../summary/?request=" + encodeURI(selectedItem.reqKw);
                    }
                }catch(err){
                    console.log("row click ");
                    window.location = "../summary/?request=" + encodeURI(selectedItem.reqKw);
                }
            },
        });
    }, function (errorResponse) {
            console.log("errorResponse", errorResponse)
    });
    */

    $('#testbtn').on("click", function(){
        $.get('/service/testscrape/').then(function (successResponse) {
            console.log("test scrape command done");
            console.log(successResponse);
//            window.open("");
        }, function (errorResponse) {
                console.log("errorResponse", errorResponse);
        });
    });

    /*
    $('#allCheckboxes').on("change", ":checkbox", function () {
        if (this.checked) {
            console.log(this.id + ' is checked');
            console.log(this.name + ' is checked');

        } else {
            console.log(this.id + ' is unchecked');
            console.log(this.name + ' is unchecked');

        }
    });
*/


    //    $('tr').on('click', function(){
        $('#reqTable').on('click', 'td', function(){
            if($(this).attr('class').indexOf('-download-link') == -1){
                console.log("this is clickable");
                console.log($(this));
                //get the link from data attribute
                var the_link = $(this).parent().attr("data-href-template");
                console.log(the_link);

                //do we have a valid link
                if (the_link == '' || typeof the_link === 'undefined') {
                    //do nothing for now
                }
                else {
                    //open the page
                    var query = $(this).parent().children('td:nth-child(2)').text();
//                    if(query.indexOf('.csv') != -1){
//                        query = query.substring(0, query.length - 4);
//                    }
                    console.log(the_link + query);
                    window.location = the_link + query;
                }
            }


        });

    $('#reqTable').on('mouseover', 'tr.clickable-row', function(){
          $(this).css("cursor", "pointer");
          $(this).css("background-color", "#c4e2ff");
        });

    $('#reqTable').on('mouseout', 'tr.clickable-row', function(){
          $(this).css("cursor", "pointer");
          var par_color= $(this).parent().css("background-color");
          $(this).css("background-color", par_color);
        });

//    // Define the `app` module
//    (function(){
//    var app = angular.module('app', []);
//
//    // Define the `requestsController` controller on the `app` module
//    app.controller('requestsController', ['$scope', '$http', function ($scope, $http) {
//        $scope.csv_preform = [];
////        $scope.headers_list = ['reqId','reqKw','reqDate','reqStatus','Download data'];
//
//    //    Read the requests from the request queue
//        $.get('/service/request1/').then(function (successResponse) {
//            var response = JSON.parse(successResponse);
////            console.log('Parsed successResponse', response);
//            var csv_preform1 = [];
//            for(i=0; i<response.length; i++){
////                console.log(response[i]);
//                csv_preform1.push(response[i]);
//            }
//
//            $scope.csv_preform = csv_preform1;
//            $scope.$apply();
//
//        }, function (errorResponse) {
//                console.log("errorResponse", errorResponse)
//        });
//    }])
//    })();

    $('#reqTable').on('click', 'td.tagdata-download-link', function (e) {
        console.log("This is linkclick");
        var query = $(this).parent().children('td:nth-child(2)').text();
        console.log(query);
        $.ajax({
            type: 'GET',
            url: '/service/request2',
            headers: {
                'X-CSRFToken': $.cookie('X-CSRFToken')
            },
            data:  {'name': query , },
            success: function(response) {
                // Get the snackbar DIV
                var x = document.getElementById("snackbar");
                x.innerText = "Download complete";
                // Add the "show" class to DIV
                x.className = "show";

                // After 3 seconds, remove the show class from DIV
                setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
                console.log("Download complete.");
//                alert('Download complete');

            },
            failure: function(response) {
                alert("Failure")
            }
        });
    });

    $('#reqTable').on('click', 'td.ngram-download-link', function (e) {
        console.log("This is linkclick");
        var query = $(this).parent().children('td:nth-child(2)').text();
        console.log(query);
        $.ajax({
            type: 'GET',
            url: '/service/request3',
            headers: {
                'X-CSRFToken': $.cookie('X-CSRFToken')
            },
            data:  {'name': query , },
            success: function(response) {
                // Get the snackbar DIV
                var x = document.getElementById("snackbar");
                x.innerText = "Download complete";
                // Add the "show" class to DIV
                x.className = "show";

                // After 3 seconds, remove the show class from DIV
                setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
                console.log("Download complete.");
//                alert('Download complete');

            },
            failure: function(response) {
                alert("Failure")
            }
        });
    });



    $('#search-query-submit').on('click', function (e) {
        var data1 = { 'site' : [], 'tagdict': []};
        var site_data = [];
        var tag_dict = [];
        $(":checked").each(function() {
            console.log($(this).attr('id').indexOf('Dict'));
            if($(this).attr("id").indexOf('Dict') == -1){
                data1['site'].push($(this).val());
                site_data.push($(this).val());
            }
            else{  // if ($(this).attr("id").indexOf('Dict') != -1)
//                if($(this).id == 'chkBoxDictFood'){
                console.log($(this).val());
                    data1['tagdict'].push($(this).val());

//                else if($(this).id == 'chkBoxDictCG'){
//                data1['tagdict'].push($(this).val());
////                    data1['tagdict'].push("C:\\Users\\akshat.gupta\\PycharmProjects\\atlas\\mysite\\atlas\\database\\TaggingDicts\\electronics_dict.csv");
//                }
//                else if($(this).id == 'chkBoxDictDS'){
//                data1['tagdict'].push($(this).val());
////                    data1['tagdict'].push("C:\\Users\\akshat.gupta\\PycharmProjects\\atlas\\mysite\\atlas\\database\\TaggingDicts\\RB_supplements_dictionary_2903.csv");
//                }
                console.log(data1['tagdict']);
                tag_dict.push($(this).val());

            }
        });
        //console.log(data1['site'])
        console.log(site_data);
        if(site_data.length != 0){
            //console.log(typeof(site_data))

            var refresh = "false";
            query = $('#search-query').val();
            console.log('searchQuery', query);
            if(query.length != 0){
//                $('.dashboard').addClass('disabled');
                $('#create-request').attr('style', 'visibility:hidden');
                $('#request-notification').attr('style', 'visibility:hidden');

                //$('#create-request #make-request').attr('href', '/requests/?request=');

                $.get('/service/product?query=' + query).then(function (successResponse) {
                    //console.log('successResponse', successResponse);
//                    $('#refresh-info').removeAttr('style');
//                    $('#refresh-data').removeAttr('style');

                    //$('#refresh-data').attr('href', '/requests/?request='+ encodeURI(query) + '&refresh=true')
                    $('#refresh-data').on('click', function(e) {

                        //console.log("Inside refresh");
                    });
                    //activateDashboard(JSON.parse(successResponse).analyticData, query)
                }, function (errorResponse) {
                    //console.log('errorResponse', errorResponse);
                    if (errorResponse.status == "404") {
                        //console.log("Changing search value button to submit");
//                        $('#create-request').removeClass('hidden');
                        var cnfm = confirm("Are you sure?");
                        if(cnfm == true){
                            //console.log("Button clicked");
                            //var refresh = window.urlUtils.getQueryParameter(window.location.href, 'refresh');
                            //console.log(refresh);
                            var type = null;
                            var url= null;

                            if(refresh==="true") {
                                //console.log("PUT CALL");
                                type='PUT';
                                url = "/service/product/" + encodeURI(query) + '/refresh'
                            } else {
                                //console.log("POST CALL");
                                type= 'POST';
                                url = "/service/product/add"
                            }
                            $.ajax({
                                type: type,
                                url: url,
                                headers: {
                                    'X-CSRFToken': $.cookie('X-CSRFToken')
                                },
                                data:  {'name': query , 'site': JSON.stringify(site_data), 'tagdict': JSON.stringify(tag_dict)},
                                success: function(response) {
                                    alert("Request raised succesfully. Please check the status of your data in the Queue.");
                                    $("#request-notification").fadeTo(2000, 500).slideUp(500, function(){
                                        $("#request-notification").slideUp(500);
                                    });
//                                    alert(JSON.stringify(tag_dict));
                                    location.reload(true);

                                },
                                failure: function(response) {
                                    alert("Failure")
                                }
                            });
                            //console.log("Ajax call request = ", query)

                        }
                        else{
                            alert("false");
                        }
                        //////$('#create-request #make-request').attr('href', '/requests/?request='+ encodeURI(query) + '&refresh=false')
                        refresh = "false"

                        $('#create-request #make-request').on('click', function (e) {
                            //console.log("Button clicked");
                            //var refresh = window.urlUtils.getQueryParameter(window.location.href, 'refresh');
                            //console.log(refresh);
                            var type = null;
                            var url= null;

                            if(refresh==="true") {
                                //console.log("PUT CALL");
                                type='PUT';
                                url = "/service/product/" + encodeURI(query) + '/refresh'
                            } else {
                                //console.log("POST CALL");
                                type= 'POST';
                                url = "/service/product/add"
                            }
                            $.ajax({
                                type: type,
                                url: url,
                                headers: {
                                    'X-CSRFToken': $.cookie('X-CSRFToken')
                                },
                                data:  {'name': query , 'site': JSON.stringify(site_data), 'tagdict': JSON.stringify(tag_dict)},
                                success: function(response) {
                                    alert("Request raised succesfully");
                                    $("#request-notification").removeAttr("style");
//                                    alert(JSON.stringify(tag_dict));
                                    location.reload(true);

                                },
                                failure: function(response) {
                                    alert("Failure")
                                }
                            });
                            //console.log("Ajax call request = ", query)
                        });
                    }
                    else{}
                        //console.log("error response : non-404");
                });
            }
            else{
                alert("Please enter the keyword to search for!");
            }

        }
        else{
            alert("Please select a source!");
        }
    });


    var activateDashboard = function(dashboards, request) {
        $('#main-panel').removeClass('hidden');
        //console.log(dashboards["sentimentData"].length);
        //console.log(dashboards["sentimentData"]);
        if (dashboards["sentimentData"] && dashboards["sentimentData"].length > 0) {
            //console.log("sentiment data available");
            $('#sentiment').removeClass('disabled');
            $('#sentiment').attr('href', '/sentiment/?request=' + request);
        } else {
            //console.log('Nothing available');
        }
    }
    })();