function getclosestpostlocation(data, val) {
    var mindist = 999999999;
    var minobj = null;
    $.each(data, function (k, v) {
        var dist = distance(v.lat, v.lon, val.lat, val.lon, 'K');
        if(dist < mindist) {
            mindist = dist;
            minobj = v;
        }
    });
    return { location: minobj, dist: mindist };
}

function getlocationfrompost(data, postcode) {
    postlocation = null;
    if(postcode.length === 4) {
        $.each(data, function (k, v) {
            if(postcode === v.p) {
                postlocation = v;
                return false;
            }
        });
    }
    return postlocation;
}

function filllatlon(lat, lon) {
    $('#id_lat').val(lat);
    $('#id_lon').val(lon);
}

const btnLocation = $("#btnLocation");
const postcodefield = $('#id_postcode');
var gps_accessed = false;
var post_code_correct = false;


$.getJSON(postcodejson, function (json) {
    btnLocation.click(function () {
        btnLocation
            .prop('disabled', true)
            .html(
                '<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>\n' + '  Loading...'
            );
        if ("geolocation" in navigator){
            navigator.geolocation.getCurrentPosition(show_location, show_error, {timeout:1000, enableHighAccuracy: true}); //position request
        } else {
            console.log("Browser doesn't support geolocation!");
        }
    });

    postcodefield.on('change paste keyup', function () {
        var val = $(this).val();
        var postposition = getlocationfrompost(json, val);
        if(postposition) {
            post_code_correct = true;
            if(!gps_accessed) {
                filllatlon(postposition.lat, postposition.lon);
            }
            $('#address').html(postposition.s + ', ' + postposition.t + ', ' + postposition.dis + ', ' + postposition.div + 'বিভাগ, ' + postposition.p);
        }
        else {
            post_code_correct = false;
            $('#address').html('পোস্ট কোডটি সঠিক নয়। ');
        }
    });

    //Success Callback
    function show_location(position) {
        gps_accessed = true;
        var pos = {lat: position.coords.latitude, lon: position.coords.longitude};
        res = getclosestpostlocation(json, pos);
        postcodefield.val(res.location.p);
        btnLocation.prop('disabled', false).html('আবার স্থান দেখুন।');
        filllatlon(res.location.lat, res.location.lon);
    }
    //Error Callback
    function show_error(error){
        console.log(error.code);
        switch(error.code) {
            case error.PERMISSION_DENIED:
                alert("Permission denied by user.");
                break;
            case error.POSITION_UNAVAILABLE:
                alert("Location position unavailable.");
                break;
            case error.TIMEOUT:
                alert("Request timeout.");
                break;
            case error.UNKNOWN_ERROR:
                alert("Unknown error.");
                break;
        }
        // var pos = {lat: 23.7, lon: 90.95};
        btnLocation.html('দুঃখিত, স্থান জানা যাচ্ছে না।');
        $('#address').html('দয়া করে ম্যানুয়ালি ইনপুট দেন।');
    }
});

grecaptcha.ready(function() {
    $('#formsubmit').submit(function (e) {
        var form = this;
        e.preventDefault();
        grecaptcha.execute('{{ site_key }}', {action: 'survey'}).then(function(token) {
            $('#recaptcha').val(token);
            if(post_code_correct) {
                form.submit()
            }
            else {
                // TODO: Trigger error here
            }
        });
    });
});

