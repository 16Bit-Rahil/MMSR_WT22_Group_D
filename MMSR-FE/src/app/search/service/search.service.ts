import {Injectable} from '@angular/core';
import {Song} from "../../model/song";
import {HttpClient} from "@angular/common/http";
import {APIModel} from "../../model/ApiModel";
import {BehaviorSubject, forkJoin, map, Observable, of, switchMap} from "rxjs";
import { PageResponse } from 'src/app/model/page-response';
import { Router } from '@angular/router';
import {Track} from "../../model/TrackInfo";

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  readonly baseUrlSongs = 'http://Springbackend-env.eba-y7r4njjq.eu-central-1.elasticbeanstalk.com/api/songs'
  readonly baseUrlSong = 'http://Springbackend-env.eba-y7r4njjq.eu-central-1.elasticbeanstalk.com/api/song'

  private searchResult$ = new BehaviorSubject<PageResponse<Song>>({} as PageResponse<Song>);

  constructor(private http: HttpClient,
    private router:Router) {}

  private search$(term:string,page?:number){
    return this.http.get<PageResponse<Song>>(`${this.baseUrlSongs}?search=${encodeURIComponent(term)}&page=${page ?? 0}&pageSize=10`).pipe(
      switchMap(page => {
        if(page.totalElements === 0) {
          return of(page)
        }
        return this.getSongsWithAlbumCover(page.content).pipe(
          map(songs => ({...page,content: songs} as PageResponse<Song>)))
      })
    )
  }

  search(term: string){
    this.searchResult$.next({} as PageResponse<Song>);
    this.search$(term).subscribe((page) => {
      this.searchResult$.next(page)
      this.router.navigate(['search-result',term])
    });

  }

  loadMore(term: string,page:number){
    this.search$(term,page).subscribe({
      next:(resp) => {
          this.searchResult$.next({
            ...resp,
            content: [...this.searchResult$.value!.content,...resp.content]
          });
      },
    })
  }
  getSearchResult(): Observable<PageResponse<Song> | null>{
    return this.searchResult$
  }


  getSongAndTrackDetailById(id: string): Observable<{trackInfo:Track,song:Song}> {
    return this.http.get<Song>(`${this.baseUrlSong}/${encodeURIComponent(id)}`).pipe(
      switchMap(song => {
        return forkJoin({
          trackInfo:this.getTrackInfo(song.songName,song.artist),
          song:this.getSongWithAlbumCover(song)})
      })
    );
  }

  private getSongsWithAlbumCover(songs: Song[]): Observable<Song[]>{
    return forkJoin<Song[]>(songs.map( song =>
      this.getAlbumCover(song.artist,song.albumName).pipe(
        map(val => ({...song,imgLink:val.album.image[3]['#text']}))
      )
    ))
  }

  private getSongWithAlbumCover(song: Song): Observable<Song>{
    return this.getAlbumCover(song.artist,song.albumName).pipe(
        map(val => ({...song,imgLink:val.album.image[3]['#text']}))
      )
  }


  private getAlbumCover(artist:string, album_name:string) {
    return this.http.get<APIModel>(encodeURI('https://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=76e37b8f0ca99ecb3d3a6ac4132dc0ef&artist='+artist.trim()+'&album='+ album_name.trim() +'&format=json'))
  }

  // https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=76e37b8f0ca99ecb3d3a6ac4132dc0ef&artist=cher&track=believe&format=json
  private getTrackInfo(track:string, artist:string): Observable<Track> {
    return this.http.get<{track:Track}>(encodeURI('https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=76e37b8f0ca99ecb3d3a6ac4132dc0ef&artist='+artist.trim()+'&track='+ track.trim() +'&format=json')).pipe(
      map((resp:{track:Track}) => resp.track)
    );
  }
}
