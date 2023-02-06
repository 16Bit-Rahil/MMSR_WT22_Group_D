package com.mmsr.mmsr_api;

import org.springframework.data.domain.Page;
import org.springframework.web.bind.annotation.*;

import java.util.List;

//@CrossOrigin(origins = "http://frontend-client.s3-website.eu-central-1.amazonaws.com")
@CrossOrigin(origins = "http://localhost:4200")
@RestController
public class SongController {

    private final SongService songService;

    public SongController(SongService songService) {
        this.songService = songService;
    }


    @GetMapping("api/songs")
    Page<Song> searchSong(@RequestParam String search,
                          @RequestParam Integer page,
                          @RequestParam Integer pageSize) {
        System.out.println(search);
        return songService.getSongBySearchInput(search,page,pageSize);
    }

    @GetMapping("api/song/{id}")
    public Song getSongById(@PathVariable String id){
        return songService.getSongById(id);
    }

    @GetMapping("api/similar-song/{id}")
    Page<Song> getSimilarSongsForId(@PathVariable String id,
                          @RequestParam Integer page,
                          @RequestParam Integer pageSize) {
        System.out.println(id);
        return songService.getSimilarSongsForId(id,page,pageSize);
    }
}
