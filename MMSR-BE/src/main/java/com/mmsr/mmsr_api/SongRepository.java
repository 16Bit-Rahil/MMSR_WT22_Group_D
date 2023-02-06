package com.mmsr.mmsr_api;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface SongRepository extends JpaRepository<Song, String> {
    @Query("""
            SELECT s
            FROM Song s WHERE s.songName iLIKE ?1% OR s.artist iLIKE ?1% OR s.albumName iLIKE ?1%
            """)
    Page<Song> findSongsBySearchTerm(String search, Pageable pageable);

    Song findSongById(String id);


}


