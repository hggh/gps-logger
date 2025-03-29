import 'bootstrap/dist/css/bootstrap.min.css';
import 'leaflet/dist/leaflet.css';
import "./style.css";


import L, { icon } from "leaflet";
import * as bootstrap from "bootstrap";

document.addEventListener("DOMContentLoaded", function() {
    const device_pub_slug = document.getElementById("device_pub").dataset.slug;

    document.getElementById('map').style.height = window.innerHeight - 100 + "px";

    const map = L.map('map').setView([51.505, 10.09], 3);
    const tiles = L.tileLayer('https://tile.openstreetmap.de/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    var r = new XMLHttpRequest();
    r.open('GET', "/api/p/" +  device_pub_slug + "/geojson_track/");
    r.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    r.addEventListener('load', function(event) {
        if (r.status == 200) {
            var d = JSON.parse(r.responseText);
            var geojson = L.geoJSON(d, {style: function (feature) {
                return {
                    color: feature.properties.color,
                    weight: feature.properties.weight,
                    opacity: feature.properties.opacity,
                };
            }});
            geojson.addTo(map);
            map.fitBounds(geojson.getBounds())
        }
    });
    r.send();

    var l = new XMLHttpRequest();
    l.open('GET', "/api/p/" +  device_pub_slug + "/last_pos/");
    l.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    l.addEventListener('load', function(event) {
        if (l.status == 200) {
            var d = JSON.parse(l.responseText);

            L.marker(
                [d.lat, d.long],
                {
                    icon: L.icon({
                        iconUrl: '/static/marker.png',
                        iconSize:    [25, 41],
		                iconAnchor:  [12, 41],
		                popupAnchor: [1, -34],
		                tooltipAnchor: [16, -28],
		                shadowSize:  [41, 41]
                    })
                }
            ).addTo(map);
        }
    });
    l.send();
});
