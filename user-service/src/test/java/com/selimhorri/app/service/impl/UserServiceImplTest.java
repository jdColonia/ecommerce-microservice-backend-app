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
import com.selimhorri.app.domain.User;
import com.selimhorri.app.domain.Credential;
import com.selimhorri.app.dto.UserDto;
import com.selimhorri.app.dto.CredentialDto;
import com.selimhorri.app.exception.wrapper.UserObjectNotFoundException;
import com.selimhorri.app.repository.UserRepository;

@ExtendWith(MockitoExtension.class)
@DisplayName("UserServiceImpl - Unit Tests")
class UserServiceImplTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserServiceImpl userService;

    private User testUser;
    private UserDto testUserDto;
    private Credential testCredential;
    private CredentialDto testCredentialDto;

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

        testUser = User.builder()
                .userId(1)
                .firstName("John")
                .lastName("Doe")
                .email("john.doe@test.com")
                .phone("+1234567890")
                .imageUrl("https://example.com/avatar.jpg")
                .credential(testCredential)
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
                .build();

        testUserDto = UserDto.builder()
                .userId(1)
                .firstName("John")
                .lastName("Doe")
                .email("john.doe@test.com")
                .phone("+1234567890")
                .imageUrl("https://example.com/avatar.jpg")
                .credentialDto(testCredentialDto)
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando existen usuarios - Debe retornar lista de UserDto")
    void findAll_WhenUsersExist_ShouldReturnUserDtoList() {
        // Arrange
        List<User> users = Arrays.asList(testUser);
        when(userRepository.findAllWithCredentials()).thenReturn(users);

        // Act
        List<UserDto> result = userService.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals(testUser.getUserId(), result.get(0).getUserId());
        assertEquals(testUser.getFirstName(), result.get(0).getFirstName());
        assertEquals(testUser.getLastName(), result.get(0).getLastName());
        assertEquals(testUser.getEmail(), result.get(0).getEmail());
        verify(userRepository, times(1)).findAllWithCredentials();
    }

    @Test
    @DisplayName("findAll - Cuando no existen usuarios - Debe retornar lista vacía")
    void findAll_WhenNoUsersExist_ShouldReturnEmptyList() {
        // Arrange
        when(userRepository.findAllWithCredentials()).thenReturn(Arrays.asList());

        // Act
        List<UserDto> result = userService.findAll();

        // Assert
        assertNotNull(result);
        assertTrue(result.isEmpty());
        verify(userRepository, times(1)).findAllWithCredentials();
    }

    @Test
    @DisplayName("findById - Cuando usuario existe - Debe retornar UserDto")
    void findById_WhenUserExists_ShouldReturnUserDto() {
        // Arrange
        Integer userId = 1;
        when(userRepository.findByIdWithCredential(userId)).thenReturn(Optional.of(testUser));

        // Act
        UserDto result = userService.findById(userId);

        // Assert
        assertNotNull(result);
        assertEquals(testUser.getUserId(), result.getUserId());
        assertEquals(testUser.getFirstName(), result.getFirstName());
        assertEquals(testUser.getEmail(), result.getEmail());
        assertEquals(testUser.getCredential().getUsername(), result.getCredentialDto().getUsername());
        verify(userRepository, times(1)).findByIdWithCredential(userId);
    }

    @Test
    @DisplayName("findById - Cuando usuario no existe - Debe lanzar UserObjectNotFoundException")
    void findById_WhenUserNotExists_ShouldThrowUserObjectNotFoundException() {
        // Arrange
        Integer userId = 999;
        when(userRepository.findByIdWithCredential(userId)).thenReturn(Optional.empty());

        // Act & Assert
        UserObjectNotFoundException exception = assertThrows(
                UserObjectNotFoundException.class,
                () -> userService.findById(userId));

        assertTrue(exception.getMessage().contains("User with id: 999 not found"));
        verify(userRepository, times(1)).findByIdWithCredential(userId);
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar UserDto")
    void save_WhenValidData_ShouldSaveAndReturnUserDto() {
        // Arrange
        when(userRepository.save(any(User.class))).thenReturn(testUser);

        // Act
        UserDto result = userService.save(testUserDto);

        // Assert
        assertNotNull(result);
        assertEquals(testUser.getUserId(), result.getUserId());
        assertEquals(testUser.getFirstName(), result.getFirstName());
        assertEquals(testUser.getEmail(), result.getEmail());
        verify(userRepository, times(1)).save(any(User.class));
    }

    @Test
    @DisplayName("findByUsername - Cuando usuario existe - Debe retornar UserDto")
    void findByUsername_WhenUserExists_ShouldReturnUserDto() {
        // Arrange
        String username = "testuser";
        when(userRepository.findByCredentialUsernameWithCredential(username)).thenReturn(Optional.of(testUser));

        // Act
        UserDto result = userService.findByUsername(username);

        // Assert
        assertNotNull(result);
        assertEquals(testUser.getUserId(), result.getUserId());
        assertEquals(testUser.getCredential().getUsername(), result.getCredentialDto().getUsername());
        verify(userRepository, times(1)).findByCredentialUsernameWithCredential(username);
    }

    @Test
    @DisplayName("findByUsername - Cuando usuario no existe - Debe lanzar UserObjectNotFoundException")
    void findByUsername_WhenUserNotExists_ShouldThrowUserObjectNotFoundException() {
        // Arrange
        String username = "nonexistent";
        when(userRepository.findByCredentialUsernameWithCredential(username)).thenReturn(Optional.empty());

        // Act & Assert
        UserObjectNotFoundException exception = assertThrows(
                UserObjectNotFoundException.class,
                () -> userService.findByUsername(username));

        assertTrue(exception.getMessage().contains("User with username: nonexistent not found"));
        verify(userRepository, times(1)).findByCredentialUsernameWithCredential(username);
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar UserDto")
    void update_WhenValidData_ShouldUpdateAndReturnUserDto() {
        // Arrange
        testUserDto.setFirstName("Jane");
        testUserDto.setLastName("Smith");

        User updatedUser = User.builder()
                .userId(1)
                .firstName("Jane")
                .lastName("Smith")
                .email("john.doe@test.com")
                .phone("+1234567890")
                .imageUrl("https://example.com/avatar.jpg")
                .credential(testCredential)
                .build();

        when(userRepository.save(any(User.class))).thenReturn(updatedUser);

        // Act
        UserDto result = userService.update(testUserDto);

        // Assert
        assertNotNull(result);
        assertEquals("Jane", result.getFirstName());
        assertEquals("Smith", result.getLastName());
        verify(userRepository, times(1)).save(any(User.class));
    }

    @Test
    @DisplayName("update con ID - Cuando usuario existe - Debe actualizar correctamente")
    void updateWithId_WhenUserExists_ShouldUpdateCorrectly() {
        // Arrange
        Integer userId = 1;
        when(userRepository.findByIdWithCredential(userId)).thenReturn(Optional.of(testUser));
        when(userRepository.save(any(User.class))).thenReturn(testUser);

        // Act
        UserDto result = userService.update(userId, testUserDto);

        // Assert
        assertNotNull(result);
        assertEquals(testUser.getUserId(), result.getUserId());
        verify(userRepository, times(1)).findByIdWithCredential(userId);
        verify(userRepository, times(1)).save(any(User.class));
    }

    @Test
    @DisplayName("update con ID - Cuando usuario no existe - Debe lanzar UserObjectNotFoundException")
    void updateWithId_WhenUserNotExists_ShouldThrowUserObjectNotFoundException() {
        // Arrange
        Integer userId = 999;
        when(userRepository.findByIdWithCredential(userId)).thenReturn(Optional.empty());

        // Act & Assert
        UserObjectNotFoundException exception = assertThrows(
                UserObjectNotFoundException.class,
                () -> userService.update(userId, testUserDto));

        assertTrue(exception.getMessage().contains("User with id: 999 not found"));
        verify(userRepository, times(1)).findByIdWithCredential(userId);
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    @DisplayName("deleteById - Cuando usuario existe - Debe eliminar sin excepción")
    void deleteById_WhenUserExists_ShouldDeleteWithoutException() {
        // Arrange
        Integer userId = 1;
        doNothing().when(userRepository).deleteById(userId);

        // Act & Assert
        assertDoesNotThrow(() -> userService.deleteById(userId));
        verify(userRepository, times(1)).deleteById(userId);
    }

    @Test
    @DisplayName("save - Con usuario sin credencial - Debe guardar correctamente")
    void save_WithUserWithoutCredential_ShouldSaveCorrectly() {
        // Arrange
        UserDto userDtoWithoutCredential = UserDto.builder()
                .firstName("No Credential")
                .lastName("User")
                .email("nocredential@test.com")
                .phone("+9876543210")
                .credentialDto(null)
                .build();

        User userWithoutCredential = User.builder()
                .userId(2)
                .firstName("No Credential")
                .lastName("User")
                .email("nocredential@test.com")
                .phone("+9876543210")
                .credential(null)
                .build();

        when(userRepository.save(any(User.class))).thenReturn(userWithoutCredential);

        // Act
        UserDto result = userService.save(userDtoWithoutCredential);

        // Assert
        assertNotNull(result);
        assertEquals("No Credential", result.getFirstName());
        assertNull(result.getCredentialDto());
        verify(userRepository, times(1)).save(any(User.class));
    }

    @Test
    @DisplayName("findAll - Con múltiples usuarios - Debe retornar todos correctamente")
    void findAll_WithMultipleUsers_ShouldReturnAllCorrectly() {
        // Arrange
        User user2 = User.builder()
                .userId(2)
                .firstName("Jane")
                .lastName("Smith")
                .email("jane.smith@test.com")
                .phone("+0987654321")
                .credential(Credential.builder()
                        .credentialId(2)
                        .username("janesmith")
                        .roleBasedAuthority(RoleBasedAuthority.ROLE_ADMIN)
                        .isEnabled(true)
                        .build())
                .build();

        List<User> users = Arrays.asList(testUser, user2);
        when(userRepository.findAllWithCredentials()).thenReturn(users);

        // Act
        List<UserDto> result = userService.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(2, result.size());
        assertEquals("John", result.get(0).getFirstName());
        assertEquals("Jane", result.get(1).getFirstName());
        verify(userRepository, times(1)).findAllWithCredentials();
    }
}
