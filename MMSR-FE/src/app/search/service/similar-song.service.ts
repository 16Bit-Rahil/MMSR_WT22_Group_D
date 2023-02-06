import {ContentChild, Injectable} from '@angular/core';
import {Song} from "../../model/song";
import {HttpClient, HttpParams} from "@angular/common/http";
import {APIModel} from "../../model/ApiModel";
import {
  BehaviorSubject,
  catchError,
  forkJoin,
  map,
  Observable,
  of,
  switchMap
} from "rxjs";
import { PageResponse } from 'src/app/model/page-response';

import {Track} from "../../model/TrackInfo";

@Injectable({
  providedIn: 'root'
})
export class SimilarSongService {

  readonly baseUrlSimilarSong = 'http://Springbackend-env.eba-y7r4njjq.eu-central-1.elasticbeanstalk.com/api/similar-song'

  private similarSongs$ = new BehaviorSubject<PageResponse<{trackInfo:Track | null,song:Song}>>({} as PageResponse<{trackInfo:Track,song:Song}>);

  constructor(private http: HttpClient) {}

  private getSimilarSongs$(id:string,page?:number){
    return this.http.get<PageResponse<Song>>(`${this.baseUrlSimilarSong}/${encodeURIComponent(id)}?page=${page ?? 0}&pageSize=10`).pipe(
      switchMap(page => {
        if(page.totalElements === 0) {
          return of({} as PageResponse<{trackInfo:Track,song:Song}>)
        }
        return this.getSongsWithTrackInfo(page.content).pipe(
          map(songs => ({...page,content: songs} as PageResponse<{trackInfo:Track,song:Song}>)))
      })
    )
  }

  getSimilarSongs(id: string){
    this.similarSongs$.next({} as PageResponse<{trackInfo:Track,song:Song}>);
    this.getSimilarSongs$(id).subscribe((page) => {
      this.similarSongs$.next(page)
    });

  }

  loadMore(id: string,page:number){
    this.getSimilarSongs$(id,page).subscribe({
      next:(resp) => {
          this.similarSongs$.next({
            ...resp,
            content: [...this.similarSongs$.value.content,...resp.content]
          });
      },
    })
  }

  getSimilarSongsPage(): Observable<PageResponse<{trackInfo:Track | null,song:Song}>>{
    return this.similarSongs$
  }


  private getSongWithTrackDetails(song: Song) {
    return forkJoin([
      this.getTrackInfo(song.songName,song.artist),
      this.getSongWithAlbumCover(song)
    ]).pipe(map(([track,song]) => ({trackInfo:track,song:song})));
  }

  private getSongWithAlbumCover(song: Song): Observable<Song>{
    return this.getAlbumCover(song.artist,song.albumName).pipe(
      map(val => ({...song,imgLink:val?.album.image[3]['#text']}))
    )
  }

  private getSongsWithTrackInfo(songs: Song[]): Observable<{trackInfo:Track,song:Song}[]>{
    return forkJoin<{trackInfo:Track,song:Song}[]>(songs.map( song =>
      this.getSongWithTrackDetails(song)
    ))
  }

  private getAlbumCover(artist:string, album_name:string):Observable<APIModel | null> {
    return this.http.get<APIModel>(encodeURI('https://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=76e37b8f0ca99ecb3d3a6ac4132dc0ef&artist='+artist.trim()+'&album='+ album_name.trim() +'&format=json')).pipe(
      catchError(err => of(null))
    )
  }
  // https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=76e37b8f0ca99ecb3d3a6ac4132dc0ef&artist=cher&track=believe&format=json
  private getTrackInfo(track:string, artist:string): Observable<Track> {
    return this.http.get<{track:Track}>(encodeURI('https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=76e37b8f0ca99ecb3d3a6ac4132dc0ef&artist='+artist.trim()+'&track='+ track.trim() +'&format=json')).pipe(
      map((resp:{track:Track}) => resp.track)
    );
  }
}
