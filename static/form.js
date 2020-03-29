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
    var val = postcodefield.val();
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

    showhelpdiv();

    $('input[name="travel_14_days"]').change(showhelpdiv);
    $('input[name="travel_infected_3_month"]').change(showhelpdiv);
    $('input[name="close_contact"]').change(showhelpdiv);

    if(cookied) {
        console.log(cookied);
        $('.cookied').show();
    }
    else {
        console.log(!cookied);
        $('.cookied').hide();
    }

    btnLocation.click(function () {
        btnLocation
            .prop('disabled', true)
            .html(
                '<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>\n' + '  Loading...'
            );
        postcodefield.val('');
        if ("geolocation" in navigator){
            navigator.geolocation.getCurrentPosition(show_location, show_error, {timeout:10000, enableHighAccuracy: true}); //position request
        } else {
            $('#address').html('আপনার ব্রাউসার সাপোর্ট করে না।');
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
        if(res.dist < 1200) {
            post_code_correct = true;
            postcodefield.val(res.location.p);
            filllatlon(res.location.lat, res.location.lon);
            $('#address').html(res.location.s + ', ' + res.location.t + ', ' + res.location.dis + ', ' + res.location.div + 'বিভাগ, ' + res.location.p);
        }
        else {
            post_code_correct = false;
            $('#address').html('<b style="color: red">আপনি দেশের বাইরে অবস্থিত।</b>');
        }
        btnLocation.prop('disabled', false).html('আবার স্থান দেখুন।');
    }
    //Error Callback
    function show_error(error){
        console.log(error.code);
        const addtext = $('#address');
        switch(error.code) {
            case error.PERMISSION_DENIED:
                addtext.html('অনুমতি পাওয়া যায় নি।');
                break;
            case error.POSITION_UNAVAILABLE:
                addtext.html('জিপিএস কাজ করছে না।');
                break;
            case error.TIMEOUT:
                addtext.html('ইন্টারনেট অনেক ধীর।');
                break;
            case error.UNKNOWN_ERROR:
                addtext.html('জিপিএস কাজ করছে না।');
                break;
        }
        // var pos = {lat: 23.7, lon: 90.95};
        btnLocation.html('দুঃখিত, স্থান জানা যাচ্ছে না।');
    }

});

function showhelpdiv() {
    if(
        $('#id_travel_14_days_0').is(':checked') ||
        $('#id_travel_infected_3_month_0').is(':checked') ||
        $('#id_close_contact_0').is(':checked')
    ) {
        $('.warning-msg').show();
    }
    else {
        $('.warning-msg').hide();
    }
}

grecaptcha.ready(function() {
    $('#formsubmit').submit(function (e) {
        e.preventDefault();
        var form = this;
        if(post_code_correct) {
            grecaptcha.execute(site_key, {action: 'survey'}).then(function(token) {
                $('#recaptcha').val(token);
                form.submit();
            });
        }
        else {
            $('#address').html('<b style="color: red">পোস্ট কোডটি সঠিক নয়।</b>');
        }
    });

});

