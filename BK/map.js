var southWest = L.latLng(20.859955, 125.293614),
    northEast = L.latLng(46.049957, 154.463614),
    bounds = L.latLngBounds(southWest, northEast);

var map = L.map('map', {
    maxBounds: bounds,
    attributionControl: false 
}).setView([38.964957,140.378614], 5);
var title=L.tileLayer('https://api.maptiler.com/maps/jp-mierune-gray/256/{z}/{x}/{y}.png?key=bvtEzFAeFqFUNkDetfaA', {
    maxZoom: 15,
    minZoom:5,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

L.geoJson(japan).addTo(map);
var markericon=L.icon({
  iconUrl:'素材/icons8-visit-50.png',
  popupAnchor:[25,0]
});

var markers = [];

    var openPopupMarker = null;
    for (var i = 0; i < locations.length; i++) {
        (function() {
            var location = locations[i];
            var marker = L.marker(location.latlng,{ icon: markericon });

            markers.push(marker);

            marker.on('click', function() {
                if (openPopupMarker === this) {
                    this.closePopup();
                    openPopupMarker = null;
                } else {
                    if (openPopupMarker) {
                        openPopupMarker.closePopup();
                    }
                    openPopupMarker = this;

                    var popupContent = "<h3 style='font-weight:bold'>" + location.name + "</h3>" +
                                    (location.option?"<p style='font-size:18px;font-weight:bold;'>"+location.option+"</p>":'')
                                    +"<img src='" + location.photo + "' alt='" + location.name + "' style='width:300px; height: 150px;'>"
                                  ;

                    this.bindPopup(popupContent,{
                      maxWidth:300,
                      minWidth:300,
                      minHeight:200,
                    }).openPopup();
                }
            });
        })();
    }

    map.on('zoomend', function() {
        var currentZoom = map.getZoom();

    
        if (currentZoom > 9) {
           
            for (var i = 0; i < markers.length; i++) {
                markers[i].addTo(map);
            }
            
        } else {
      
            for (var i = 0; i < markers.length; i++) {
                map.removeLayer(markers[i]);
            }
        }
    });

    function getcolor(d){
        switch(d){
          case '北海道':
            return '#33a8c7';
          case '東北地區':
            return '#52e3e1';
          case '關東地區':
            return '#a0e426';  
          case '中部地區':
            return '#e79580';
          case '近畿地區':
            return '#fdf148';
          case '中國地區':
            return '#ffab00';
          case '四國地區':
            return '#f77976';
          case '九州地區':
            return '#f050ae';
          case '沖繩地區':
            return '#9336fd';
         
        }
      }

function style(feature){
    return{
        fillColor:getcolor(feature.properties.area),
        weight: 2.5,
        opacity: 0.8,
        color:'#b89e14',
        dashArray:'3',
        fillOpacity: 0.5
    };

};

L.geoJson(japan,{style: style}).addTo(map);

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.6
    });
    info.update(layer.feature.properties);
    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}

var geojson;
geojson = L.geoJson(japan);

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
    
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover:highlightFeature,
        mouseout:resetHighlight,
        click:zoomToFeature
    });
}

geojson = L.geoJson(japan, {
    style: style,
    onEachFeature:onEachFeature
}).addTo(map);

var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); 
    this.update();
    return this._div;
};


info.update = function (props) {
    this._div.innerHTML = '<h4>日本行政區</h4>' +  (props ?'<span>地區:'+props.area+'</span><br />'+
        '<span>行政區:'+'<b>' + props.nam_ja + '</span></b><br /><span>' + props.nam +'</span>'+'<br />'
        : 'Hover over a state');
};

info.addTo(map);