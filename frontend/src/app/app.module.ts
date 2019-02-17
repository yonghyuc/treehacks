import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {ReceiverComponent} from './receiver/receiver.component';
import {RouterModule, Routes} from "@angular/router";
import {CurrentComponent} from './current/current.component';
import {StatusComponent} from './status/status.component';
import {HttpClientModule} from "@angular/common/http";
import {BackendSenderService} from "./service/backend-sender.service";

const appRoutes: Routes = [
  { path: 'receive', component: ReceiverComponent },
  { path: 'current', component: CurrentComponent },
  { path: 'status', component: StatusComponent },
  { path: '', redirectTo: '/index.html', pathMatch: 'full' }
];


@NgModule({
  declarations: [
    AppComponent,
    ReceiverComponent,
    CurrentComponent,
    StatusComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RouterModule.forRoot(
      appRoutes,
      { enableTracing: true } // <-- debugging purposes only
    ),
    HttpClientModule
  ],
  providers: [
    BackendSenderService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
