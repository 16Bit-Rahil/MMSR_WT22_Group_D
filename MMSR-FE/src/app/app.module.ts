import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {NbThemeModule, NbLayoutModule, NbSearchModule, NbCardModule, NbButtonModule,NbListModule, NbSpinnerModule} from '@nebular/theme';
import { NbEvaIconsModule } from '@nebular/eva-icons';
import { AppRoutingModule } from './app-routing.module';
import { PageNotFoundComponent } from './components/404/page-not-found.component';
import {HttpClientModule} from "@angular/common/http";
import { SearchResultComponent } from './search/feature/search-result/search-result.component';
import { SongItemComponent } from './search/ui/song-item.component';
import { SearchHeaderComponent } from "./search/feature/search-header/search-header.component";
import { HomeComponent } from './home/home.component';
import {YouTubePlayerModule} from "@angular/youtube-player";

@NgModule({
  declarations: [
    AppComponent,
    PageNotFoundComponent,
    SearchResultComponent,
    SongItemComponent,
  ],
  providers: [],
  bootstrap: [AppComponent],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    NbThemeModule.forRoot({name: 'default'}),
    NbLayoutModule,
    NbEvaIconsModule,
    AppRoutingModule,
    NbCardModule,
    NbButtonModule,
    HttpClientModule,
    NbListModule,
    SearchHeaderComponent,
    HomeComponent,
    NbSpinnerModule,
    YouTubePlayerModule
  ]
})
export class AppModule { }
