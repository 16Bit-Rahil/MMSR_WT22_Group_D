export interface Track {
  name: string
  url: string
  duration: string
  streamable: Streamable
  listeners: string
  playcount: string
  artist: Artist
  album: Album
  toptags: Toptags
  wiki: Wiki
}

export interface Streamable {
  "#text": string
  fulltrack: string
}

export interface Artist {
  name: string
  url: string
}

export interface Album {
  artist: string
  title: string
  url: string
  image: Image[]
}

export interface Image {
  "#text": string
  size: string
}

export interface Toptags {
  tag: Tag[]
}

export interface Tag {
  name: string
  url: string
}

export interface Wiki {
  published: string
  summary: string
  content: string
}
