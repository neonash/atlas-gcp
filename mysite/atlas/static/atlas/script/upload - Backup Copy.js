(function(){
    $(document).on('ready', function() {

        $('.upload-buttons div:first-child button:last-child').on('click', function(){
            //to upload other dicts
            try{
                $('input:checked').each(function(){
                    if($(this).attr('id') == 'senti_check'){

                        // to upload senti dict
                        var myFile = $('#upl_senti').prop('files')[0];
            //            console.log(myFile.name);

                        var fr = new FileReader();
                        fr.onload = function(){
            //                alert(fr.result);
                            $.ajax({
                                type: "POST",
                                url: "/service/upload/",
                                data: {'upl_type': 'upl_senti', "filename": myFile.name, 'filedata': fr.result},
                                success: function (response) {
                                    console.log("File uploaded");
                                },
                                failure: function (response) {
                                    alert("failed");
                                }
                            });

                        }
                        fr.readAsText( myFile );
            //             console.log(fr.result);
                    }
                    else if($(this).attr('id') == 'driver_check'){

                        // to upload driver dict
                        var myFile = $('#upl_driver').prop('files')[0];
            //            console.log(myFile.name);

                        var fr = new FileReader();
                        fr.onload = function(){
            //                alert(fr.result);
                            $.ajax({
                                type: "POST",
                                url: "/service/upload/",
                                data: {'upl_type': 'upl_driver', "filename": myFile.name, 'filedata': fr.result},
                                success: function (response) {
                                    console.log("File uploaded");
                                },
                                failure: function (response) {
                                    alert("failed");
                                }
                            });

                        }
                        fr.readAsText( myFile );
            //             console.log(fr.result);
                    }
                    else if($(this).attr('id') == 'tag_check'){

                        // to upload tag dict
                        var myFile = $('#upl_tag').prop('files')[0];
            //            console.log(myFile.name);

                        var fr = new FileReader();
                        fr.onload = function(){
            //                alert(fr.result);
                            $.ajax({
                                type: "POST",
                                url: "/service/upload/",
                                data: {'upl_type': 'upl_tag', "filename": myFile.name, 'filedata': fr.result},
                                success: function (response) {
                                    console.log("File uploaded");
                                },
                                failure: function (response) {
                                    alert("failed");
                                }
                            });

                        }
                        fr.readAsText( myFile );
            //             console.log(fr.result);
                    }
                });
            }catch(err){console.log(err);}


            // to upload dataset
            var myFile = $('#upl_data').prop('files')[0];
            console.log(myFile.name);

            var fr = new FileReader();
            fr.onload = function(){
//                alert(fr.result);
                $.ajax({
                    type: "POST",
                    url: "/service/upload/",
                    data: {'upl_type': 'upl_data', "filename": myFile.name, 'filedata': fr.result},
                    success: function (response) {
                        console.log("File uploaded");
                    },
                    failure: function (response) {
                        alert("failed");
                    }
                });

            }
            fr.readAsText( myFile );
//             console.log(fr.result);
        });




        $('.upload-buttons div:last-child button:last-child').on("click", function(){
            try{
            var myFile = $('#upl_data').prop('files')[0];
            }
            catch(err){var myFile = "Not uploaded!"}
            if(myFile.name == "Not uploaded!"){
                alert("Please upload a dataset!");
            }
            else{
                $.get('/service/start/').then(function (successResponse) {
                    //console.log('Parsed successResponse', JSON.parse(successResponse));
                }, function (errorResponse) {
                        //console.log("errorResponse", errorResponse);
                });
                alert("Analysis initiated. You can track the progress as listed on the home page.");

                location.href = "/";
            }

        });

        $('.upload-buttons div:first-child button:first-child').on("click", function(){

            $('#upl_data').attr('value', null);
            $('#senti_check').attr('checked', false);
            $('#upl_senti').attr({'value': null, 'disabled': true});
            $('#driver_check').attr('checked', false);
            $('#upl_driver').attr({'value': null, 'disabled': true});
            $('#tag_check').attr('checked', false);
            $('#upl_tag').attr({'value': null, 'disabled': true});
        });

        $("#senti_check").change(function() {
            if(this.checked) {
                $('#upl_senti').removeAttr('disabled');
            }
            else{
                $('#upl_senti').attr('disabled', true);
            }
        });

        $("#driver_check").change(function() {
            if(this.checked) {
                $('#upl_driver').removeAttr('disabled');
            }
            else{
                $('#upl_driver').attr('disabled', true);
            }
        });

        $("#tag_check").change(function() {
            if(this.checked) {
                $('#upl_tag').removeAttr('disabled');
            }
            else{
                $('#upl_tag').attr('disabled', true);
            }
        });

    });

})();