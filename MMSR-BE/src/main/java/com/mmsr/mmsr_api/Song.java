package com.mmsr.mmsr_api;

import jakarta.annotation.Nullable;
import jakarta.persistence.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

@Entity
@Table(name="song")
public class Song {
    @Id
    private String id;
    private String artist;
    @Column(name = "song_name")
    private String songName;
    @Column(name = "album_name")
    private String albumName;

    @Nullable
    @Column(name = "youtube_link")
    private String youtubeLink;

    public Song(String id, String artist, String songName, String albumName, String youtubeLink) {
        this.id = id;
        this.artist = artist;
        this.songName = songName;
        this.albumName = albumName;
        this.youtubeLink = youtubeLink;
    }

    public Song() {

    }

    public void setId(String id) {
        this.id = id;
    }

    public void setArtist(String artist) {
        this.artist = artist;
    }

    public void setSongName(String songName) {
        this.songName = songName;
    }

    public void setAlbumName(String albumName) {
        this.albumName = albumName;
    }

    public void setYoutubeLink(String youtubeLink) {
        this.youtubeLink = youtubeLink;
    }
    public String getId() {
        return id;
    }

    public String getArtist() {
        return artist;
    }

    public String getSongName() {
        return songName;
    }

    public String getAlbumName() {
        return albumName;
    }

    public String getYoutubeLink() {
        return youtubeLink;
    }
    @Override
    public String toString() {
        return "Song{" +
                "id='" + id + '\'' +
                ", artist='" + artist + '\'' +
                ", songName='" + songName + '\'' +
                ", albumName='" + albumName + '\'' +
                ", youtubeLink='" + youtubeLink + '\'' +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Song song = (Song) o;
        return Objects.equals(id, song.id) && Objects.equals(artist, song.artist) && Objects.equals(songName, song.songName) && Objects.equals(albumName, song.albumName) && Objects.equals(youtubeLink, song.youtubeLink);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, artist, songName, albumName, youtubeLink);
    }
}
