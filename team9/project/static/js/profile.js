var verifycode="";

function getVerified(tag) {
    var phonenum = document.getElementById('phoneNum').value.toString();
    console.log(phonenum);
    $.ajax({
        url:"/project/sendVerifyCode/"+phonenum,
        type:"POST",
        data: "&csrfmiddlewaretoken="+getCSRFToken(),
        dataType:"json",
        success: function(response) {
            verifycode = response;
            console.log(verifycode);
            //document.getElementById('verify_code').value = verifycode;
            //displayError(response.error); 
        }
    }); 

    var flag = arguments[0];
    if (flag == 0) {
        $("#verification_code").append(
        '<td><label class="col-sm-2 col-md-12 control-label" style="margin:20px"  id = "verify_code_label">' +
        'verification code:</label></td><td>' +
        '<input type="text" name="verification_code" id = "verify_code" value=""></td>'
        );
        $("#button1").remove();
        $("#veri_buttons").append(
            '<button class="btn btn-primary btn-sm" onclick="getVerified(1)" id = "resendButton">'
            + 'Resend verification code</button>'
        );
        $("#verification_footer").prepend (
            '<button class="btn btn-primary btn-sm" onclick="verifyPhone()" id = "submitVerifyButton">Submit</button>'
        );
    }
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}

function verifyPhone(){
    var inputcode = document.getElementById('verify_code').value;
    if(inputcode == verifycode){
        console.log("success");
        message = "phone number has been changed successfully";
        document.getElementById('verify_code_label').remove();
        document.getElementById('verify_code').remove();
        document.getElementById('resendButton').remove();
        document.getElementById('submitVerifyButton').remove();
        $("#veri_buttons").append(
            '<button id="button1" class="btn btn-primary btn-sm" onclick="getVerified(0)">Get verification code</button>'
        );
    }
    else{
        console.log("fail");
        error = "wrong verification code, try again";
        document.getElementById('verify_code').value="";
    }
}

var addr;
var lat;
var lng;

function addFavoriteLocation() {
    var autocomplete = new google.maps.places.Autocomplete(document.getElementById('addFavLo'));

    google.maps.event.addListener(autocomplete, 'place_changed',function() {
        var place = autocomplete.getPlace();
        addr = place.formatted_address;
        lat = place.geometry.location.lat();
        lng = place.geometry.location.lng();
        var location = "<b>Address:</b>" + place.formatted_address + "<br />";
        location += "<b>Latitude:</b>" + place.geometry.location.lat() + "<br/>";
        location += "<b>Longitude:</b>" + place.geometry.location.lng();
        console.log(place);
        document.getElementById('addFavLoRst').innerHTML = location

    });
}

function sendLocation() {
    console.log(addr);
    console.log(lat);
    console.log(lng);
    var data = {'address':addr, 'latitude':lat, 'longitude':lng};
    $.ajax({
        url:"add-favorite-location",
        data: data,
        // {
        //     "address": addr,
        //     "latitude": lat,
        //     "longitude":lng
        // },
        dataType : "json",
        contentType: 'application/json',
        type:"POST",
        // traditional:true,
        success: function(result) {

        }
    });
}

google.maps.event.addDomListener(window, 'load', addFavoriteLocation);
