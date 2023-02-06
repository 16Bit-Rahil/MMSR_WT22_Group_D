//package com.mmsr.mmsr_api;
//
//import org.junit.ClassRule;
//import org.junit.jupiter.api.BeforeAll;
//import org.junit.jupiter.api.Test;
//import org.junit.runner.RunWith;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
//import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
//import org.springframework.boot.test.util.TestPropertyValues;
//import org.springframework.context.ApplicationContextInitializer;
//import org.springframework.context.ConfigurableApplicationContext;
//import org.springframework.data.domain.PageRequest;
//import org.springframework.data.domain.Pageable;
//import org.springframework.test.context.ContextConfiguration;
//import org.springframework.test.context.junit4.SpringRunner;
//import org.testcontainers.containers.BindMode;
//import org.testcontainers.containers.PostgreSQLContainer;
//import org.testcontainers.junit.jupiter.Testcontainers;
//
//import java.util.List;
//import java.util.Optional;
//
//import static org.assertj.core.api.Assertions.assertThat;
//
//@Testcontainers
//@RunWith(SpringRunner.class)
//@DataJpaTest
//@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
//@ContextConfiguration(initializers = {SongRepositoryContainerTest.Initializer.class})
//class SongRepositoryContainerTest {
//
//    @ClassRule
//    static PostgreSQLContainer postgreSQLContainer = new PostgreSQLContainer<>("postgres")
//            .withDatabaseName("postgres")
//            .withUsername("postgres")
//            .withPassword("postgres")
//            .withFileSystemBind("db-container/songs_mmsr_input.sql", "/docker-entrypoint-initdb.d/songs_mmsr_input.sql",
//                    BindMode.READ_ONLY)
//            .withFileSystemBind("db-container/update_links.sql", "/docker-entrypoint-initdb.d/update_links.sql",
//                    BindMode.READ_ONLY)
//            .withFileSystemBind("db-container/similar_songs.sql", "/docker-entrypoint-initdb.d/similar_songs.sql",
//                    BindMode.READ_ONLY)
//            .withReuse(true);
//
//    @BeforeAll
//    static void startContainer(){
//        postgreSQLContainer.start();
//    }
//
//    static class Initializer
//            implements ApplicationContextInitializer<ConfigurableApplicationContext> {
//        public void initialize(ConfigurableApplicationContext configurableApplicationContext) {
//            TestPropertyValues.of(
//                    "spring.datasource.url=" + postgreSQLContainer.getJdbcUrl(),
//                    "spring.datasource.username=" + postgreSQLContainer.getUsername(),
//                    "spring.datasource.password=" + postgreSQLContainer.getUsername()
//            ).applyTo(configurableApplicationContext.getEnvironment());
//        }
//    }
//    @Autowired SongRepository songRepository;
//    @Autowired SimilarSongsRepository similarSongsRepository;
//
//    @Test
//    void getSongById(){
//        String songId = "zzznMjZAKnJJXQSj";
//        Optional<Song> oDuaLipaSong =  songRepository.findById(songId);
//        assertThat(oDuaLipaSong).isNotEmpty();
//        assertThat(oDuaLipaSong.get().getSongName()).isNotBlank();
//        assertThat(oDuaLipaSong.get().getYoutubeLink()).isNotBlank();
//        assertThat(oDuaLipaSong.get().getAlbumName()).isNotBlank();
//        assertThat(oDuaLipaSong.get().getArtist()).isNotBlank();
//        assertThat(oDuaLipaSong.get().getId()).isEqualTo(songId);
//    }
//
//    @Test
//    void getSongBySearchTerm(){
//        String searchTerm = "Dua Lipa";
//        Pageable pageable = PageRequest.of(0,20);
//        Song songShouldBeThere = new Song(
//                "m3bU7wEiG8i3QgLU",
//                "Dua Lipa",
//                "New Rules - Initial Talk Remix",
//                "New Rules (Initial Talk Remix)",
//                "https://www.youtube.com/watch?v=wLjNTTCVat0");
//
//        List<Song> result = songRepository.findSongsBySearchTerm(searchTerm,pageable);
//
//        assertThat(result).isNotEmpty();
//        assertThat(result).contains(songShouldBeThere);
//    }
//
//    @Test
//    void getSimilarSongsDetailsFromZeroToTen(){
//        Pageable pageable = PageRequest.of(0,10);
//        Song firstSongFromPageable = new Song(
//                "m3bU7wEiG8i3QgLU",
//                "Dua Lipa",
//                "New Rules - Initial Talk Remix",
//                "New Rules (Initial Talk Remix)",
//                "https://www.youtube.com/watch?v=wLjNTTCVat0");
//
//
//        List<Song> songs = similarSongsRepository.findAllById("zzznMjZAKnJJXQSj",pageable);
//
//        assertThat(songs.size()).isEqualTo(10);
//        assertThat(songs.get(0)).isEqualTo(firstSongFromPageable);
//    }
//
//}