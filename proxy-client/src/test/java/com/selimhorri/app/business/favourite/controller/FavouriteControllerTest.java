package com.selimhorri.app.business.favourite.controller;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.time.LocalDateTime;
import java.util.Arrays;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.ResponseEntity;

import com.selimhorri.app.business.favourite.model.FavouriteDto;
import com.selimhorri.app.business.favourite.model.response.FavouriteFavouriteServiceCollectionDtoResponse;
import com.selimhorri.app.business.favourite.service.FavouriteClientService;

@ExtendWith(MockitoExtension.class)
@DisplayName("FavouriteController - Unit Tests")
class FavouriteControllerTest {

    @Mock
    private FavouriteClientService favouriteClientService;

    @InjectMocks
    private FavouriteController favouriteController;

    private FavouriteDto testFavouriteDto;
    private FavouriteFavouriteServiceCollectionDtoResponse testCollectionResponse;

    @BeforeEach
    void setUp() {
        testFavouriteDto = FavouriteDto.builder()
                .userId(1)
                .productId(2)
                .likeDate(LocalDateTime.now())
                .build();

        testCollectionResponse = FavouriteFavouriteServiceCollectionDtoResponse.builder()
                .collection(Arrays.asList(testFavouriteDto))
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando servicio retorna favoritos - Debe retornar colección de favoritos")
    void findAll_WhenServiceReturnsFavourites_ShouldReturnFavouriteCollection() {
        // Arrange
        ResponseEntity<FavouriteFavouriteServiceCollectionDtoResponse> serviceResponse = 
                ResponseEntity.ok(testCollectionResponse);
        when(favouriteClientService.findAll()).thenReturn(serviceResponse);

        // Act
        ResponseEntity<FavouriteFavouriteServiceCollectionDtoResponse> result = favouriteController.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertNotNull(result.getBody());
        assertEquals(1, result.getBody().getCollection().size());
        verify(favouriteClientService, times(1)).findAll();
    }

    @Test
    @DisplayName("findById - Cuando favorito existe - Debe retornar favorito")
    void findById_WhenFavouriteExists_ShouldReturnFavourite() {
        // Arrange
        String userId = "1";
        String productId = "2";
        String likeDate = "2024-01-01 10:00:00";
        ResponseEntity<FavouriteDto> serviceResponse = ResponseEntity.ok(testFavouriteDto);
        when(favouriteClientService.findById(userId, productId, likeDate)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<FavouriteDto> result = favouriteController.findById(userId, productId, likeDate);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals(1, result.getBody().getUserId());
        assertEquals(2, result.getBody().getProductId());
        verify(favouriteClientService, times(1)).findById(userId, productId, likeDate);
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar favorito")
    void save_WhenValidData_ShouldSaveAndReturnFavourite() {
        // Arrange
        ResponseEntity<FavouriteDto> serviceResponse = ResponseEntity.ok(testFavouriteDto);
        when(favouriteClientService.save(testFavouriteDto)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<FavouriteDto> result = favouriteController.save(testFavouriteDto);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals(1, result.getBody().getUserId());
        verify(favouriteClientService, times(1)).save(testFavouriteDto);
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar favorito")
    void update_WhenValidData_ShouldUpdateAndReturnFavourite() {
        // Arrange
        ResponseEntity<FavouriteDto> serviceResponse = ResponseEntity.ok(testFavouriteDto);
        when(favouriteClientService.update(testFavouriteDto)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<FavouriteDto> result = favouriteController.update(testFavouriteDto);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals(1, result.getBody().getUserId());
        verify(favouriteClientService, times(1)).update(testFavouriteDto);
    }

    @Test
    @DisplayName("deleteById - Cuando favorito existe - Debe eliminar y retornar true")
    void deleteById_WhenFavouriteExists_ShouldDeleteAndReturnTrue() {
        // Arrange
        String userId = "1";
        String productId = "2";
        String likeDate = "2024-01-01 10:00:00";
        ResponseEntity<Boolean> serviceResponse = ResponseEntity.ok(true);
        when(favouriteClientService.deleteById(userId, productId, likeDate)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<Boolean> result = favouriteController.deleteById(userId, productId, likeDate);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertTrue(result.getBody());
        verify(favouriteClientService, times(1)).deleteById(userId, productId, likeDate);
    }
}
