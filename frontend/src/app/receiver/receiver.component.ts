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

  @ViewChild('googleMap') gmapElement: any;

  phone_number = "+13234960810"

  constructor(private backendSenderService: BackendSenderService) {
  }

  ngAfterViewInit() {
    var mapProp = {
      center: new google.maps.LatLng(28.4595, 77.0266),
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
    var marker = new google.maps.Marker({ position: mapProp.center });
    marker.setMap(this.map);

    var infowindow = new google.maps.InfoWindow({
      content: "Hey, We are here"
    });
    infowindow.open(this.map, marker);

    this.showDangerousSpot();
  }

  showDangerousSpot(){
    var heatmapData = [];

    var latLng = new google.maps.LatLng(28.4595, 77.0266);
    heatmapData.push(latLng);

    var heatmap = new google.maps.visualization.HeatmapLayer({
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
