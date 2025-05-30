package com.selimhorri.app.service.impl;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.web.client.RestTemplate;

import com.selimhorri.app.domain.Favourite;
import com.selimhorri.app.domain.id.FavouriteId;
import com.selimhorri.app.dto.FavouriteDto;
import com.selimhorri.app.dto.ProductDto;
import com.selimhorri.app.dto.UserDto;
import com.selimhorri.app.exception.wrapper.FavouriteNotFoundException;
import com.selimhorri.app.repository.FavouriteRepository;

@ExtendWith(MockitoExtension.class)
@DisplayName("FavouriteServiceImpl - Unit Tests")
class FavouriteServiceImplTest {

    @Mock
    private FavouriteRepository favouriteRepository;

    @Mock
    private RestTemplate restTemplate;

    @InjectMocks
    private FavouriteServiceImpl favouriteService;

    private Favourite testFavourite;
    private FavouriteDto testFavouriteDto;
    private FavouriteId testFavouriteId;
    private UserDto testUserDto;
    private ProductDto testProductDto;
    private LocalDateTime testLikeDate;

    @BeforeEach
    void setUp() {
        // Arrange - Configurar datos de prueba
        testLikeDate = LocalDateTime.now();

        testFavouriteId = new FavouriteId(1, 1, testLikeDate);

        testUserDto = UserDto.builder()
                .userId(1)
                .build();

        testProductDto = ProductDto.builder()
                .productId(1)
                .build();

        testFavourite = Favourite.builder()
                .userId(1)
                .productId(1)
                .likeDate(testLikeDate)
                .build();

        testFavouriteDto = FavouriteDto.builder()
                .userId(1)
                .productId(1)
                .likeDate(testLikeDate)
                .userDto(testUserDto)
                .productDto(testProductDto)
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando existen favoritos - Debe retornar lista de FavouriteDto")
    void findAll_WhenFavouritesExist_ShouldReturnFavouriteDtoList() {
        // Arrange
        List<Favourite> favourites = Arrays.asList(testFavourite);
        when(favouriteRepository.findAll()).thenReturn(favourites);
        when(restTemplate.getForObject(contains("user-service"), eq(UserDto.class))).thenReturn(testUserDto);
        when(restTemplate.getForObject(contains("product-service"), eq(ProductDto.class))).thenReturn(testProductDto);

        // Act
        List<FavouriteDto> result = favouriteService.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals(testFavourite.getUserId(), result.get(0).getUserId());
        assertEquals(testFavourite.getProductId(), result.get(0).getProductId());
        assertEquals(testFavourite.getLikeDate(), result.get(0).getLikeDate());
        verify(favouriteRepository, times(1)).findAll();
        verify(restTemplate, times(1)).getForObject(contains("user-service"), eq(UserDto.class));
        verify(restTemplate, times(1)).getForObject(contains("product-service"), eq(ProductDto.class));
    }

    @Test
    @DisplayName("findAll - Cuando no existen favoritos - Debe retornar lista vacía")
    void findAll_WhenNoFavouritesExist_ShouldReturnEmptyList() {
        // Arrange
        when(favouriteRepository.findAll()).thenReturn(Arrays.asList());

        // Act
        List<FavouriteDto> result = favouriteService.findAll();

        // Assert
        assertNotNull(result);
        assertTrue(result.isEmpty());
        verify(favouriteRepository, times(1)).findAll();
        verify(restTemplate, never()).getForObject(anyString(), eq(UserDto.class));
        verify(restTemplate, never()).getForObject(anyString(), eq(ProductDto.class));
    }

    @Test
    @DisplayName("findById - Cuando favorito existe - Debe retornar FavouriteDto")
    void findById_WhenFavouriteExists_ShouldReturnFavouriteDto() {
        // Arrange
        when(favouriteRepository.findById(testFavouriteId)).thenReturn(Optional.of(testFavourite));
        when(restTemplate.getForObject(contains("user-service"), eq(UserDto.class))).thenReturn(testUserDto);
        when(restTemplate.getForObject(contains("product-service"), eq(ProductDto.class))).thenReturn(testProductDto);

        // Act
        FavouriteDto result = favouriteService.findById(testFavouriteId);

        // Assert
        assertNotNull(result);
        assertEquals(testFavourite.getUserId(), result.getUserId());
        assertEquals(testFavourite.getProductId(), result.getProductId());
        assertEquals(testFavourite.getLikeDate(), result.getLikeDate());
        assertNotNull(result.getUserDto());
        assertNotNull(result.getProductDto());
        verify(favouriteRepository, times(1)).findById(testFavouriteId);
        verify(restTemplate, times(1)).getForObject(contains("user-service"), eq(UserDto.class));
        verify(restTemplate, times(1)).getForObject(contains("product-service"), eq(ProductDto.class));
    }

    @Test
    @DisplayName("findById - Cuando favorito no existe - Debe lanzar FavouriteNotFoundException")
    void findById_WhenFavouriteNotExists_ShouldThrowFavouriteNotFoundException() {
        // Arrange
        FavouriteId nonExistentId = new FavouriteId(999, 999, LocalDateTime.now());
        when(favouriteRepository.findById(nonExistentId)).thenReturn(Optional.empty());

        // Act & Assert
        FavouriteNotFoundException exception = assertThrows(
                FavouriteNotFoundException.class,
                () -> favouriteService.findById(nonExistentId));

        assertTrue(exception.getMessage().contains("Favourite with id:"));
        verify(favouriteRepository, times(1)).findById(nonExistentId);
        verify(restTemplate, never()).getForObject(anyString(), eq(UserDto.class));
        verify(restTemplate, never()).getForObject(anyString(), eq(ProductDto.class));
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar FavouriteDto")
    void save_WhenValidData_ShouldSaveAndReturnFavouriteDto() {
        // Arrange
        when(favouriteRepository.save(any(Favourite.class))).thenReturn(testFavourite);

        // Act
        FavouriteDto result = favouriteService.save(testFavouriteDto);

        // Assert
        assertNotNull(result);
        assertEquals(testFavourite.getUserId(), result.getUserId());
        assertEquals(testFavourite.getProductId(), result.getProductId());
        assertEquals(testFavourite.getLikeDate(), result.getLikeDate());
        verify(favouriteRepository, times(1)).save(any(Favourite.class));
    }

    @Test
    @DisplayName("save - Cuando usuario diferente - Debe guardar correctamente")
    void save_WhenDifferentUser_ShouldSaveCorrectly() {
        // Arrange
        FavouriteDto differentUserDto = FavouriteDto.builder()
                .userId(2)
                .productId(1)
                .likeDate(testLikeDate)
                .build();

        Favourite differentUserFavourite = Favourite.builder()
                .userId(2)
                .productId(1)
                .likeDate(testLikeDate)
                .build();

        when(favouriteRepository.save(any(Favourite.class))).thenReturn(differentUserFavourite);

        // Act
        FavouriteDto result = favouriteService.save(differentUserDto);

        // Assert
        assertNotNull(result);
        assertEquals(2, result.getUserId());
        assertEquals(1, result.getProductId());
        verify(favouriteRepository, times(1)).save(any(Favourite.class));
    }

    @Test
    @DisplayName("save - Cuando producto diferente - Debe guardar correctamente")
    void save_WhenDifferentProduct_ShouldSaveCorrectly() {
        // Arrange
        FavouriteDto differentProductDto = FavouriteDto.builder()
                .userId(1)
                .productId(2)
                .likeDate(testLikeDate)
                .build();

        Favourite differentProductFavourite = Favourite.builder()
                .userId(1)
                .productId(2)
                .likeDate(testLikeDate)
                .build();

        when(favouriteRepository.save(any(Favourite.class))).thenReturn(differentProductFavourite);

        // Act
        FavouriteDto result = favouriteService.save(differentProductDto);

        // Assert
        assertNotNull(result);
        assertEquals(1, result.getUserId());
        assertEquals(2, result.getProductId());
        verify(favouriteRepository, times(1)).save(any(Favourite.class));
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar FavouriteDto")
    void update_WhenValidData_ShouldUpdateAndReturnFavouriteDto() {
        // Arrange
        LocalDateTime newLikeDate = LocalDateTime.now().plusDays(1);
        testFavouriteDto.setLikeDate(newLikeDate);

        Favourite updatedFavourite = Favourite.builder()
                .userId(1)
                .productId(1)
                .likeDate(newLikeDate)
                .build();

        when(favouriteRepository.save(any(Favourite.class))).thenReturn(updatedFavourite);

        // Act
        FavouriteDto result = favouriteService.update(testFavouriteDto);

        // Assert
        assertNotNull(result);
        assertEquals(newLikeDate, result.getLikeDate());
        verify(favouriteRepository, times(1)).save(any(Favourite.class));
    }

    @Test
    @DisplayName("update - Cuando se actualiza fecha - Debe mantener otros campos")
    void update_WhenDateUpdated_ShouldKeepOtherFields() {
        // Arrange
        LocalDateTime newLikeDate = LocalDateTime.now().minusDays(1);
        FavouriteDto updateDto = FavouriteDto.builder()
                .userId(1)
                .productId(1)
                .likeDate(newLikeDate)
                .build();

        Favourite updatedFavourite = Favourite.builder()
                .userId(1)
                .productId(1)
                .likeDate(newLikeDate)
                .build();

        when(favouriteRepository.save(any(Favourite.class))).thenReturn(updatedFavourite);

        // Act
        FavouriteDto result = favouriteService.update(updateDto);

        // Assert
        assertNotNull(result);
        assertEquals(1, result.getUserId());
        assertEquals(1, result.getProductId());
        assertEquals(newLikeDate, result.getLikeDate());
        verify(favouriteRepository, times(1)).save(any(Favourite.class));
    }

    @Test
    @DisplayName("deleteById - Cuando favorito existe - Debe eliminar sin excepción")
    void deleteById_WhenFavouriteExists_ShouldDeleteWithoutException() {
        // Arrange
        doNothing().when(favouriteRepository).deleteById(testFavouriteId);

        // Act & Assert
        assertDoesNotThrow(() -> favouriteService.deleteById(testFavouriteId));
        verify(favouriteRepository, times(1)).deleteById(testFavouriteId);
    }

    @Test
    @DisplayName("deleteById - Cuando se intenta eliminar - Debe llamar al repositorio")
    void deleteById_WhenCalled_ShouldCallRepository() {
        // Arrange
        FavouriteId favouriteId = new FavouriteId(999, 999, LocalDateTime.now());
        doNothing().when(favouriteRepository).deleteById(favouriteId);

        // Act
        favouriteService.deleteById(favouriteId);

        // Assert
        verify(favouriteRepository, times(1)).deleteById(favouriteId);
    }
}
