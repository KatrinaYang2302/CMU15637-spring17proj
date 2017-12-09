
        var map;
        var start = null;
        var end = null;
        var startmarker = null;
        var endmarker = null;
        var directionsService;
        var directionsDisplay;
        var geocoder;
        var cityaddress = "Pittsburgh";
        var citymarker = null;
        var markerarray = [];
        var markerid = 0;
        var stopdetails = [];
        function initMap() {
      
          map = new google.maps.Map(document.getElementById('map'), {
              center: {lat: 40.4406247, lng: -79.9958864}, // pittsburgh
              zoom: 13
          });
          // set city-marker
          var image = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
            citymarker = new google.maps.Marker({
                position:{lat: 40.4406247, lng: -79.9958864},
                map: map,
                icon: image
            });
            map.panTo({lat: 40.4406247, lng: -79.9958864});
            // add click listener
          map.addListener('click', function(e) {
              placeMarkerAndPanTo(e.latLng);
          });
          directionsService = new google.maps.DirectionsService;
          directionsDisplay = new google.maps.DirectionsRenderer;
          directionsDisplay.setMap(map);
          //directionsDisplay.setPanel(document.getElementById('result-panel'));
          geocoder = new google.maps.Geocoder();
        }
        function placeMarkerAndPanTo(latLng) {
          var marker = new google.maps.Marker({
            position: latLng,
            map: map
          });
          map.panTo(latLng);
          var lstring = latLng.lat().toString()+latLng.lng().toString();
          markerarray[markerid]=marker;
          var infowindow = new google.maps.InfoWindow({
              content: '<p>latLng: '+latLng+'</p>' +'<button onclick="setClickStart('+latLng.lat().toString()+','+latLng.lng().toString()+','+markerid+')">Set as Origin</button>'+'<button onclick="setClickEnd('+latLng.lat().toString()+','+latLng.lng().toString()+','+markerid+')">Set as Destination</button>'+'<button onclick="removeMarker('+markerid+')">Remove Marker</button>'
          });
          markerid++;
          marker.addListener('click', function() {
              infowindow.open(marker.get('map'), marker);
          });
        }
        function calculateAndDisplayRoute(){
          var startaddress = document.getElementById('start').value;
          var endaddress = document.getElementById('end').value;
          if(startaddress == null || endaddress == null){
            document.getElementById("errortext").value = "invalid origin or destination";
            return;
          }
            setStart(); 
            setEnd();
          directionsService.route({
              origin: start,
              destination: end,
              travelMode: 'TRANSIT',
              transitOptions: {
            modes: ['BUS'],
            routingPreference: 'FEWER_TRANSFERS'  // LESS_WALKING
          }
          }, function(response, status) {
            if (status === 'OK') {
              directionsDisplay.setDirections(response);
              var rst='';
              var stepnum = 1;
              for(var i = 0;i<response.routes[0].legs.length;i++){
                var leg = response.routes[0].legs[i];
                for(var j = 0;j<leg.steps.length;j++){
                  var step = leg.steps[j];
                  rst+="Step "+stepnum++;
                  rst+=': '+step.instructions+'\n';
                  if(step.travel_mode == 'TRANSIT'){
                    var linename=step.transit.line.short_name;
                    var departurelatlng = step.transit.departure_stop.location;
                    var arrivallatlng = step.transit.arrival_stop.location;
                    var arrivetime = "hahahahahaha"; /// insert time-compute method
                    var busstring = "BusName: "+linename+'\n'+"DepartureStopName: "+step.transit.departure_stop.name+'\n'+"DepartureStopLatlng: "+departurelatlng+'\n'+"ArrivalStopName: "+step.transit.arrival_stop.name+'\n'+"ArrivalStopLatlng: "+arrivallatlng+'\n'+"BusArriveTime: "+arrivetime+'\n';
                    rst+=busstring;
                  }
                  rst+='\n';
                }
                rst+="leg\n";
              }
              document.getElementById('routeresult').value = rst;
            } 
            else {
              window.alert('Directions request failed due to ' + status);
            }
          });
        }
        function setCity() {
          cityaddress = document.getElementById('address').value;
          geocoder.geocode({'address': cityaddress}, function(results, status) {
            if (status === 'OK') {
              map.setCenter(results[0].geometry.location);
              map.setZoom(12);
              var image = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
              var marker = new google.maps.Marker({
                  position:results[0].geometry.location,
                  map: map,
                  icon: image
              });
              map.panTo(results[0].geometry.location);
              if(citymarker != null){
                  citymarker.setMap(null);
              }
              citymarker = marker;
           
            } 
            else {
              alert('Geocode was not successful for the following reason: ' + status);
            }
          });
        }
        function setStart(){
          var address = document.getElementById('start').value;
          if(address == "Current Location"){
            return;
          }
          geocoder.geocode({'address': address+cityaddress}, function(results, status) {
            if (status === 'OK') {
              map.setCenter(results[0].geometry.location);
              var id = markerid;
              placeMarkerAndPanTo(results[0].geometry.location);
              var marker = markerarray[id];
              start = results[0].geometry.location;
              if(startmarker != null && startmarker!= marker){
                  startmarker.setMap(null);
              }
              startmarker = marker;
           
            } 
            else {
              alert('Geocode was not successful for the following reason: ' + status);
            }
          }); 
        }
        function setEnd(){
          var address = document.getElementById('end').value;
          if(address == "Current Location"){
            return;
          }
          geocoder.geocode({'address': address+cityaddress}, function(results, status) {
            if (status === 'OK') {
              var id = markerid;
              placeMarkerAndPanTo(results[0].geometry.location);
              var marker = markerarray[id];
              end = results[0].geometry.location;
              if(endmarker != null && endmarker!=marker){
                  endmarker.setMap(null);
              }
              endmarker = marker;  
            } 
            else {
              alert('Geocode was not successful for the following reason: ' + status);
            }
          });
        }
        function setClickStart(lat,lng,id){
          var latLng = new google.maps.LatLng(parseFloat(lat), parseFloat(lng));
          var lstring = lat+lng;
          var marker = markerarray[id];
          geocoder.geocode({'location': latLng}, function(results, status) {
              if (status === 'OK') {
                  if (results[1]) {
                    document.getElementById("start").value=results[1].formatted_address;
                    start = latLng;
                    if(startmarker != null && startmarker != marker){
                          startmarker.setMap(null);
                      }
                      startmarker = marker;
                      if(end != null){
                        calculateAndDisplayRoute();
                      }
                  } 
                  else {
                    window.alert('No results found');
                  }
              } 
              else {
                  window.alert('Geocoder failed due to: ' + status);
              }
          });
        }
        function setClickEnd(lat,lng,id){
          var latLng = new google.maps.LatLng(parseFloat(lat), parseFloat(lng));
          var lstring = lat+lng;
          var marker = markerarray[id];
          geocoder.geocode({'location': latLng}, function(results, status) {
              if (status === 'OK') {
                  if (results[1]) {
                    document.getElementById("end").value=results[1].formatted_address;
                    end = latLng;
                    if(endmarker != null && endmarker != marker){
                          endmarker.setMap(null);
                      }
                      endmarker = marker;
                      if(start != null){
                        calculateAndDisplayRoute();
                      }
                  } 
                  else {
                    window.alert('No results found');
                  }
              } 
              else {
                  window.alert('Geocoder failed due to: ' + status);
              }
          });
        }
        function removeMarker(id){
          var marker = markerarray[id];
          marker.setMap(null);
        }
        function getLocation(flag) {
        if (navigator.geolocation) {
          if(flag == 0){
                navigator.geolocation.getCurrentPosition(setCurrStart, showCurrError);
          }
          else if (flag == 1){
            navigator.geolocation.getCurrentPosition(setCurrEnd, showCurrError);
          }
          } 
          else {
          x.innerHTML = "Geolocation is not supported by this browser.";
        }
      }
      function setCurrStart(position) {
        var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        map.setCenter(latlng);
            var id = markerid;
            placeMarkerAndPanTo(latlng);
            var marker = markerarray[id];
            start = latlng;
            if(startmarker != null && startmarker!=null){
                startmarker.setMap(null);
            }
            startmarker = marker;
            document.getElementById("start").value = "Current Location";
    }
    function setCurrEnd(position) {
      var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            var id = markerid;
            placeMarkerAndPanTo(latlng);
            var marker = markerarray[id];
            end = latlng;
            if(endmarker != null && endmarker!=marker){
                endmarker.setMap(null);
            }
            endmarker = marker;
            document.getElementById("end").value = "Current Location";
    }
    function showCurrError(error) {
      var errorString;
        switch(error.code) {
            case error.PERMISSION_DENIED:
                errorString = "User denied the request for Geolocation."
              break;
            case error.POSITION_UNAVAILABLE:
                errorString = "Location information is unavailable."
              break;
            case error.TIMEOUT:
                errorString = "The request to get user location timed out."
              break;
            case error.UNKNOWN_ERROR:
                errorString = "An unknown error occurred."
              break;
        }
        document.getElementById("errortext").value = errorString;
    }