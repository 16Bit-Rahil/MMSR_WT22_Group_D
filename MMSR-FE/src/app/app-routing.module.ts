import { NgModule } from '@angular/core';

import { Routes, RouterModule } from '@angular/router';
import {PageNotFoundComponent} from "./components/404/page-not-found.component";
import { SearchResultComponent } from './search/feature/search-result/search-result.component';
import { SongDetailPageComponent } from './search/feature/song-detail-page/song-detail-page.component';
import { HomeComponent } from './home/home.component';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'search-result/:searchTerm', component: SearchResultComponent},
  { path: 'song/:songId', component: SongDetailPageComponent},
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule { }
