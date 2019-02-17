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

  constructor(private backendSenderService: BackendSenderService) {
  }

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
    var marker = new google.maps.Marker({ position: mapProp.center });
    marker.setMap(this.map);

    var infowindow = new google.maps.InfoWindow({
      content: "Hey, We are here"
    });
    infowindow.open(this.map, marker);
  }

  sendMsg() {
    this.backendSenderService.get("test").subscribe((item) => {
      console.log(item);
    });
  }


}
