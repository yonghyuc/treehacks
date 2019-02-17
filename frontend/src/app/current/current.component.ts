/// <reference types="@types/googlemaps" />
import {AfterViewInit, Component, ViewChild} from '@angular/core';

declare let google: any;

@Component({
  selector: 'app-current',
  templateUrl: './current.component.html',
  styleUrls: ['./current.component.scss']
})
export class CurrentComponent implements AfterViewInit {
  map: google.maps.Map;
  marker;
  autocomplete;

  @ViewChild('googleMap') gmapElement: any;
  @ViewChild('search') searchElement: any;

  ngAfterViewInit() {
    var mapProp = {
      center: new google.maps.LatLng(28.4595, 77.0266),
      zoom: 14,
      // mapTypeId: google.maps.MapTypeId.ROADMAP
      mapTypeId: google.maps.MapTypeId.HYBRID
      // mapTypeId: google.maps.MapTypeId.SATELLITE
      // mapTypeId: google.maps.MapTypeId.TERRAIN
    };

    this.map = new google.maps.Map(this.gmapElement.nativeElement, mapProp);
    this.marker = new google.maps.Marker({ position: mapProp.center });
    this.marker.setMap(this.map);

    this.autocomplete = new google.maps.places.Autocomplete(this.searchElement.nativeElement);

    this.autocomplete.bindTo('bounds', this.map);

    // Set the data fields to return when the user selects a place.
    this.autocomplete.set("Fields", ['address_components', 'geometry', 'icon', 'name']);

    this.autocomplete.addListener('place_changed', this.changeLocation.bind(this));
  }

  private changeLocation () {
    this.marker.setVisible(false);
    let place = this.autocomplete.getPlace();
    if (!place.geometry) {
      // User entered the name of a Place that was not suggested and
      // pressed the Enter key, or the Place Details request failed.
      window.alert("No details available for input: '" + place.name + "'");
      return;
    }

    // If the place has a geometry, then present it on a map.
    if (place.geometry.viewport) {
      this.map.fitBounds(place.geometry.viewport);
    } else {
      this.map.setCenter(place.geometry.location);
      this.map.setZoom(17);  // Why 17? Because it looks good.
    }
    this.marker.setPosition(place.geometry.location);
    this.marker.setVisible(true);
  }
}
