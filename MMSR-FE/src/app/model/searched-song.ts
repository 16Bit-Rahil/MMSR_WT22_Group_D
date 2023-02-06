export class SearchedSong {
  id: string;
  similarSongs:string[]

  constructor(id:string, similarSongs:string[]) {
    this.id = id;
    this.similarSongs = similarSongs;
  }
}
