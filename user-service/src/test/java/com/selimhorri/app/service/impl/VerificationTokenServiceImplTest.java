package com.selimhorri.app.service.impl;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

import java.time.LocalDate;
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

import com.selimhorri.app.domain.RoleBasedAuthority;
import com.selimhorri.app.domain.VerificationToken;
import com.selimhorri.app.domain.Credential;
import com.selimhorri.app.dto.VerificationTokenDto;
import com.selimhorri.app.dto.CredentialDto;
import com.selimhorri.app.exception.wrapper.VerificationTokenNotFoundException;
import com.selimhorri.app.repository.VerificationTokenRepository;

@ExtendWith(MockitoExtension.class)
@DisplayName("VerificationTokenServiceImpl - Unit Tests")
class VerificationTokenServiceImplTest {

    @Mock
    private VerificationTokenRepository verificationTokenRepository;

    @InjectMocks
    private VerificationTokenServiceImpl verificationTokenService;

    private VerificationToken testVerificationToken;
    private VerificationTokenDto testVerificationTokenDto;
    private Credential testCredential;

    @BeforeEach
    void setUp() {
        testCredential = Credential.builder()
                .credentialId(1)
                .username("testuser")
                .password("$2a$10$encodedPassword")
                .roleBasedAuthority(RoleBasedAuthority.ROLE_USER)
                .isEnabled(true)
                .isAccountNonExpired(true)
                .isAccountNonLocked(true)
                .isCredentialsNonExpired(true)
                .build();

        testVerificationToken = VerificationToken.builder()
                .verificationTokenId(1)
                .token("test-verification-token-123")
                .expireDate(LocalDate.now().plusDays(7))
                .credential(testCredential)
                .build();

        testVerificationTokenDto = VerificationTokenDto.builder()
                .verificationTokenId(1)
                .token("test-verification-token-123")
                .expireDate(LocalDate.now().plusDays(7))
                .credentialDto(CredentialDto.builder()
                        .credentialId(1)
                        .username("testuser")
                        .password("$2a$10$encodedPassword")
                        .roleBasedAuthority(RoleBasedAuthority.ROLE_USER)
                        .isEnabled(true)
                        .isAccountNonExpired(true)
                        .isAccountNonLocked(true)
                        .isCredentialsNonExpired(true)
                        .build())
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando existen tokens - Debe retornar lista de VerificationTokenDto")
    void findAll_WhenTokensExist_ShouldReturnVerificationTokenDtoList() {
        // Arrange
        List<VerificationToken> tokens = Arrays.asList(testVerificationToken);
        when(verificationTokenRepository.findAll()).thenReturn(tokens);

        // Act
        List<VerificationTokenDto> result = verificationTokenService.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals(testVerificationToken.getVerificationTokenId(), result.get(0).getVerificationTokenId());
        assertEquals(testVerificationToken.getToken(), result.get(0).getToken());
        assertEquals(testVerificationToken.getExpireDate(), result.get(0).getExpireDate());
        verify(verificationTokenRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("findAll - Cuando no existen tokens - Debe retornar lista vacía")
    void findAll_WhenNoTokensExist_ShouldReturnEmptyList() {
        // Arrange
        when(verificationTokenRepository.findAll()).thenReturn(Arrays.asList());

        // Act
        List<VerificationTokenDto> result = verificationTokenService.findAll();

        // Assert
        assertNotNull(result);
        assertTrue(result.isEmpty());
        verify(verificationTokenRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("findById - Cuando token existe - Debe retornar VerificationTokenDto")
    void findById_WhenTokenExists_ShouldReturnVerificationTokenDto() {
        // Arrange
        Integer tokenId = 1;
        when(verificationTokenRepository.findById(tokenId)).thenReturn(Optional.of(testVerificationToken));

        // Act
        VerificationTokenDto result = verificationTokenService.findById(tokenId);

        // Assert
        assertNotNull(result);
        assertEquals(testVerificationToken.getVerificationTokenId(), result.getVerificationTokenId());
        assertEquals(testVerificationToken.getToken(), result.getToken());
        assertEquals(testVerificationToken.getExpireDate(), result.getExpireDate());
        verify(verificationTokenRepository, times(1)).findById(tokenId);
    }

    @Test
    @DisplayName("findById - Cuando token no existe - Debe lanzar VerificationTokenNotFoundException")
    void findById_WhenTokenNotExists_ShouldThrowVerificationTokenNotFoundException() {
        // Arrange
        Integer tokenId = 999;
        when(verificationTokenRepository.findById(tokenId)).thenReturn(Optional.empty());

        // Act & Assert
        VerificationTokenNotFoundException exception = assertThrows(
                VerificationTokenNotFoundException.class,
                () -> verificationTokenService.findById(tokenId));

        assertTrue(exception.getMessage().contains("VerificationToken with id: 999 not found"));
        verify(verificationTokenRepository, times(1)).findById(tokenId);
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar VerificationTokenDto")
    void save_WhenValidData_ShouldSaveAndReturnVerificationTokenDto() {
        // Arrange
        when(verificationTokenRepository.save(any(VerificationToken.class))).thenReturn(testVerificationToken);

        // Act
        VerificationTokenDto result = verificationTokenService.save(testVerificationTokenDto);

        // Assert
        assertNotNull(result);
        assertEquals(testVerificationToken.getVerificationTokenId(), result.getVerificationTokenId());
        assertEquals(testVerificationToken.getToken(), result.getToken());
        verify(verificationTokenRepository, times(1)).save(any(VerificationToken.class));
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar VerificationTokenDto")
    void update_WhenValidData_ShouldUpdateAndReturnVerificationTokenDto() {
        // Arrange
        testVerificationTokenDto.setToken("updated-token-456");
        testVerificationTokenDto.setExpireDate(LocalDate.now().plusDays(14));

        VerificationToken updatedToken = VerificationToken.builder()
                .verificationTokenId(1)
                .token("updated-token-456")
                .expireDate(LocalDate.now().plusDays(14))
                .credential(testCredential)
                .build();

        when(verificationTokenRepository.save(any(VerificationToken.class))).thenReturn(updatedToken);

        // Act
        VerificationTokenDto result = verificationTokenService.update(testVerificationTokenDto);

        // Assert
        assertNotNull(result);
        assertEquals("updated-token-456", result.getToken());
        verify(verificationTokenRepository, times(1)).save(any(VerificationToken.class));
    }

    @Test
    @DisplayName("update con ID - Cuando token existe - Debe actualizar correctamente")
    void updateWithId_WhenTokenExists_ShouldUpdateCorrectly() {
        // Arrange
        Integer tokenId = 1;
        when(verificationTokenRepository.findById(tokenId)).thenReturn(Optional.of(testVerificationToken));
        when(verificationTokenRepository.save(any(VerificationToken.class))).thenReturn(testVerificationToken);

        // Act
        VerificationTokenDto result = verificationTokenService.update(tokenId, testVerificationTokenDto);

        // Assert
        assertNotNull(result);
        assertEquals(testVerificationToken.getVerificationTokenId(), result.getVerificationTokenId());
        verify(verificationTokenRepository, times(1)).findById(tokenId);
        verify(verificationTokenRepository, times(1)).save(any(VerificationToken.class));
    }

    @Test
    @DisplayName("update con ID - Cuando token no existe - Debe lanzar VerificationTokenNotFoundException")
    void updateWithId_WhenTokenNotExists_ShouldThrowVerificationTokenNotFoundException() {
        // Arrange
        Integer tokenId = 999;
        when(verificationTokenRepository.findById(tokenId)).thenReturn(Optional.empty());

        // Act & Assert
        VerificationTokenNotFoundException exception = assertThrows(
                VerificationTokenNotFoundException.class,
                () -> verificationTokenService.update(tokenId, testVerificationTokenDto));

        assertTrue(exception.getMessage().contains("VerificationToken with id: 999 not found"));
        verify(verificationTokenRepository, times(1)).findById(tokenId);
        verify(verificationTokenRepository, never()).save(any(VerificationToken.class));
    }

    @Test
    @DisplayName("deleteById - Cuando token existe - Debe eliminar sin excepción")
    void deleteById_WhenTokenExists_ShouldDeleteWithoutException() {
        // Arrange
        Integer tokenId = 1;
        doNothing().when(verificationTokenRepository).deleteById(tokenId);

        // Act & Assert
        assertDoesNotThrow(() -> verificationTokenService.deleteById(tokenId));
        verify(verificationTokenRepository, times(1)).deleteById(tokenId);
    }

    @Test
    @DisplayName("save - Con token sin credencial - Debe guardar correctamente")
    void save_WithTokenWithoutCredential_ShouldSaveCorrectly() {
        // Arrange
        VerificationTokenDto tokenDtoWithoutCredential = VerificationTokenDto.builder()
                .token("token-without-credential")
                .expireDate(LocalDate.now().plusDays(30))
                .credentialDto(null)
                .build();

        VerificationToken tokenWithoutCredential = VerificationToken.builder()
                .verificationTokenId(2)
                .token("token-without-credential")
                .expireDate(LocalDate.now().plusDays(30))
                .credential(null)
                .build();

        when(verificationTokenRepository.save(any(VerificationToken.class))).thenReturn(tokenWithoutCredential);

        // Act
        VerificationTokenDto result = verificationTokenService.save(tokenDtoWithoutCredential);

        // Assert
        assertNotNull(result);
        assertEquals("token-without-credential", result.getToken());
        assertNull(result.getCredentialDto());
        verify(verificationTokenRepository, times(1)).save(any(VerificationToken.class));
    }

    @Test
    @DisplayName("save - Con token expirado - Debe guardar correctamente")
    void save_WithExpiredToken_ShouldSaveCorrectly() {
        // Arrange
        LocalDate expiredDate = LocalDate.now().minusDays(1);
        testVerificationTokenDto.setExpireDate(expiredDate);
        testVerificationToken.setExpireDate(expiredDate);

        when(verificationTokenRepository.save(any(VerificationToken.class))).thenReturn(testVerificationToken);

        // Act
        VerificationTokenDto result = verificationTokenService.save(testVerificationTokenDto);

        // Assert
        assertNotNull(result);
        assertEquals(expiredDate, result.getExpireDate());
        verify(verificationTokenRepository, times(1)).save(any(VerificationToken.class));
    }
}
