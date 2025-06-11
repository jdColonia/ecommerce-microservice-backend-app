package com.selimhorri.app.service.impl;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

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
import com.selimhorri.app.domain.Credential;
import com.selimhorri.app.domain.User;
import com.selimhorri.app.dto.CredentialDto;
import com.selimhorri.app.dto.UserDto;
import com.selimhorri.app.exception.wrapper.CredentialNotFoundException;
import com.selimhorri.app.exception.wrapper.UserObjectNotFoundException;
import com.selimhorri.app.repository.CredentialRepository;

@ExtendWith(MockitoExtension.class)
@DisplayName("CredentialServiceImpl - Unit Tests")
class CredentialServiceImplTest {

    @Mock
    private CredentialRepository credentialRepository;

    @InjectMocks
    private CredentialServiceImpl credentialService;

    private Credential testCredential;
    private CredentialDto testCredentialDto;
    private User testUser;

    @BeforeEach
    void setUp() {
        testUser = User.builder()
                .userId(1)
                .firstName("John")
                .lastName("Doe")
                .email("john.doe@test.com")
                .phone("+1234567890")
                .build();

        testCredential = Credential.builder()
                .credentialId(1)
                .username("testuser")
                .password("$2a$10$encodedPassword")
                .roleBasedAuthority(RoleBasedAuthority.ROLE_USER)
                .isEnabled(true)
                .isAccountNonExpired(true)
                .isAccountNonLocked(true)
                .isCredentialsNonExpired(true)
                .user(testUser)
                .build();

        testCredentialDto = CredentialDto.builder()
                .credentialId(1)
                .username("testuser")
                .password("$2a$10$encodedPassword")
                .roleBasedAuthority(RoleBasedAuthority.ROLE_USER)
                .isEnabled(true)
                .isAccountNonExpired(true)
                .isAccountNonLocked(true)
                .isCredentialsNonExpired(true)
                .userDto(UserDto.builder()
                        .userId(1)
                        .firstName("John")
                        .lastName("Doe")
                        .email("john.doe@test.com")
                        .phone("+1234567890")
                        .build())
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando existen credenciales - Debe retornar lista de CredentialDto")
    void findAll_WhenCredentialsExist_ShouldReturnCredentialDtoList() {
        // Arrange
        List<Credential> credentials = Arrays.asList(testCredential);
        when(credentialRepository.findAllWithUser()).thenReturn(credentials);

        // Act
        List<CredentialDto> result = credentialService.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals(testCredential.getCredentialId(), result.get(0).getCredentialId());
        assertEquals(testCredential.getUsername(), result.get(0).getUsername());
        verify(credentialRepository, times(1)).findAllWithUser();
    }

    @Test
    @DisplayName("findAll - Cuando no existen credenciales - Debe retornar lista vacía")
    void findAll_WhenNoCredentialsExist_ShouldReturnEmptyList() {
        // Arrange
        when(credentialRepository.findAllWithUser()).thenReturn(Arrays.asList());

        // Act
        List<CredentialDto> result = credentialService.findAll();

        // Assert
        assertNotNull(result);
        assertTrue(result.isEmpty());
        verify(credentialRepository, times(1)).findAllWithUser();
    }

    @Test
    @DisplayName("findById - Cuando credencial existe - Debe retornar CredentialDto")
    void findById_WhenCredentialExists_ShouldReturnCredentialDto() {
        // Arrange
        Integer credentialId = 1;
        when(credentialRepository.findByIdWithUser(credentialId)).thenReturn(Optional.of(testCredential));

        // Act
        CredentialDto result = credentialService.findById(credentialId);

        // Assert
        assertNotNull(result);
        assertEquals(testCredential.getCredentialId(), result.getCredentialId());
        assertEquals(testCredential.getUsername(), result.getUsername());
        verify(credentialRepository, times(1)).findByIdWithUser(credentialId);
    }

    @Test
    @DisplayName("findById - Cuando credencial no existe - Debe lanzar CredentialNotFoundException")
    void findById_WhenCredentialNotExists_ShouldThrowCredentialNotFoundException() {
        // Arrange
        Integer credentialId = 999;
        when(credentialRepository.findByIdWithUser(credentialId)).thenReturn(Optional.empty());

        // Act & Assert
        CredentialNotFoundException exception = assertThrows(
                CredentialNotFoundException.class,
                () -> credentialService.findById(credentialId));

        assertTrue(exception.getMessage().contains("Credential with id: 999 not found"));
        verify(credentialRepository, times(1)).findByIdWithUser(credentialId);
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar CredentialDto")
    void save_WhenValidData_ShouldSaveAndReturnCredentialDto() {
        // Arrange
        when(credentialRepository.save(any(Credential.class))).thenReturn(testCredential);

        // Act
        CredentialDto result = credentialService.save(testCredentialDto);

        // Assert
        assertNotNull(result);
        assertEquals(testCredential.getCredentialId(), result.getCredentialId());
        assertEquals(testCredential.getUsername(), result.getUsername());
        verify(credentialRepository, times(1)).save(any(Credential.class));
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar CredentialDto")
    void update_WhenValidData_ShouldUpdateAndReturnCredentialDto() {
        // Arrange
        when(credentialRepository.save(any(Credential.class))).thenReturn(testCredential);

        // Act
        CredentialDto result = credentialService.update(testCredentialDto);

        // Assert
        assertNotNull(result);
        assertEquals(testCredential.getCredentialId(), result.getCredentialId());
        verify(credentialRepository, times(1)).save(any(Credential.class));
    }

    @Test
    @DisplayName("update con ID - Cuando credencial existe - Debe actualizar correctamente")
    void updateWithId_WhenCredentialExists_ShouldUpdateCorrectly() {
        // Arrange
        Integer credentialId = 1;
        when(credentialRepository.findByIdWithUser(credentialId)).thenReturn(Optional.of(testCredential));
        when(credentialRepository.save(any(Credential.class))).thenReturn(testCredential);

        // Act
        CredentialDto result = credentialService.update(credentialId, testCredentialDto);

        // Assert
        assertNotNull(result);
        assertEquals(testCredential.getCredentialId(), result.getCredentialId());
        verify(credentialRepository, times(1)).findByIdWithUser(credentialId);
        verify(credentialRepository, times(1)).save(any(Credential.class));
    }

    @Test
    @DisplayName("deleteById - Cuando credencial existe - Debe eliminar sin excepción")
    void deleteById_WhenCredentialExists_ShouldDeleteWithoutException() {
        // Arrange
        Integer credentialId = 1;
        doNothing().when(credentialRepository).deleteById(credentialId);

        // Act & Assert
        assertDoesNotThrow(() -> credentialService.deleteById(credentialId));
        verify(credentialRepository, times(1)).deleteById(credentialId);
    }

    @Test
    @DisplayName("findByUsername - Cuando usuario existe - Debe retornar CredentialDto")
    void findByUsername_WhenUserExists_ShouldReturnCredentialDto() {
        // Arrange
        String username = "testuser";
        when(credentialRepository.findByUsernameWithUser(username)).thenReturn(Optional.of(testCredential));

        // Act
        CredentialDto result = credentialService.findByUsername(username);

        // Assert
        assertNotNull(result);
        assertEquals(testCredential.getUsername(), result.getUsername());
        assertEquals(testCredential.getCredentialId(), result.getCredentialId());
        verify(credentialRepository, times(1)).findByUsernameWithUser(username);
    }

    @Test
    @DisplayName("findByUsername - Cuando usuario no existe - Debe lanzar UserObjectNotFoundException")
    void findByUsername_WhenUserNotExists_ShouldThrowUserObjectNotFoundException() {
        // Arrange
        String username = "nonexistent";
        when(credentialRepository.findByUsernameWithUser(username)).thenReturn(Optional.empty());

        // Act & Assert
        UserObjectNotFoundException exception = assertThrows(
                UserObjectNotFoundException.class,
                () -> credentialService.findByUsername(username));

        assertTrue(exception.getMessage().contains("Credential with username: nonexistent not found"));
        verify(credentialRepository, times(1)).findByUsernameWithUser(username);
    }
}
