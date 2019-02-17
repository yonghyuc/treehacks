import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable()
export class BackendSenderService {

  BACKEND_BASE_URL = "https://treehacks-mappal.appspot.com/";

  constructor(private http: HttpClient) {

  }

  get(url: string) {
    return this.http.get(this.BACKEND_BASE_URL + url);
  }
}
