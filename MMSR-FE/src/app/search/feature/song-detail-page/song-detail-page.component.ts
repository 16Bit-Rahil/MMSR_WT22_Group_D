import {Component, OnInit, Renderer2} from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchService } from '../../service/search.service';
import {ActivatedRoute, Router, RouterModule} from "@angular/router";
import {NbButtonModule, NbIconModule, NbLayoutModule} from "@nebular/theme";
import {Song} from "../../../model/song";
import {Track} from "../../../model/TrackInfo";
import { BehaviorSubject } from 'rxjs';
import {YouTubePlayerModule} from "@angular/youtube-player";
import {YtPlayerComponent} from "./yt-player/yt-player.component";
import {SimilarSongService} from "../../service/similar-song.service";

@Component({
  selector: 'app-song-detail-page',
  standalone: true,
  imports: [CommonModule, NbLayoutModule, YouTubePlayerModule, YtPlayerComponent, NbButtonModule, RouterModule, NbIconModule],
  templateUrl: './song-detail-page.component.html',
  styleUrls: ['./song-detail-page.component.css']
})
export class SongDetailPageComponent implements OnInit {

  songId!: string;
  detailsData = new BehaviorSubject<{song: Song, trackInfo: Track} | null>(null);
  similarSongs = this.similarSongService.getSimilarSongsPage();

  private apiLoaded: boolean = false;
  private currentPage: number = 0;
  constructor(public searchService: SearchService, private similarSongService: SimilarSongService,
              private route: ActivatedRoute, private router: Router) { }
  ngOnInit(): void {
    this.songId = this.route.snapshot.params['songId'];
    if (!this.apiLoaded) {
      const tag = document.createElement('script');
      tag.src = 'https://www.youtube.com/iframe_api';
      document.body.appendChild(tag);
      this.apiLoaded = true;
    }
    this.searchService.getSongAndTrackDetailById(this.songId).subscribe(resp =>{

      console.log(resp.trackInfo);
      console.log(resp)
      this.detailsData.next(resp)
    })

    this.similarSongService.getSimilarSongs(this.songId);
  }


  loadMore(){
    this.currentPage++;
    this.similarSongService.loadMore(this.songId,this.currentPage)
  }


  //https://www.youtube.com/watch?v=JGwWNGJdvx8
  getYoutubeId(link: string) {
    return link.substring(32, link.length);
  }

  setDefaultCover(song:Song) {
    song.imgLink = 'http://www.scottishculture.org/themes/scottishculture/images/music_placeholder.png';
  }

  getSummary(summary: string | undefined) {
    let idx = summary?.indexOf('<');
    return summary?.substring(0, idx);
  }

  navigate(id: string) {
    this.router.navigate(['/song/' + id]).then(r => window.location.reload());

  }
}
