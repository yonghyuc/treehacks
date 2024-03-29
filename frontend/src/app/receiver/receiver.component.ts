/// <reference types="@types/googlemaps" />
import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {BackendSenderService} from "../service/backend-sender.service";

declare let google: any;

@Component({
  selector: 'app-receiver',
  templateUrl: './receiver.component.html',
  styleUrls: ['./receiver.component.scss']
})
export class ReceiverComponent implements AfterViewInit {
  map: google.maps.Map;
  marker: any;

  @ViewChild('googleMap') gmapElement: any;

  phone_number = "+13202887535";

  item: any;

  constructor(private backendSenderService: BackendSenderService) {
  }

  ngAfterViewInit() {
    this.backendSenderService.get("test").subscribe((item: any) => {
      this.item = item;
      this.setMap(item.location);
    });
  }

  setMap(location) {
    let googleLocation = new google.maps.LatLng(location.lat, location.lng);

    var mapProp = {
      center: googleLocation,
      zoom: 16,
      minZoom: 13,
      mapTypeId: google.maps.MapTypeId.HYBRID,
      zoomControl: true,
      mapTypeControl: false,
      scaleControl: false,
      streetViewControl: false,
      rotateControl: false,
      fullscreenControl: false
    };

    this.map = new google.maps.Map(this.gmapElement.nativeElement, mapProp);
    this.marker = new google.maps.Marker({ position: mapProp.center });
    this.marker.setMap(this.map);

    var infowindow = new google.maps.InfoWindow({
      content: "Mike is here"
    });
    infowindow.open(this.map, this.marker);

    this.showDangerousSpot(googleLocation);
  }

  showDangerousSpot(googleLocation){
    var heatmapData = [];

    heatmapData.push(googleLocation);

    new google.maps.visualization.HeatmapLayer({
      map: this.map,
      data: heatmapData,
      dissipating: false,
      radius: 0.0003
    });
  }

  sendMsg() {
    this.backendSenderService.get("test").subscribe((item) => {
      console.log(item);
    });
  }
}
