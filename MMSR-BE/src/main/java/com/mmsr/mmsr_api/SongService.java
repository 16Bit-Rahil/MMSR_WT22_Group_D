package com.mmsr.mmsr_api;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class SongService {
    private final SongRepository songRepository;
    private final SimilarSongsRepository similarSongsRepository;

    public SongService(SongRepository songRepository,SimilarSongsRepository similarSongsRepository) {
        this.songRepository = songRepository;
        this.similarSongsRepository = similarSongsRepository;
    }
    public Page<Song> getSongBySearchInput(String input,int page ,int pageSize){
        return this.songRepository.findSongsBySearchTerm(input, PageRequest.of(page,pageSize));
    }

    public Song getSongById(String id) {
        return this.songRepository.findSongById(id);
    }

    public Page<Song> getSimilarSongsForId(String id,int page, int pageSize){
        return this.similarSongsRepository.findAllById(id,PageRequest.of(page,pageSize));
    }
}
