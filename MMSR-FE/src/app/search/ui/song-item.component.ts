import {Component, Input, OnInit} from '@angular/core';
import {__core_private_testing_placeholder__} from '@angular/core/testing';
import {Song} from 'src/app/model/song';

@Component({
  selector: 'song-item',
  template: `
    <nb-card>
      <nb-card-header class="header">
        <img [src]="song.imgLink" (error)="setDefaultCover()">
      </nb-card-header>
      <nb-card-body>
        <div class="song-content">
          <div class="song-title">{{song.songName}}</div>
          <div class="song-artist">{{song.artist}}</div>
          <div class="song-release">{{song.albumName}}</div>
        </div>
      </nb-card-body>
      <nb-card-footer>
        <button [routerLink]="['/','song',song.id]" nbButton>Details</button>
      </nb-card-footer>
    </nb-card>
  `,
  styleUrls: ['./song-item.component.css'],
})

export class SongItemComponent implements OnInit {
  @Input() song!: Song;

  constructor() {
  }

  ngOnInit() {
  }


  setDefaultCover() {
    this.song.imgLink = 'http://www.scottishculture.org/themes/scottishculture/images/music_placeholder.png';
  }
}
