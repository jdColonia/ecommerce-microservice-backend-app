package com.selimhorri.app.jwt.service.impl;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

import java.util.Date;
import java.util.function.Function;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.core.userdetails.UserDetails;

import com.selimhorri.app.jwt.util.JwtUtil;

import io.jsonwebtoken.Claims;

@ExtendWith(MockitoExtension.class)
@DisplayName("JwtServiceImpl - Unit Tests")
class JwtServiceImplTest {

    @Mock
    private JwtUtil jwtUtil;

    @Mock
    private UserDetails userDetails;

    @Mock
    private Claims claims;

    @InjectMocks
    private JwtServiceImpl jwtService;

    private String testToken;
    private String testUsername;
    private Date testExpirationDate;

    @BeforeEach
    void setUp() {
        testToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.token";
        testUsername = "testuser";
        testExpirationDate = new Date(System.currentTimeMillis() + 3600000); // 1 hora en el futuro
    }

    @Test
    @DisplayName("extractUsername - Cuando token válido - Debe retornar username")
    void extractUsername_WhenValidToken_ShouldReturnUsername() {
        // Arrange
        when(jwtUtil.extractUsername(testToken)).thenReturn(testUsername);

        // Act
        String result = jwtService.extractUsername(testToken);

        // Assert
        assertEquals(testUsername, result);
        verify(jwtUtil, times(1)).extractUsername(testToken);
    }

    @Test
    @DisplayName("extractUsername - Cuando token inválido - Debe propagar excepción")
    void extractUsername_WhenInvalidToken_ShouldPropagateException() {
        // Arrange
        when(jwtUtil.extractUsername(testToken))
                .thenThrow(new RuntimeException("Invalid token"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> jwtService.extractUsername(testToken));

        assertEquals("Invalid token", exception.getMessage());
        verify(jwtUtil, times(1)).extractUsername(testToken);
    }

    @Test
    @DisplayName("extractExpiration - Cuando token válido - Debe retornar fecha de expiración")
    void extractExpiration_WhenValidToken_ShouldReturnExpirationDate() {
        // Arrange
        when(jwtUtil.extractExpiration(testToken)).thenReturn(testExpirationDate);

        // Act
        Date result = jwtService.extractExpiration(testToken);

        // Assert
        assertEquals(testExpirationDate, result);
        verify(jwtUtil, times(1)).extractExpiration(testToken);
    }

    @Test
    @DisplayName("extractExpiration - Cuando token inválido - Debe propagar excepción")
    void extractExpiration_WhenInvalidToken_ShouldPropagateException() {
        // Arrange
        when(jwtUtil.extractExpiration(testToken))
                .thenThrow(new RuntimeException("Token expired"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> jwtService.extractExpiration(testToken));

        assertEquals("Token expired", exception.getMessage());
        verify(jwtUtil, times(1)).extractExpiration(testToken);
    }

    @Test
    @DisplayName("extractClaims - Cuando token válido y resolver válido - Debe retornar claims procesados")
    void extractClaims_WhenValidTokenAndResolver_ShouldReturnProcessedClaims() {
        // Arrange
        Function<Claims, String> claimsResolver = Claims::getSubject;
        String expectedSubject = "test-subject";
        when(jwtUtil.extractClaims(eq(testToken), eq(claimsResolver))).thenReturn(expectedSubject);

        // Act
        String result = jwtService.extractClaims(testToken, claimsResolver);

        // Assert
        assertEquals(expectedSubject, result);
        verify(jwtUtil, times(1)).extractClaims(testToken, claimsResolver);
    }

    @Test
    @DisplayName("extractClaims - Cuando resolver lanza excepción - Debe propagar excepción")
    void extractClaims_WhenResolverThrowsException_ShouldPropagateException() {
        // Arrange
        Function<Claims, String> claimsResolver = Claims::getSubject;
        when(jwtUtil.extractClaims(eq(testToken), eq(claimsResolver)))
                .thenThrow(new RuntimeException("Claims processing failed"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> jwtService.extractClaims(testToken, claimsResolver));

        assertEquals("Claims processing failed", exception.getMessage());
        verify(jwtUtil, times(1)).extractClaims(testToken, claimsResolver);
    }

    @Test
    @DisplayName("generateToken - Cuando userDetails válido - Debe retornar token")
    void generateToken_WhenValidUserDetails_ShouldReturnToken() {
        // Arrange
        String expectedToken = "generated.jwt.token";
        when(jwtUtil.generateToken(userDetails)).thenReturn(expectedToken);

        // Act
        String result = jwtService.generateToken(userDetails);

        // Assert
        assertEquals(expectedToken, result);
        verify(jwtUtil, times(1)).generateToken(userDetails);
    }

    @Test
    @DisplayName("generateToken - Cuando userDetails es null - Debe propagar excepción")
    void generateToken_WhenUserDetailsIsNull_ShouldPropagateException() {
        // Arrange
        when(jwtUtil.generateToken(null))
                .thenThrow(new RuntimeException("UserDetails cannot be null"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> jwtService.generateToken(null));

        assertEquals("UserDetails cannot be null", exception.getMessage());
        verify(jwtUtil, times(1)).generateToken(null);
    }

    @Test
    @DisplayName("validateToken - Cuando token válido y userDetails coinciden - Debe retornar true")
    void validateToken_WhenValidTokenAndMatchingUserDetails_ShouldReturnTrue() {
        // Arrange
        when(jwtUtil.validateToken(testToken, userDetails)).thenReturn(true);

        // Act
        Boolean result = jwtService.validateToken(testToken, userDetails);

        // Assert
        assertTrue(result);
        verify(jwtUtil, times(1)).validateToken(testToken, userDetails);
    }

    @Test
    @DisplayName("validateToken - Cuando token inválido - Debe retornar false")
    void validateToken_WhenInvalidToken_ShouldReturnFalse() {
        // Arrange
        when(jwtUtil.validateToken(testToken, userDetails)).thenReturn(false);

        // Act
        Boolean result = jwtService.validateToken(testToken, userDetails);

        // Assert
        assertFalse(result);
        verify(jwtUtil, times(1)).validateToken(testToken, userDetails);
    }

    @Test
    @DisplayName("validateToken - Cuando jwtUtil lanza excepción - Debe propagar excepción")
    void validateToken_WhenJwtUtilThrowsException_ShouldPropagateException() {
        // Arrange
        when(jwtUtil.validateToken(testToken, userDetails))
                .thenThrow(new RuntimeException("Token validation failed"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> jwtService.validateToken(testToken, userDetails));

        assertEquals("Token validation failed", exception.getMessage());
        verify(jwtUtil, times(1)).validateToken(testToken, userDetails);
    }

    @Test
    @DisplayName("extractUsername - Cuando token es null - Debe propagar excepción")
    void extractUsername_WhenTokenIsNull_ShouldPropagateException() {
        // Arrange
        when(jwtUtil.extractUsername(null))
                .thenThrow(new RuntimeException("Token cannot be null"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> jwtService.extractUsername(null));

        assertEquals("Token cannot be null", exception.getMessage());
        verify(jwtUtil, times(1)).extractUsername(null);
    }

    @Test
    @DisplayName("extractExpiration - Cuando token es vacío - Debe propagar excepción")
    void extractExpiration_WhenTokenIsEmpty_ShouldPropagateException() {
        // Arrange
        String emptyToken = "";
        when(jwtUtil.extractExpiration(emptyToken))
                .thenThrow(new RuntimeException("Token cannot be empty"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> jwtService.extractExpiration(emptyToken));

        assertEquals("Token cannot be empty", exception.getMessage());
        verify(jwtUtil, times(1)).extractExpiration(emptyToken);
    }

    @Test
    @DisplayName("validateToken - Cuando userDetails es null - Debe propagar excepción")
    void validateToken_WhenUserDetailsIsNull_ShouldPropagateException() {
        // Arrange
        when(jwtUtil.validateToken(testToken, null))
                .thenThrow(new RuntimeException("UserDetails cannot be null"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> jwtService.validateToken(testToken, null));

        assertEquals("UserDetails cannot be null", exception.getMessage());
        verify(jwtUtil, times(1)).validateToken(testToken, null);
    }
} 