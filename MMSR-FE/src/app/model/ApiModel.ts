export interface APIModel {
  album: Album;
}

export interface Album {
  artist:    string;
  mbid:      string;
  tags:      Tags;
  name:      string;
  image:     Image[];
  tracks:    Tracks;
  listeners: string;
  playcount: string;
  url:       string;
}

export interface Image {
  size:    string;
  "#text": string;
}

export interface Tags {
  tag: Tag[];
}

export interface Tag {
  url:  string;
  name: string;
}

export interface Tracks {
  track: Track[];
}

export interface Track {
  streamable: Streamable;
  duration:   number;
  url:        string;
  name:       string;
  "@attr":    Attr;
  artist:     Artist;
}

export interface Attr {
  rank: number;
}

export interface Artist {
  url:  string;
  name: string;
  mbid: string;
}

export interface Streamable {
  fulltrack: string;
  "#text":   string;
}
