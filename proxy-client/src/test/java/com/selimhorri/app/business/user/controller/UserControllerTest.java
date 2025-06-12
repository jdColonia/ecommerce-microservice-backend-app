package com.selimhorri.app.business.user.controller;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.util.Arrays;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.ResponseEntity;

import com.selimhorri.app.business.user.model.UserDto;
import com.selimhorri.app.business.user.model.response.UserUserServiceCollectionDtoResponse;
import com.selimhorri.app.business.user.service.UserClientService;

@ExtendWith(MockitoExtension.class)
@DisplayName("UserController - Unit Tests")
class UserControllerTest {

    @Mock
    private UserClientService userClientService;

    @InjectMocks
    private UserController userController;

    private UserDto testUserDto;
    private UserUserServiceCollectionDtoResponse testCollectionResponse;

    @BeforeEach
    void setUp() {
        testUserDto = UserDto.builder()
                .userId(1)
                .firstName("Juan")
                .lastName("Pérez")
                .email("juan.perez@test.com")
                .phone("+57123456789")
                .imageUrl("https://example.com/avatar.jpg")
                .build();

        testCollectionResponse = UserUserServiceCollectionDtoResponse.builder()
                .collection(Arrays.asList(testUserDto))
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando servicio retorna usuarios - Debe retornar colección de usuarios")
    void findAll_WhenServiceReturnsUsers_ShouldReturnUserCollection() {
        // Arrange
        ResponseEntity<UserUserServiceCollectionDtoResponse> serviceResponse = ResponseEntity
                .ok(testCollectionResponse);
        when(userClientService.findAll()).thenReturn(serviceResponse);

        // Act
        ResponseEntity<UserUserServiceCollectionDtoResponse> result = userController.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertNotNull(result.getBody());
        assertEquals(1, result.getBody().getCollection().size());
        assertEquals("Juan", result.getBody().getCollection().iterator().next().getFirstName());
        verify(userClientService, times(1)).findAll();
    }

    @Test
    @DisplayName("findAll - Cuando servicio lanza excepción - Debe propagar excepción")
    void findAll_WhenServiceThrowsException_ShouldPropagateException() {
        // Arrange
        when(userClientService.findAll())
                .thenThrow(new RuntimeException("Service unavailable"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> userController.findAll());

        assertEquals("Service unavailable", exception.getMessage());
        verify(userClientService, times(1)).findAll();
    }

    @Test
    @DisplayName("findById - Cuando usuario existe - Debe retornar usuario")
    void findById_WhenUserExists_ShouldReturnUser() {
        // Arrange
        String userId = "1";
        ResponseEntity<UserDto> serviceResponse = ResponseEntity.ok(testUserDto);
        when(userClientService.findById(userId)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<UserDto> result = userController.findById(userId);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertNotNull(result.getBody());
        assertEquals(1, result.getBody().getUserId());
        assertEquals("Juan", result.getBody().getFirstName());
        verify(userClientService, times(1)).findById(userId);
    }

    @Test
    @DisplayName("findById - Cuando usuario no existe - Debe propagar excepción del servicio")
    void findById_WhenUserNotExists_ShouldPropagateServiceException() {
        // Arrange
        String userId = "999";
        when(userClientService.findById(userId))
                .thenThrow(new RuntimeException("User not found"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> userController.findById(userId));

        assertEquals("User not found", exception.getMessage());
        verify(userClientService, times(1)).findById(userId);
    }

    @Test
    @DisplayName("findByUsername - Cuando usuario existe - Debe retornar usuario")
    void findByUsername_WhenUserExists_ShouldReturnUser() {
        // Arrange
        String username = "testuser";
        ResponseEntity<UserDto> serviceResponse = ResponseEntity.ok(testUserDto);
        when(userClientService.findByUsername(username)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<UserDto> result = userController.findByUsername(username);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertNotNull(result.getBody());
        assertEquals("Juan", result.getBody().getFirstName());
        verify(userClientService, times(1)).findByUsername(username);
    }

    @Test
    @DisplayName("findByUsername - Cuando username no existe - Debe propagar excepción")
    void findByUsername_WhenUsernameNotExists_ShouldPropagateException() {
        // Arrange
        String username = "nonexistent";
        when(userClientService.findByUsername(username))
                .thenThrow(new RuntimeException("Username not found"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> userController.findByUsername(username));

        assertEquals("Username not found", exception.getMessage());
        verify(userClientService, times(1)).findByUsername(username);
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar usuario")
    void save_WhenValidData_ShouldSaveAndReturnUser() {
        // Arrange
        ResponseEntity<UserDto> serviceResponse = ResponseEntity.ok(testUserDto);
        when(userClientService.save(testUserDto)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<UserDto> result = userController.save(testUserDto);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertNotNull(result.getBody());
        assertEquals("Juan", result.getBody().getFirstName());
        verify(userClientService, times(1)).save(testUserDto);
    }

    @Test
    @DisplayName("save - Cuando servicio lanza excepción - Debe propagar excepción")
    void save_WhenServiceThrowsException_ShouldPropagateException() {
        // Arrange
        when(userClientService.save(testUserDto))
                .thenThrow(new RuntimeException("Save failed"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> userController.save(testUserDto));

        assertEquals("Save failed", exception.getMessage());
        verify(userClientService, times(1)).save(testUserDto);
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar usuario")
    void update_WhenValidData_ShouldUpdateAndReturnUser() {
        // Arrange
        UserDto updatedUser = UserDto.builder()
                .userId(1)
                .firstName("Juan Carlos")
                .lastName("Pérez")
                .email("juan.carlos@test.com")
                .build();

        ResponseEntity<UserDto> serviceResponse = ResponseEntity.ok(updatedUser);
        when(userClientService.update(updatedUser)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<UserDto> result = userController.update(updatedUser);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals("Juan Carlos", result.getBody().getFirstName());
        verify(userClientService, times(1)).update(updatedUser);
    }

    @Test
    @DisplayName("update con userId - Cuando datos válidos - Debe actualizar y retornar usuario")
    void updateWithUserId_WhenValidData_ShouldUpdateAndReturnUser() {
        // Arrange
        String userId = "1";
        ResponseEntity<UserDto> serviceResponse = ResponseEntity.ok(testUserDto);
        when(userClientService.update(testUserDto)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<UserDto> result = userController.update(userId, testUserDto);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals("Juan", result.getBody().getFirstName());
        verify(userClientService, times(1)).update(testUserDto);
    }

    @Test
    @DisplayName("update con userId - Cuando usuario no existe - Debe propagar excepción")
    void updateWithUserId_WhenUserNotExists_ShouldPropagateException() {
        // Arrange
        String userId = "999";
        when(userClientService.update(testUserDto))
                .thenThrow(new RuntimeException("User not found for update"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> userController.update(userId, testUserDto));

        assertEquals("User not found for update", exception.getMessage());
        verify(userClientService, times(1)).update(testUserDto);
    }

    @Test
    @DisplayName("deleteById - Cuando usuario existe - Debe eliminar y retornar true")
    void deleteById_WhenUserExists_ShouldDeleteAndReturnTrue() {
        // Arrange
        String userId = "1";
        ResponseEntity<Boolean> serviceResponse = ResponseEntity.ok(true);
        when(userClientService.deleteById(userId)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<Boolean> result = userController.deleteById(userId);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertTrue(result.getBody());
        verify(userClientService, times(1)).deleteById(userId);
    }

    @Test
    @DisplayName("deleteById - Cuando usuario no existe - Debe propagar excepción")
    void deleteById_WhenUserNotExists_ShouldPropagateException() {
        // Arrange
        String userId = "999";
        when(userClientService.deleteById(userId))
                .thenThrow(new RuntimeException("User not found for deletion"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> userController.deleteById(userId));

        assertEquals("User not found for deletion", exception.getMessage());
        verify(userClientService, times(1)).deleteById(userId);
    }

    @Test
    @DisplayName("findById - Cuando userId es null - Debe manejar como parámetro válido")
    void findById_WhenUserIdIsNull_ShouldHandleAsValidParameter() {
        // Arrange
        String userId = null;
        ResponseEntity<UserDto> serviceResponse = ResponseEntity.ok(testUserDto);
        when(userClientService.findById(userId)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<UserDto> result = userController.findById(userId);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        verify(userClientService, times(1)).findById(userId);
    }

    @Test
    @DisplayName("save - Cuando userDto es null - Debe propagar excepción del servicio")
    void save_WhenUserDtoIsNull_ShouldPropagateServiceException() {
        // Arrange
        when(userClientService.save(null))
                .thenThrow(new RuntimeException("UserDto cannot be null"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> userController.save(null));

        assertEquals("UserDto cannot be null", exception.getMessage());
        verify(userClientService, times(1)).save(null);
    }
}
