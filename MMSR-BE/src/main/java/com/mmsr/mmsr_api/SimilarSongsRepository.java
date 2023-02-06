package com.mmsr.mmsr_api;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
@Repository
public interface SimilarSongsRepository extends JpaRepository<Song,String> {
    @Query(value = """
SELECT s.id, s.artist, s.song_name, s.album_name, s.youtube_link
FROM song s
JOIN ( SELECT unnest(ARRAY [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                          "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                          "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
                          "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
                          "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
                          "51", "52", "53", "54", "55", "56", "57", "58", "59", "60",
                          "61", "62", "63", "64", "65", "66", "67", "68", "69", "70",
                          "71", "72", "73", "74", "75", "76", "77", "78", "79", "80",
                          "81", "82", "83", "84", "85", "86", "87", "88", "89", "90",
                          "91", "92", "93", "94", "95", "96", "97", "98", "99"]) as similar_song_id
               FROM similar_songs
               WHERE id = ?1
               ) sim_songs
              ON s.id = sim_songs.similar_song_id
""",nativeQuery = true)
    Page<Song> findAllById(String id, Pageable pageable);

}
