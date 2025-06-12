package com.selimhorri.app.business.auth.controller;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.ResponseEntity;

import com.selimhorri.app.business.auth.model.request.AuthenticationRequest;
import com.selimhorri.app.business.auth.model.response.AuthenticationResponse;
import com.selimhorri.app.business.auth.service.AuthenticationService;

@ExtendWith(MockitoExtension.class)
@DisplayName("AuthenticationController - Unit Tests")
class AuthenticationControllerTest {

    @Mock
    private AuthenticationService authenticationService;

    @InjectMocks
    private AuthenticationController authenticationController;

    private AuthenticationRequest testAuthRequest;
    private AuthenticationResponse testAuthResponse;

    @BeforeEach
    void setUp() {
        testAuthRequest = new AuthenticationRequest("testuser", "password123");
        testAuthResponse = new AuthenticationResponse("jwt.token.here");
    }

    @Test
    @DisplayName("authenticate - Cuando credenciales válidas - Debe retornar token JWT")
    void authenticate_WhenValidCredentials_ShouldReturnJwtToken() {
        // Arrange
        when(authenticationService.authenticate(testAuthRequest)).thenReturn(testAuthResponse);

        // Act
        ResponseEntity<AuthenticationResponse> result = authenticationController.authenticate(testAuthRequest);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertNotNull(result.getBody());
        verify(authenticationService, times(1)).authenticate(testAuthRequest);
    }

    @Test
    @DisplayName("authenticate - Cuando service lanza excepción - Debe propagar excepción")
    void authenticate_WhenServiceThrowsException_ShouldPropagateException() {
        // Arrange
        when(authenticationService.authenticate(testAuthRequest))
                .thenThrow(new RuntimeException("Authentication failed"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> authenticationController.authenticate(testAuthRequest));

        assertEquals("Authentication failed", exception.getMessage());
        verify(authenticationService, times(1)).authenticate(testAuthRequest);
    }

    @Test
    @DisplayName("authenticate - Cuando username es null - Debe manejar correctamente")
    void authenticate_WhenUsernameIsNull_ShouldHandleCorrectly() {
        // Arrange
        AuthenticationRequest nullUsernameRequest = new AuthenticationRequest(null, "password123");
        AuthenticationResponse expectedResponse = new AuthenticationResponse("token.for.null.user");
        when(authenticationService.authenticate(nullUsernameRequest)).thenReturn(expectedResponse);

        // Act
        ResponseEntity<AuthenticationResponse> result = authenticationController.authenticate(nullUsernameRequest);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        verify(authenticationService, times(1)).authenticate(nullUsernameRequest);
    }

    @Test
    @DisplayName("authenticate - Cuando password es vacío - Debe manejar correctamente")
    void authenticate_WhenPasswordIsEmpty_ShouldHandleCorrectly() {
        // Arrange
        AuthenticationRequest emptyPasswordRequest = new AuthenticationRequest("testuser", "");
        AuthenticationResponse expectedResponse = new AuthenticationResponse("token.for.empty.password");
        when(authenticationService.authenticate(emptyPasswordRequest)).thenReturn(expectedResponse);

        // Act
        ResponseEntity<AuthenticationResponse> result = authenticationController.authenticate(emptyPasswordRequest);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        verify(authenticationService, times(1)).authenticate(emptyPasswordRequest);
    }

    @Test
    @DisplayName("authenticate por JWT - Cuando token válido - Debe retornar true")
    void authenticateByJwt_WhenValidToken_ShouldReturnTrue() {
        // Arrange
        String validJwt = "valid.jwt.token";
        when(authenticationService.authenticate(validJwt)).thenReturn(true);

        // Act
        ResponseEntity<Boolean> result = authenticationController.authenticate(validJwt);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertTrue(result.getBody());
        verify(authenticationService, times(1)).authenticate(validJwt);
    }

    @Test
    @DisplayName("authenticate por JWT - Cuando token inválido - Debe retornar false")
    void authenticateByJwt_WhenInvalidToken_ShouldReturnFalse() {
        // Arrange
        String invalidJwt = "invalid.jwt.token";
        when(authenticationService.authenticate(invalidJwt)).thenReturn(false);

        // Act
        ResponseEntity<Boolean> result = authenticationController.authenticate(invalidJwt);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertFalse(result.getBody());
        verify(authenticationService, times(1)).authenticate(invalidJwt);
    }

    @Test
    @DisplayName("authenticate por JWT - Cuando token es null - Debe manejar correctamente")
    void authenticateByJwt_WhenTokenIsNull_ShouldHandleCorrectly() {
        // Arrange
        String nullJwt = null;
        when(authenticationService.authenticate(nullJwt)).thenReturn(false);

        // Act
        ResponseEntity<Boolean> result = authenticationController.authenticate(nullJwt);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertFalse(result.getBody());
        verify(authenticationService, times(1)).authenticate(nullJwt);
    }

    @Test
    @DisplayName("authenticate por JWT - Cuando service lanza excepción - Debe propagar excepción")
    void authenticateByJwt_WhenServiceThrowsException_ShouldPropagateException() {
        // Arrange
        String jwt = "some.jwt.token";
        when(authenticationService.authenticate(jwt))
                .thenThrow(new RuntimeException("JWT validation failed"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> authenticationController.authenticate(jwt));

        assertEquals("JWT validation failed", exception.getMessage());
        verify(authenticationService, times(1)).authenticate(jwt);
    }

    @Test
    @DisplayName("authenticate - Cuando response es null - Debe manejar correctamente")
    void authenticate_WhenResponseIsNull_ShouldHandleCorrectly() {
        // Arrange
        when(authenticationService.authenticate(testAuthRequest)).thenReturn(null);

        // Act
        ResponseEntity<AuthenticationResponse> result = authenticationController.authenticate(testAuthRequest);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertNull(result.getBody());
        verify(authenticationService, times(1)).authenticate(testAuthRequest);
    }
}
