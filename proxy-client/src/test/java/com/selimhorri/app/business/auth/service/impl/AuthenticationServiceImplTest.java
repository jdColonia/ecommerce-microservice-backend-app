package com.selimhorri.app.business.auth.service.impl;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;

import com.selimhorri.app.business.auth.model.request.AuthenticationRequest;
import com.selimhorri.app.business.auth.model.response.AuthenticationResponse;
import com.selimhorri.app.exception.wrapper.IllegalAuthenticationCredentialsException;
import com.selimhorri.app.jwt.service.JwtService;

@ExtendWith(MockitoExtension.class)
@DisplayName("AuthenticationServiceImpl - Unit Tests")
class AuthenticationServiceImplTest {

    @Mock
    private AuthenticationManager authenticationManager;

    @Mock
    private UserDetailsService userDetailsService;

    @Mock
    private JwtService jwtService;

    @Mock
    private UserDetails userDetails;

    @InjectMocks
    private AuthenticationServiceImpl authenticationService;

    private AuthenticationRequest testAuthRequest;

    @BeforeEach
    void setUp() {
        testAuthRequest = new AuthenticationRequest("testuser", "password123");
    }

    @Test
    @DisplayName("authenticate - Cuando credenciales válidas - Debe retornar token JWT")
    void authenticate_WhenValidCredentials_ShouldReturnJwtToken() {
        // Arrange
        String expectedToken = "generated.jwt.token";
        when(userDetailsService.loadUserByUsername("testuser")).thenReturn(userDetails);
        when(jwtService.generateToken(userDetails)).thenReturn(expectedToken);

        // Act
        AuthenticationResponse result = authenticationService.authenticate(testAuthRequest);

        // Assert
        assertNotNull(result);
        verify(userDetailsService, times(1)).loadUserByUsername("testuser");
        verify(jwtService, times(1)).generateToken(userDetails);
    }

    @Test
    @DisplayName("authenticate - Cuando credenciales inválidas - Debe lanzar IllegalAuthenticationCredentialsException")
    void authenticate_WhenInvalidCredentials_ShouldThrowIllegalAuthenticationCredentialsException() {
        // Arrange
        doThrow(new BadCredentialsException("Bad credentials"))
                .when(authenticationManager).authenticate(any());

        // Act & Assert
        IllegalAuthenticationCredentialsException exception = assertThrows(
                IllegalAuthenticationCredentialsException.class,
                () -> authenticationService.authenticate(testAuthRequest));

        assertEquals("#### Bad credentials! ####", exception.getMessage());
        verify(authenticationManager, times(1)).authenticate(any());
    }

    @Test
    @DisplayName("authenticate por JWT - Cuando se llama - Debe retornar null")
    void authenticateByJwt_WhenCalled_ShouldReturnNull() {
        // Arrange
        String jwt = "some.jwt.token";

        // Act
        Boolean result = authenticationService.authenticate(jwt);

        // Assert
        assertNull(result);
    }
}
