package com.selimhorri.app.integration;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.test.context.ActiveProfiles;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.selimhorri.app.domain.RoleBasedAuthority;
import com.selimhorri.app.domain.User;
import com.selimhorri.app.domain.Credential;
import com.selimhorri.app.dto.UserDto;
import com.selimhorri.app.dto.CredentialDto;
import com.selimhorri.app.repository.UserRepository;

/**
 * Integration tests for User Service.
 * These tests verify the complete user management workflow including:
 * - REST API endpoints
 * - Service layer business logic
 * - Data persistence in H2 database
 * - DTO/Entity mapping
 * - Authentication and authorization features
 */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
@TestPropertySource(properties = {
        // H2 database configuration for fast testing
        "spring.datasource.url=jdbc:h2:mem:testdb;MODE=MySQL;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE",
        "spring.datasource.driver-class-name=org.h2.Driver",
        "spring.datasource.username=sa",
        "spring.datasource.password="
})
@AutoConfigureMockMvc
@Transactional
@DisplayName("User Service Integration Tests")
public class UserServiceIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private UserRepository userRepository;

    private UserDto testUserDto;
    private User testUser;

    @BeforeEach
    void setUp() {
        // Clear repository before each test
        userRepository.deleteAll();

        // Generate unique identifiers to avoid constraint violations
        String timestamp = String.valueOf(System.currentTimeMillis());
        String uniqueUsernameMaria = "maria_" + timestamp;
        String uniqueUsernameJuan = "juan_" + timestamp;

        // Setup test data with proper bidirectional relationships and unique usernames
        testUser = User.builder()
                .firstName("María José")
                .lastName("López Martínez")
                .email("maria.lopez." + timestamp + "@universidadean.edu.co")
                .phone("+57 314 987 6543")
                .imageUrl("https://cdn.universidadean.edu.co/avatars/maria-lopez.jpg")
                .build();

        Credential credential = Credential.builder()
                .username(uniqueUsernameMaria)
                .password("$2a$10$N.zmdr9k7uOCQb07YxkiNOhsqlQ5166rWa8rN5.4aDh7d6c8QWsma")
                .roleBasedAuthority(RoleBasedAuthority.ROLE_USER)
                .isEnabled(true)
                .isAccountNonExpired(true)
                .isAccountNonLocked(true)
                .isCredentialsNonExpired(true)
                .user(testUser) // Set bidirectional relationship
                .build();

        testUser.setCredential(credential); // Complete bidirectional relationship

        // Setup DTO for creating new users with unique username
        CredentialDto credentialDto = CredentialDto.builder()
                .username(uniqueUsernameJuan)
                .password("$2a$10$N.zmdr9k7uOCQb07YxkiNOhsqlQ5166rWa8rN5.4aDh7d6c8QWsma")
                .roleBasedAuthority(RoleBasedAuthority.ROLE_USER)
                .isEnabled(true)
                .isAccountNonExpired(true)
                .isAccountNonLocked(true)
                .isCredentialsNonExpired(true)
                .build();

        testUserDto = UserDto.builder()
                .firstName("Juan David")
                .lastName("Pérez Rodríguez")
                .email("juan.perez." + timestamp + "@universidadean.edu.co")
                .phone("+57 321 456 7890")
                .imageUrl("https://cdn.universidadean.edu.co/avatars/juan-perez.jpg")
                .credentialDto(credentialDto)
                .build();
    }

    @Test
    @DisplayName("POST /api/users - Should create new user and return 200")
    void createUser_WithValidData_ShouldCreateUserAndReturn200() throws Exception {
        // When & Then
        MvcResult result = mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(testUserDto)))
                .andExpect(status().isOk()) // API returns 200, not 201
                .andExpect(jsonPath("$.userId").exists())
                .andExpect(jsonPath("$.firstName").value("Juan David"))
                .andExpect(jsonPath("$.lastName").value("Pérez Rodríguez"))
                .andExpect(jsonPath("$.email").value(testUserDto.getEmail()))
                .andExpect(jsonPath("$.phone").value("+57 321 456 7890"))
                .andExpect(jsonPath("$.imageUrl").value("https://cdn.universidadean.edu.co/avatars/juan-perez.jpg"))
                .andExpect(jsonPath("$.credential.username").value(testUserDto.getCredentialDto().getUsername()))
                .andExpect(jsonPath("$.credential.roleBasedAuthority").value("ROLE_USER"))
                .andExpect(jsonPath("$.credential.isEnabled").value(true))
                .andReturn();

        // Verify user was persisted in database
        List<User> users = userRepository.findAll();
        assertThat(users).hasSize(1);

        User savedUser = users.get(0);
        assertThat(savedUser.getFirstName()).isEqualTo("Juan David");
        assertThat(savedUser.getLastName()).isEqualTo("Pérez Rodríguez");
        assertThat(savedUser.getEmail()).isEqualTo(testUserDto.getEmail());
        assertThat(savedUser.getCredential().getUsername()).isEqualTo(testUserDto.getCredentialDto().getUsername());
    }

    @Test
    @DisplayName("GET /api/users/{userId} - Should return user when exists")
    void getUserById_WhenUserExists_ShouldReturnUser() throws Exception {
        // Given - Save user in database
        User savedUser = userRepository.save(testUser);

        // When & Then
        mockMvc.perform(get("/api/users/{userId}", savedUser.getUserId())
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.userId").value(savedUser.getUserId()))
                .andExpect(jsonPath("$.firstName").value("María José"))
                .andExpect(jsonPath("$.lastName").value("López Martínez"))
                .andExpect(jsonPath("$.email").value(savedUser.getEmail()))
                .andExpect(jsonPath("$.phone").value("+57 314 987 6543"))
                .andExpect(jsonPath("$.credential.username").value(savedUser.getCredential().getUsername()));
    }

    @Test
    @DisplayName("GET /api/users/{userId} - Should return 400 when user not exists")
    void getUserById_WhenUserNotExists_ShouldReturn400() throws Exception {
        // When & Then
        mockMvc.perform(get("/api/users/{userId}", 999)
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.msg").value("#### User with id: 999 not found! ####"));
    }

    @Test
    @DisplayName("GET /api/users - Should return all users")
    void getAllUsers_ShouldReturnAllUsers() throws Exception {
        // Given - Save multiple users
        User user1 = userRepository.save(testUser);

        // Create second user with proper bidirectional relationship and unique username
        String uniqueUsername2 = "carlos_" + System.currentTimeMillis();
        User user2 = User.builder()
                .firstName("Carlos")
                .lastName("Rodríguez")
                .email("carlos.rodriguez." + System.currentTimeMillis() + "@universidadean.edu.co")
                .phone("+57 302 555 7777")
                .imageUrl("https://cdn.universidadean.edu.co/avatars/carlos.jpg")
                .build();

        Credential credential2 = Credential.builder()
                .username(uniqueUsername2)
                .password("$2a$10$N.zmdr9k7uOCQb07YxkiNOhsqlQ5166rWa8rN5.4aDh7d6c8QWsma")
                .roleBasedAuthority(RoleBasedAuthority.ROLE_ADMIN)
                .isEnabled(true)
                .isAccountNonExpired(true)
                .isAccountNonLocked(true)
                .isCredentialsNonExpired(true)
                .user(user2)
                .build();

        user2.setCredential(credential2);
        userRepository.save(user2);

        // When & Then
        mockMvc.perform(get("/api/users")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.collection").isArray())
                .andExpect(jsonPath("$.collection.length()").value(2))
                .andExpect(jsonPath("$.collection[0].firstName").value("María José"))
                .andExpect(jsonPath("$.collection[1].firstName").value("Carlos"))
                .andExpect(jsonPath("$.collection[0].credential.roleBasedAuthority").value("ROLE_USER"))
                .andExpect(jsonPath("$.collection[1].credential.roleBasedAuthority").value("ROLE_ADMIN"));
    }

    @Test
    @DisplayName("GET /api/users/username/{username} - Should return user by username")
    void getUserByUsername_WhenUserExists_ShouldReturnUser() throws Exception {
        // Given - Save user in database
        User savedUser = userRepository.save(testUser);

        // When & Then
        mockMvc.perform(get("/api/users/username/{username}", savedUser.getCredential().getUsername())
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.userId").value(savedUser.getUserId()))
                .andExpect(jsonPath("$.firstName").value("María José"))
                .andExpect(jsonPath("$.credential.username").value(savedUser.getCredential().getUsername()));
    }

    @Test
    @DisplayName("GET /api/users/username/{username} - Should return 400 when username not exists")
    void getUserByUsername_WhenUsernameNotExists_ShouldReturn400() throws Exception {
        // When & Then
        mockMvc.perform(get("/api/users/username/{username}", "nonexistent")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.msg").value("#### User with username: nonexistent not found! ####"));
    }

    @Test
    @DisplayName("PUT /api/users/{userId} - Should update existing user")
    void updateUser_WithValidData_ShouldUpdateUserAndReturn200() throws Exception {
        // Given - Save user in database
        User savedUser = userRepository.save(testUser);

        // Prepare updated data
        CredentialDto updatedCredentialDto = CredentialDto.builder()
                .credentialId(savedUser.getCredential().getCredentialId())
                .username("updateduser")
                .password("$2a$10$newEncodedPassword")
                .roleBasedAuthority(RoleBasedAuthority.ROLE_ADMIN)
                .isEnabled(true)
                .isAccountNonExpired(true)
                .isAccountNonLocked(true)
                .isCredentialsNonExpired(true)
                .build();

        UserDto updatedUserDto = UserDto.builder()
                .userId(savedUser.getUserId())
                .firstName("María Actualizada")
                .lastName("López Actualizada")
                .email("maria.updated@universidadean.edu.co")
                .phone("+57 315 999 8888")
                .imageUrl("https://cdn.universidadean.edu.co/avatars/maria-updated.jpg")
                .credentialDto(updatedCredentialDto)
                .build();

        // When & Then
        mockMvc.perform(put("/api/users/{userId}", savedUser.getUserId())
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updatedUserDto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.userId").value(savedUser.getUserId()))
                .andExpect(jsonPath("$.firstName").value("María Actualizada"))
                .andExpect(jsonPath("$.lastName").value("López Actualizada"))
                .andExpect(jsonPath("$.email").value("maria.updated@universidadean.edu.co"))
                .andExpect(jsonPath("$.credential.username").value("updateduser"))
                .andExpect(jsonPath("$.credential.roleBasedAuthority").value("ROLE_ADMIN"));

        // Verify user was updated in database
        User updatedUser = userRepository.findById(savedUser.getUserId()).orElseThrow();
        assertThat(updatedUser.getFirstName()).isEqualTo("María Actualizada");
        assertThat(updatedUser.getEmail()).isEqualTo("maria.updated@universidadean.edu.co");
        assertThat(updatedUser.getCredential().getUsername()).isEqualTo("updateduser");
        assertThat(updatedUser.getCredential().getRoleBasedAuthority()).isEqualTo(RoleBasedAuthority.ROLE_ADMIN);
    }

    @Test
    @DisplayName("PUT /api/users - Should update user without specific ID")
    void updateUserWithoutId_WithValidData_ShouldUpdateUser() throws Exception {
        // Given - Save user in database
        User savedUser = userRepository.save(testUser);

        UserDto updateDto = UserDto.builder()
                .userId(savedUser.getUserId())
                .firstName("María Sin ID")
                .lastName("López Sin ID")
                .email("maria.sinid@universidadean.edu.co")
                .phone("+57 316 111 2222")
                .imageUrl("https://cdn.universidadean.edu.co/avatars/maria-sinid.jpg")
                .credentialDto(CredentialDto.builder()
                        .credentialId(savedUser.getCredential().getCredentialId())
                        .username("marialopez2024")
                        .password("$2a$10$N.zmdr9k7uOCQb07YxkiNOhsqlQ5166rWa8rN5.4aDh7d6c8QWsma")
                        .roleBasedAuthority(RoleBasedAuthority.ROLE_USER)
                        .isEnabled(true)
                        .isAccountNonExpired(true)
                        .isAccountNonLocked(true)
                        .isCredentialsNonExpired(true)
                        .build())
                .build();

        // When & Then
        mockMvc.perform(put("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updateDto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.firstName").value("María Sin ID"));
    }

    @Test
    @DisplayName("DELETE /api/users/{userId} - Should delete existing user")
    void deleteUser_WhenUserExists_ShouldDeleteUserAndReturn200() throws Exception {
        // Given - Save user in database
        User savedUser = userRepository.save(testUser);
        assertThat(userRepository.findById(savedUser.getUserId())).isPresent();

        // When & Then
        mockMvc.perform(delete("/api/users/{userId}", savedUser.getUserId())
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk()) // API returns 200 with Boolean, not 204
                .andExpect(jsonPath("$").value(true));

        // Verify user was deleted from database
        assertThat(userRepository.findById(savedUser.getUserId())).isEmpty();
    }

    @Test
    @DisplayName("POST /api/users - Should validate required fields and return 400")
    void createUser_WithInvalidData_ShouldReturn400() throws Exception {
        // Given - Invalid user data (missing required fields)
        UserDto invalidUserDto = UserDto.builder()
                .firstName("") // Empty firstName
                .lastName("") // Empty lastName  
                .email("invalid-email") // Invalid email format
                .credentialDto(CredentialDto.builder()
                        .username("") // Empty username
                        .password("short") // Short password
                        .roleBasedAuthority(RoleBasedAuthority.ROLE_USER)
                        .isEnabled(true)
                        .isAccountNonExpired(true)
                        .isAccountNonLocked(true)
                        .isCredentialsNonExpired(true)
                        .build())
                .build();

        // When & Then - Should return 400 for validation errors
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(invalidUserDto)))
                .andExpect(status().isBadRequest());
    }

    @Test
    @DisplayName("Integration Test - Complete user lifecycle")
    void completeUserLifecycle_ShouldWorkEndToEnd() throws Exception {
        // 1. Create user
        MvcResult createResult = mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(testUserDto)))
                .andExpect(status().isCreated())
                .andReturn();

        String responseContent = createResult.getResponse().getContentAsString();
        UserDto createdUser = objectMapper.readValue(responseContent, UserDto.class);
        Integer userId = createdUser.getUserId();

        // 2. Get user by ID
        mockMvc.perform(get("/api/users/{userId}", userId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.firstName").value("Juan David"));

        // 3. Get user by username
        mockMvc.perform(get("/api/users/username/{username}", testUserDto.getCredentialDto().getUsername())
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.firstName").value("Juan David"));

        // 4. Update user
        testUserDto.setUserId(userId);
        testUserDto.setFirstName("Juan Actualizado");

        mockMvc.perform(put("/api/users/{userId}", userId)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(testUserDto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.firstName").value("Juan Actualizado"));

        // 5. Verify update persisted
        mockMvc.perform(get("/api/users/{userId}", userId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.firstName").value("Juan Actualizado"));

        // 6. Delete user
        mockMvc.perform(delete("/api/users/{userId}", userId))
                .andExpect(status().isNoContent());

        // 7. Verify user was deleted
        mockMvc.perform(get("/api/users/{userId}", userId))
                .andExpect(status().isNotFound());

        // Verify database state
        assertThat(userRepository.findById(userId)).isEmpty();
    }

    @Test
    @DisplayName("DEBUG - Simple user creation test")
    void debugCreateUser_ShouldWork() throws Exception {
        // Clear everything first
        userRepository.deleteAll();
        
        // Create simple DTO with unique data
        String uniqueUsername = "debug_" + System.currentTimeMillis();
        String uniqueEmail = "debug_" + System.currentTimeMillis() + "@test.com";
        
        CredentialDto credentialDto = CredentialDto.builder()
                .username(uniqueUsername)
                .password("$2a$10$N.zmdr9k7uOCQb07YxkiNOhsqlQ5166rWa8rN5.4aDh7d6c8QWsma")
                .roleBasedAuthority(RoleBasedAuthority.ROLE_USER)
                .isEnabled(true)
                .isAccountNonExpired(true)
                .isAccountNonLocked(true)
                .isCredentialsNonExpired(true)
                .build();

        UserDto debugUserDto = UserDto.builder()
                .firstName("Debug")
                .lastName("User")
                .email(uniqueEmail)
                .phone("+57 300 000 0000")
                .imageUrl("https://example.com/debug.jpg")
                .credentialDto(credentialDto)
                .build();

        // When & Then
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(debugUserDto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.firstName").value("Debug"));

        // Verify in database  
        List<User> users = userRepository.findAll();
        assertThat(users).hasSize(1);
        assertThat(users.get(0).getFirstName()).isEqualTo("Debug");
    }
}
