// Define the `app` module
var app = angular.module('app', []);

// Define the `PhoneListController` controller on the `app` module
app.controller('PhoneListController', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
    console.log("entered app controller");
    var foamtree = new CarrotSearchFoamTree({
      id: "visualization",
    });


    $('article ul a').tooltip({
        placement: "bottom",
        trigger: "hover"
    });
    $('[data-toggle="tooltip"]').tooltip();

    $('article ul a').on('click', function(){
        var val = $(this).text();
        var engine = val.toLowerCase();
    //        console.log(val);
            var sel = $(this).data('title');
            var tog = $(this).data('toggle');
            $('#'+tog).prop('value', sel);

            $('a[data-toggle="'+tog+'"]').not('[data-title="'+sel+'"]').removeClass('active-tab');
            $('a[data-toggle="'+tog+'"][data-title="'+sel+'"]').addClass('active-tab');
            $(this).addClass('active-tab');
        if (val == "Topic Modeling"){
            $('#row1').hide();
            $('#row2').show();
//            var query;
//            if(request.indexOf('.csv')!=-1){
//                query = request.substring(0,request.length-4);
//            }
//            else{
//                query = request;
//            }
//            $.ajax({
//                type: "GET",
//                url: "/service/clustering_topicmodel/",
//                data: { 'query': query },
//                contentType: "application/json; charset=utf-8",
//                dataType: "json",
//                success: function (response) {
//
//                },
//                failure: function (response) {
//                    alert("failed");
//                }
//            });
        }
        else{
            $('#row1').show();
            $('#row2').hide();

            drawChart(request, engine);
        }
    });
//  Clustering.js
var request = window.urlUtils.getQueryParameter(window.location.href, 'request');
    //console.log(request);
     $('#summary').attr('href', '/summary/?request='+ encodeURI(request));
//    $('#analysis').attr('href', '/analysis/?request=' + encodeURI(request));
    $('#clustering').attr('href','/clustering/?request=' + encodeURI(request));
    $('#pivot').attr('href','/pivot/?request=' + encodeURI(request));
    $('#association').attr('href','/association/?request=' + encodeURI(request));
    $('#discover').attr('href','/discover/');

    //var modal_closed_flag = false;
    //var last_response = null;

    //$("#helpModal").on('hide.bs.modal', function () {
     //       drawChart(request, "lingo");
    //});

    $(".glyphicon-info-sign").on('hover', function () {
            $('[data-toggle="tooltip"]').tooltip();
    });

    drawChart(request, "lingo");

    function drawChart(request, engine) {
        //console.log("Drawing Chart with algo=", engine);

        $scope.phones = [];

        function load_table(data) {
//            console.log(data);
            $scope.phones = [];
            $timeout(function() {
                $scope.phones = data;
            }, 0);
        }

        Array.prototype.removeValue = function(name, value){
           var array = $.map(this, function(v,i){
              return v[name] === value ? null : v;
           });
           this.length = 0; //clear original array
           this.push.apply(this, array); //push all elements except the one we want to delete
        }

        function convert(clusters) {

//            clusters.removeValue("other-topics", true);

            //        console.log("-------------------------Clusters-----------------------------------------")
//            console.log("clusters=", clusters);
//            console.log("datatype of clusters=", typeof(clusters));
            return $.map(clusters, function(cluster){
//                console.log(cluster);
                      for(var propertyName in cluster) {
                    // propertyName is what you want
                    // you can get the value like this: myObject[propertyName]
                }
                return {
                    id:     cluster.docs,
                    label:  cluster.labels,
                    weight: cluster.attributes && cluster.attributes["other-topics"] ? 0 : cluster.docs.length,
                    groups: cluster.clusters ? convert(cluster.clusters) : []
                }
            });
//            return clusters.map(function(cluster) {
//                for(var propertyName in cluster) {
//                    // propertyName is what you want
//                    // you can get the value like this: myObject[propertyName]
//                }
//                return {
//                    id:     cluster.response.docs,
//                    label:  cluster.labels,
//                    weight: cluster.attributes && cluster.attributes["other-topics"] ? 0 : cluster.docs.length,
//                    groups: cluster.clusters ? convert(cluster.clusters) : []
//                }
//             });
        }

        // Clear the previous model.
        foamtree.set("dataObject", null);
        foamtree.set("logging", true);

        var url = "";

        if(request.indexOf('.csv')!=-1){
            //console.log(request.substring(0,request.length-4));
//            $http.get("http://localhost:8983/solr/MY_PRODUCT3/dataimport?command=full-import&indent=on&wt=json").then(function(response) {});
//            $http.get("http://localhost:8983/solr/MY_PRODUCT3_1/dataimport?command=full-import&indent=on&wt=json").then(function(response){});
            $.ajax({
                type: "GET",
                url: "/service/clustering_data_social/",
                data: {"query": request, 'engine': engine},
                success: function (response) {
                    var response = JSON.parse(response);
//                         console.log("parsing response for clustering");
//                        console.log("Response = ", response);
//                        console.log(typeof (JSON.parse(response)));
//                        console.log('length of response.data.clusters > ');
//                            console.log(response.data.clusters.length);
                            //last_response = response;
                            //console.log(response.data.response.numFound)
                            if (response.response.numFound > 0){

                                foamtree.set({
                                    dataObject: {
//                                        groups: convert(response.data.clusters)
                                        groups: convert(response.clusters)
                                    },

                                    onGroupSelectionChanged: function(info) {
                                        //console.log("info > ");
//                                        console.log(info);

                                        var selectedClusterObjects = [];
                                        selectedCluster = {};

                                        function findText(element) {
//                                            console.log("data.response.docs = ", response.data.response.docs)
//                                            console.log("element= " , element);
//                                            console.log("inside findText()");
                                            response.response.docs.forEach(function(e)  {
//                                                console.log("looping thru response docs");
                                                if(request.localeCompare('Kelloggs')==0){
                                                    if(element.localeCompare(e.t_id) == 0){
                                                        //console.log("e.rtext = ", e.rText)
                                                        selectedCluster.rText = e.t_text;
                                                        if((e.t_title).toString() == 'nan'){
                                                            selectedCluster.rTitle = "";
                                                        }
                                                        else{
                                                            selectedCluster.rTitle = e.t_title;
                                                        }
                                                        selectedCluster = {};
                                                        selectedClusterObjects.push(selectedCluster);
                                                        //console.log(selectedClusterObjects)
                                                    }
                                                }
                                                else if(request.localeCompare('Cars')==0){
                                                    if(element.localeCompare(e.c_id) == 0){
                                                        //console.log("e.rtext = ", e.rText)
                                                        selectedCluster.rText = e.c_text;
                                                        if((e.c_title).toString() == 'nan'){
                                                            selectedCluster.rTitle = "";
                                                        }
                                                        else{
                                                            selectedCluster.rTitle = e.c_title;
                                                        }
                                                        selectedCluster = {};
                                                        selectedClusterObjects.push(selectedCluster);
//                                                        console.log("length(selectedClusterObjects)", selectedClusterObjects.length);
                                                    }
                                                }
                                                else {
                                                    //console.log("e=", e);
                                                    if(element.localeCompare(e.rid) == 0){
//                                                        console.log("e.rid= ", e.rid);
//                                                        console.log("e.rtext = ", e.rText)
                                                        selectedCluster = {};
                                                        selectedCluster.rText = e.rText;
                                                        if((e.rTitle).toString() == 'nan'){
                                                            selectedCluster.rTitle = "";
                                                        }
                                                        else{
                                                            selectedCluster.rTitle = e.rTitle;
                                                        }


                                                        selectedClusterObjects.push(selectedCluster);
                                                        //console.log("selected cluster");
                                                        //console.log(selectedCluster);
                                                    }
                                                }
                                            });
                                        }

//                                        console.log("info.groups[0]=", info.groups[0]);

                                        info.groups[0].id.forEach(function(ele) {
//                                            console.log("ele=", ele);
                                            findText(ele);
                                        });
                                        //console.log(reviewText)
//                                        console.log(selectedClusterObjects);
                                        load_table(selectedClusterObjects);
                                    },
                                });

                        //      console.log(foamtree.get("selection").groups);
                                //console.log(data.response.docs)
                                load_table(response.response.docs);

                             }
                             else {
                                    $.ajax({
                                    type: "GET",
                                    url: "/service/clustering_data_upload/",
                                    data: {"query": request, 'engine': engine},
                                    success: function (response) {
                                        var response = JSON.parse(response);
                    //                         console.log("parsing response for clustering");
//                                            console.log("Response = ", response);
                    //                        console.log(typeof (JSON.parse(response)));
                    //                        console.log('length of response.data.clusters > ');
                    //                            console.log(response.data.clusters.length);
                                                //last_response = response;
                                                //console.log(response.data.response.numFound)
                                                if (response.response.numFound > 0){

                                                    foamtree.set({
                                                        dataObject: {
                    //                                        groups: convert(response.data.clusters)
                                                            groups: convert(response.clusters)
                                                        },

                                                        onGroupSelectionChanged: function(info) {
                                                            //console.log("info > ");
                    //                                        console.log(info);

                                                            var selectedClusterObjects = [];
                                                            selectedCluster = {};

                                                            function findText(element) {
                    //                                            console.log("data.response.docs = ", response.data.response.docs)
                    //                                            console.log("element= " , element);
                    //                                            console.log("inside findText()");
                                                                response.response.docs.forEach(function(e)  {
                    //                                                console.log("looping thru response docs");
                                                                    if(request.localeCompare('Kelloggs')==0){
                                                                        if(element.localeCompare(e.t_id) == 0){
                                                                            //console.log("e.rtext = ", e.rText)
                                                                            selectedCluster.rText = e.t_text;
                                                                            if((e.t_title).toString() == 'nan'){
                                                                                selectedCluster.rTitle = "";
                                                                            }
                                                                            else{
                                                                                selectedCluster.rTitle = e.t_title;
                                                                            }
                                                                            selectedCluster = {};
                                                                            selectedClusterObjects.push(selectedCluster);
                                                                            //console.log(selectedClusterObjects)
                                                                        }
                                                                    }
                                                                    else if(request.localeCompare('Cars')==0){
                                                                        if(element.localeCompare(e.c_id) == 0){
                                                                            //console.log("e.rtext = ", e.rText)
                                                                            selectedCluster.rText = e.c_text;
                                                                            if((e.c_title).toString() == 'nan'){
                                                                                selectedCluster.rTitle = "";
                                                                            }
                                                                            else{
                                                                                selectedCluster.rTitle = e.c_title;
                                                                            }
                                                                            selectedCluster = {};
                                                                            selectedClusterObjects.push(selectedCluster);
//                                                                            console.log("length(selectedClusterObjects)", selectedClusterObjects.length);
                                                                        }
                                                                    }
                                                                    else {
                                                                        //console.log("e=", e);
                                                                        if(element.localeCompare(e.rid) == 0){
                    //                                                        console.log("e.rid= ", e.rid);
                    //                                                        console.log("e.rtext = ", e.rText)
                                                                            selectedCluster = {};
                                                                            selectedCluster.rText = e.rText;
                                                                            if((e.rTitle).toString() == 'nan'){
                                                                                selectedCluster.rTitle = "";
                                                                            }
                                                                            else{
                                                                                selectedCluster.rTitle = e.rTitle;
                                                                            }


                                                                            selectedClusterObjects.push(selectedCluster);
                                                                            //console.log("selected cluster");
                                                                            //console.log(selectedCluster);
                                                                        }
                                                                    }
                                                                });
                                                            }

                    //                                        console.log("info.groups[0]=", info.groups[0]);

                                                            info.groups[0].id.forEach(function(ele) {
                    //                                            console.log("ele=", ele);
                                                                findText(ele);
                                                            });
                                                            //console.log(reviewText)
//                                                            console.log(selectedClusterObjects);
                                                            load_table(selectedClusterObjects);
                                                        },
                                                    });

                                            //      console.log(foamtree.get("selection").groups);
                                                    //console.log(data.response.docs)
                                                    load_table(response.response.docs);

                                                 }
                                                 else if (response.response.numFound == 0){
                                                    $('#chartArea').children().removeClass('active');
                                                    $('#chartArea').children().addClass('hidden');
                                                    $('#chartArea').text('Please try reloading the page. If the chart still does not load, then data for the request is not present!');
                                                 }
                                    },
                                    failure: function (response) {
                                        alert("failed");
                                    }
                                });

                             }
                },
                failure: function (response) {
                    alert("failed");
                }
            });
            }


        else{
            //console.log('importing myproduct');

            try{
//            console.log("entered try");
            $.ajax({
                type: "GET",
                url: "/service/clustering_data/",
                data: {"query": request, 'engine': engine},
                success: function (response) {
                    var response = JSON.parse(response);
//                         console.log("parsing response for clustering");
//                        console.log("Response = ", response);
//                        console.log(typeof (JSON.parse(response)));
//                        console.log('length of response.data.clusters > ');
//                            console.log(response.data.clusters.length);
                            //last_response = response;
                            //console.log(response.data.response.numFound)
                            if (response.response.numFound > 0){

                                foamtree.set({
                                    dataObject: {
//                                        groups: convert(response.data.clusters)
                                        groups: convert(response.clusters)
                                    },

                                    onGroupSelectionChanged: function(info) {
                                        //console.log("info > ");
//                                        console.log(info);

                                        var selectedClusterObjects = [];
                                        selectedCluster = {};

                                        function findText(element) {
//                                            console.log("data.response.docs = ", response.data.response.docs)
//                                            console.log("element= " , element);
//                                            console.log("inside findText()");
                                            response.response.docs.forEach(function(e)  {
//                                                console.log("looping thru response docs");
                                                if(request.localeCompare('Kelloggs')==0){
                                                    if(element.localeCompare(e.t_id) == 0){
                                                        //console.log("e.rtext = ", e.rText)
                                                        selectedCluster.rText = e.t_text;
                                                        if((e.t_title).toString() == 'nan'){
                                                            selectedCluster.rTitle = "";
                                                        }
                                                        else{
                                                            selectedCluster.rTitle = e.t_title;
                                                        }
                                                        selectedCluster = {};
                                                        selectedClusterObjects.push(selectedCluster);
                                                        //console.log(selectedClusterObjects)
                                                    }
                                                }
                                                else if(request.localeCompare('Cars')==0){
                                                    if(element.localeCompare(e.c_id) == 0){
                                                        //console.log("e.rtext = ", e.rText)
                                                        selectedCluster.rText = e.c_text;
                                                        if((e.c_title).toString() == 'nan'){
                                                            selectedCluster.rTitle = "";
                                                        }
                                                        else{
                                                            selectedCluster.rTitle = e.c_title;
                                                        }
                                                        selectedCluster = {};
                                                        selectedClusterObjects.push(selectedCluster);
//                                                        console.log("length(selectedClusterObjects)", selectedClusterObjects.length);
                                                    }
                                                }
                                                else {
                                                    //console.log("e=", e);
                                                    if(element.localeCompare(e.rid) == 0){
//                                                        console.log("e.rid= ", e.rid);
//                                                        console.log("e.rtext = ", e.rText)
                                                        selectedCluster = {};
                                                        selectedCluster.rText = e.rText;
                                                        if((e.rTitle).toString() == 'nan'){
                                                            selectedCluster.rTitle = "";
                                                        }
                                                        else{
                                                            selectedCluster.rTitle = e.rTitle;
                                                        }


                                                        selectedClusterObjects.push(selectedCluster);
                                                        //console.log("selected cluster");
                                                        //console.log(selectedCluster);
                                                    }
                                                }
                                            });
                                        }

//                                        console.log("info.groups[0]=", info.groups[0]);

                                        info.groups[0].id.forEach(function(ele) {
//                                            console.log("ele=", ele);
                                            findText(ele);
                                        });
                                        //console.log(reviewText)
//                                        console.log(selectedClusterObjects);
                                        load_table(selectedClusterObjects);
                                    },
                                });

                        //      console.log(foamtree.get("selection").groups);
                                //console.log(data.response.docs)
                                load_table(response.response.docs);

                             }
                             else if (response.response.numFound == 0){
                                $('#chartArea').children().removeClass('active');
                                $('#chartArea').children().addClass('hidden');
                                $('#chartArea').text('Please try reloading the page. If the chart still does not load, then data for the request is not present!');
                             }
                },
                failure: function (response) {
                    alert("failed");
                }
            });
            }catch(err){
            //console.log("entered catch");
            console.log(err);
                }


//            //trying ajax call
//            $.ajax({
//                type: "GET",
////                "async": true,
//                url: "http://35.231.18.86/solr/MY_PRODUCT/clustering?q=pCategory:"+ request +"&clustering.engine="+ engine +"&wt=jsonp&indent=on",
////                data: {},
////                crossDomain:true,
//                crossOrigin:true,
//                beforeSend: function (xhr) {
////                    xhr.setRequestHeader ("Authorization", "Basic " + encodedString);
//                    xhr.setRequestHeader ("Authorization", "Basic " + btoa(username + ":" + password));
//                },
//                dataType: "jsonp",
//                headers: {
//                    "Authorization": "Basic " + encodedString,
////                    "Cache-Control": "no-cache",
////                    "Postman-Token": "a3d1f4d6-2006-4a8e-82f7-523195a4e13c",
//                    "From-Origin": "http://127.0.0.1:8000",
//                    "Access-Control-Allow-Origin" : '*',
////                    "X-Content-Type-Options": 'nosniff',
//                    'Content-Type': "text/html",
//                     'Access-Control-Allow-Credentials': true,
//                },
//                success: function (response) {
//                    try{
//                        console.log("inside try of successresponse");
//                        console.log("this is the the response: ", response);
//                        }catch(err){console.log(" inside catch of successresponse");}
//                },
//                failure: function (response) {
//                    alert("failed");
//                }
//            });
//            }catch(err){
//            console.log("entered catch");console.log(err);
//                }

                // trying http request
//
//            $http.get("http://35.231.18.86/solr/MY_PRODUCT/dataimport?command=full-import&indent=on&wt=json").then(function(response) {
//                console.log("data import command given");
//                if(response.data.statusMessages["Total Documents Processed"] != 0){
////                    console.log(response.data.statusMessages["Total Documents Processed"]);
//                    //url = "http://localhost:8983/solr/MY_PRODUCT/clustering?q=pCategory:"+ request +"&clustering.engine="+ engine +"&wt=json&indent=on";
//                    url = "http://35.231.18.86/solr/MY_PRODUCT/clustering?q=pCategory:"+ request +"&clustering.engine="+ engine +"&wt=json&indent=on";
////                    console.log(url);
//                    $http.get(url).then(function(response) {
//                        console.log("parsing response for clustering");
////                        console.log("Response = ", response);
////                        console.log('data = ', response.data.clusters);
////                        console.log('length of response.data.clusters > ');
////                            console.log(response.data.clusters.length);
//                            //last_response = response;
//                            //console.log(response.data.response.numFound)
//                            if (response.data.response.numFound > 0){
//
//                                foamtree.set({
//                                    dataObject: {
////                                        groups: convert(response.data.clusters)
//                                        groups: convert(response.data.clusters)
//                                    },
//
//                                    onGroupSelectionChanged: function(info) {
//                                        //console.log("info > ");
////                                        console.log(info);
//
//                                        var selectedClusterObjects = [];
//                                        selectedCluster = {};
//
//                                        function findText(element) {
////                                            console.log("data.response.docs = ", response.data.response.docs)
////                                            console.log("element= " , element);
////                                            console.log("inside findText()");
//                                            response.data.response.docs.forEach(function(e)  {
////                                                console.log("looping thru response docs");
//                                                if(request.localeCompare('Kelloggs')==0){
//                                                    if(element.localeCompare(e.t_id) == 0){
//                                                        //console.log("e.rtext = ", e.rText)
//                                                        selectedCluster.rText = e.t_text;
//                                                        if((e.t_title).toString() == 'nan'){
//                                                            selectedCluster.rTitle = "";
//                                                        }
//                                                        else{
//                                                            selectedCluster.rTitle = e.t_title;
//                                                        }
//                                                        selectedCluster = {};
//                                                        selectedClusterObjects.push(selectedCluster);
//                                                        //console.log(selectedClusterObjects)
//                                                    }
//                                                }
//                                                else if(request.localeCompare('Cars')==0){
//                                                    if(element.localeCompare(e.c_id) == 0){
//                                                        //console.log("e.rtext = ", e.rText)
//                                                        selectedCluster.rText = e.c_text;
//                                                        if((e.c_title).toString() == 'nan'){
//                                                            selectedCluster.rTitle = "";
//                                                        }
//                                                        else{
//                                                            selectedCluster.rTitle = e.c_title;
//                                                        }
//                                                        selectedCluster = {};
//                                                        selectedClusterObjects.push(selectedCluster);
//                                                        console.log("length(selectedClusterObjects)", selectedClusterObjects.length);
//                                                    }
//                                                }
//                                                else {
//                                                    console.log("e=", e);
//                                                    if(element.localeCompare(e.rid) == 0){
////                                                        console.log("e.rid= ", e.rid);
////                                                        console.log("e.rtext = ", e.rText)
//                                                        selectedCluster = {};
//                                                        selectedCluster.rText = e.rText;
//                                                        if((e.rTitle).toString() == 'nan'){
//                                                            selectedCluster.rTitle = "";
//                                                        }
//                                                        else{
//                                                            selectedCluster.rTitle = e.rTitle;
//                                                        }
//
//
//                                                        selectedClusterObjects.push(selectedCluster);
//                                                        //console.log("selected cluster");
//                                                        //console.log(selectedCluster);
//                                                    }
//                                                }
//                                            });
//                                        }
//
////                                        console.log("info.groups[0]=", info.groups[0]);
//
//                                        info.groups[0].id.forEach(function(ele) {
////                                            console.log("ele=", ele);
//                                            findText(ele);
//                                        });
//                                        //console.log(reviewText)
//                                        console.log(selectedClusterObjects);
//                                        load_table(selectedClusterObjects);
//                                    },
//                                });
//
//                        //      console.log(foamtree.get("selection").groups);
//                                //console.log(data.response.docs)
//                                load_table(response.data.response.docs);
//
//                             }
//                             else if (response.data.response.numFound == 0){
//                                $('#chartArea').children().removeClass('active');
//                                $('#chartArea').children().addClass('hidden');
//                                $('#chartArea').text('Please try reloading the page. If the chart still does not load, then data for the request is not present!');
//                             }
//                    },  //success response
//                    function(response){
//                        console.log("this is not success response: ", response);
//                    });
//                }
//            });
//

        }
    }

    $('#btnFullImport').on('click', function(){
          $.ajax({
                type: "GET",
                url: "/service/clustering_fullimport/",
                data: {},
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function (response) {
                    console.log("Full import done.");
                },
                failure: function (response) {
                    alert("failed");
                }
            });
    });

    $.get('/service/request/').then(function (successResponse) {

        }, function (errorResponse) {

        console.log("errorResponse", errorResponse)
    });

    //$scope.$apply();
}]);
