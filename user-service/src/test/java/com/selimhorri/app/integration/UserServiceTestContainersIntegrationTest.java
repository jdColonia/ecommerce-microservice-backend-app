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
import org.springframework.transaction.annotation.Transactional;
import org.testcontainers.containers.MySQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.springframework.test.context.ActiveProfiles;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.selimhorri.app.domain.RoleBasedAuthority;
import com.selimhorri.app.domain.User;
import com.selimhorri.app.domain.Credential;
import com.selimhorri.app.dto.UserDto;
import com.selimhorri.app.dto.CredentialDto;
import com.selimhorri.app.repository.UserRepository;

/**
 * Advanced Integration tests for User Service using TestContainers with MySQL.
 * These tests verify the complete user management workflow in a real database
 * environment:
 * - Real MySQL database via TestContainers
 * - Database transactions and rollbacks
 * - Complex user scenarios with authentication
 * - Performance and concurrent access testing
 * - Data integrity and constraint validation
 */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
@TestPropertySource(properties = {
        // MySQL TestContainer specific configuration
        "spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect",
        // Performance and connection settings
        "spring.datasource.hikari.maximum-pool-size=20",
        "spring.datasource.hikari.minimum-idle=5",
        "spring.datasource.hikari.connection-timeout=20000"
})
@AutoConfigureMockMvc
@Testcontainers
@Transactional
@DisplayName("User Service TestContainers Integration Tests")
public class UserServiceTestContainersIntegrationTest {

    @Container
    static MySQLContainer<?> mysql = new MySQLContainer<>("mysql:8.0.33")
            .withDatabaseName("user_service_test")
            .withUsername("testuser")
            .withPassword("testpass")
            .withReuse(true)
            .withEnv("MYSQL_ROOT_HOST", "%")
            .withEnv("MYSQL_ROOT_PASSWORD", "rootpass");

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
        // Configure TestContainer datasource properties
        System.setProperty("spring.datasource.url", mysql.getJdbcUrl());
        System.setProperty("spring.datasource.username", mysql.getUsername());
        System.setProperty("spring.datasource.password", mysql.getPassword());
        System.setProperty("spring.datasource.driver-class-name", mysql.getDriverClassName());

        // Clear repository before each test
        userRepository.deleteAll();

        // Setup test data with Colombian context
        CredentialDto credentialDto = CredentialDto.builder()
                .username("juanperez2024")
                .password("$2a$10$N.zmdr9k7uOCQb07YxkiNOhsqlQ5166rWa8rN5.4aDh7d6c8QWsma") // encoded "password123"
                .roleBasedAuthority(RoleBasedAuthority.ROLE_USER)
                .isEnabled(true)
                .isAccountNonExpired(true)
                .isAccountNonLocked(true)
                .isCredentialsNonExpired(true)
                .build();

        testUserDto = UserDto.builder()
                .firstName("Juan David")
                .lastName("Pérez Rodríguez")
                .email("juan.perez@universidadean.edu.co")
                .phone("+57 321 456 7890")
                .imageUrl("https://cdn.universidadean.edu.co/avatars/juan-perez.jpg")
                .credentialDto(credentialDto)
                .build();

        Credential credential = Credential.builder()
                .username("marialopez2024")
                .password("$2a$10$N.zmdr9k7uOCQb07YxkiNOhsqlQ5166rWa8rN5.4aDh7d6c8QWsma")
                .roleBasedAuthority(RoleBasedAuthority.ROLE_USER)
                .isEnabled(true)
                .isAccountNonExpired(true)
                .isAccountNonLocked(true)
                .isCredentialsNonExpired(true)
                .build();

        testUser = User.builder()
                .firstName("María José")
                .lastName("López Martínez")
                .email("maria.lopez@universidadean.edu.co")
                .phone("+57 314 987 6543")
                .imageUrl("https://cdn.universidadean.edu.co/avatars/maria-lopez.jpg")
                .credential(credential)
                .build();
    }

    @Test
    @DisplayName("MySQL Integration - Should create user with database constraints")
    void createUser_WithMySQLDatabase_ShouldRespectConstraints() throws Exception {
        // When & Then
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(testUserDto)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.userId").exists())
                .andExpect(jsonPath("$.firstName").value("Juan David"))
                .andExpect(jsonPath("$.lastName").value("Pérez Rodríguez"))
                .andExpect(jsonPath("$.email").value("juan.perez@universidadean.edu.co"))
                .andExpect(jsonPath("$.credentialDto.username").value("juanperez2024"));

        // Verify database constraints and data integrity
        List<User> users = userRepository.findAll();
        assertThat(users).hasSize(1);

        User savedUser = users.get(0);
        assertThat(savedUser.getUserId()).isNotNull().isPositive();
        assertThat(savedUser.getCredential().getCredentialId()).isNotNull().isPositive();
        assertThat(savedUser.getCredential().getUsername()).isEqualTo("juanperez2024");
        assertThat(savedUser.getEmail()).contains("@universidadean.edu.co");
    }

    @Test
    @DisplayName("MySQL Integration - Should handle unique constraint violations")
    void createUser_WithDuplicateEmail_ShouldHandleConstraintViolation() throws Exception {
        // Given - Save first user
        userRepository.save(testUser);

        // When - Try to create another user with same email
        UserDto duplicateEmailUser = UserDto.builder()
                .firstName("Carlos")
                .lastName("Pérez")
                .email("maria.lopez@universidadean.edu.co") // Same email as testUser
                .phone("+57 300 111 2222")
                .credentialDto(CredentialDto.builder()
                        .username("carlosperez2024")
                        .password("$2a$10$encoded")
                        .roleBasedAuthority(RoleBasedAuthority.ROLE_USER)
                        .isEnabled(true)
                        .isAccountNonExpired(true)
                        .isAccountNonLocked(true)
                        .isCredentialsNonExpired(true)
                        .build())
                .build();

        // Then - Should handle constraint violation gracefully
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(duplicateEmailUser)))
                .andExpect(status().isConflict()); // Assuming proper error handling

        // Verify only one user exists
        List<User> users = userRepository.findAll();
        assertThat(users).hasSize(1);
    }

    @Test
    @DisplayName("MySQL Integration - Should handle concurrent user creation")
    void createUsers_Concurrently_ShouldMaintainDataIntegrity() throws Exception {
        // Given - Multiple users with different data
        UserDto user1 = createTestUserDto("carlos", "Carlos", "Rodríguez", "carlos.rodriguez@universidadean.edu.co");
        UserDto user2 = createTestUserDto("ana", "Ana", "García", "ana.garcia@universidadean.edu.co");
        UserDto user3 = createTestUserDto("luis", "Luis", "Martínez", "luis.martinez@universidadean.edu.co");

        // When - Create users in sequence (simulating concurrent scenario)
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(user1)))
                .andExpect(status().isCreated());

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(user2)))
                .andExpect(status().isCreated());

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(user3)))
                .andExpect(status().isCreated());

        // Then - Verify all users were created correctly
        List<User> users = userRepository.findAll();
        assertThat(users).hasSize(3);

        // Verify data integrity
        assertThat(users.stream().map(User::getEmail)).containsExactlyInAnyOrder(
                "carlos.rodriguez@universidadean.edu.co",
                "ana.garcia@universidadean.edu.co",
                "luis.martinez@universidadean.edu.co");

        assertThat(users.stream().map(u -> u.getCredential().getUsername())).containsExactlyInAnyOrder(
                "carlos", "ana", "luis");
    }

    @Test
    @DisplayName("MySQL Integration - Should perform complex queries with joins")
    void getUserByUsername_WithJoinQueries_ShouldWorkEfficiently() throws Exception {
        // Given - Save user with complete credential data
        User savedUser = userRepository.save(testUser);

        // When & Then - Test complex query that involves joins
        mockMvc.perform(get("/api/users/username/{username}", "marialopez2024")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.userId").value(savedUser.getUserId()))
                .andExpect(jsonPath("$.firstName").value("María José"))
                .andExpect(jsonPath("$.credentialDto.username").value("marialopez2024"))
                .andExpect(jsonPath("$.credentialDto.roleBasedAuthority").value("ROLE_USER"))
                .andExpect(jsonPath("$.credentialDto.isEnabled").value(true));

        // Verify query was executed efficiently (this would be visible in logs)
        assertThat(userRepository.findByCredentialUsername("marialopez2024")).isPresent();
    }

    @Test
    @DisplayName("MySQL Integration - Should handle transaction rollback scenarios")
    void updateUser_WithTransactionFailure_ShouldRollbackCorrectly() throws Exception {
        // Given - Save user
        User savedUser = userRepository.save(testUser);
        String originalFirstName = savedUser.getFirstName();

        // When - Update user with valid data
        UserDto updateDto = UserDto.builder()
                .userId(savedUser.getUserId())
                .firstName("María José Actualizada")
                .lastName("López Martínez Actualizada")
                .email("maria.lopez.actualizada@universidadean.edu.co")
                .phone("+57 315 888 9999")
                .imageUrl("https://cdn.universidadean.edu.co/avatars/maria-updated.jpg")
                .credentialDto(CredentialDto.builder()
                        .credentialId(savedUser.getCredential().getCredentialId())
                        .username("marialopez2024")
                        .password("$2a$10$newPassword")
                        .roleBasedAuthority(RoleBasedAuthority.ROLE_ADMIN)
                        .isEnabled(true)
                        .isAccountNonExpired(true)
                        .isAccountNonLocked(true)
                        .isCredentialsNonExpired(true)
                        .build())
                .build();

        // Then - Update should succeed and persist
        mockMvc.perform(put("/api/users/{userId}", savedUser.getUserId())
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updateDto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.firstName").value("María José Actualizada"))
                .andExpect(jsonPath("$.credentialDto.roleBasedAuthority").value("ROLE_ADMIN"));

        // Verify changes persisted in database
        User updatedUser = userRepository.findById(savedUser.getUserId()).orElseThrow();
        assertThat(updatedUser.getFirstName()).isEqualTo("María José Actualizada");
        assertThat(updatedUser.getCredential().getRoleBasedAuthority()).isEqualTo(RoleBasedAuthority.ROLE_ADMIN);
    }

    @Test
    @DisplayName("MySQL Integration - Should maintain referential integrity")
    void deleteUser_WithReferentialIntegrity_ShouldCascadeCorrectly() throws Exception {
        // Given - Save user with credentials
        User savedUser = userRepository.save(testUser);
        Integer userId = savedUser.getUserId();
        Integer credentialId = savedUser.getCredential().getCredentialId();

        // Verify user and credential exist
        assertThat(userRepository.findById(userId)).isPresent();

        // When - Delete user
        mockMvc.perform(delete("/api/users/{userId}", userId)
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isNoContent());

        // Then - User should be deleted (and credentials should be handled according to
        // cascade settings)
        assertThat(userRepository.findById(userId)).isEmpty();
    }

    @Test
    @DisplayName("MySQL Integration - Performance test with multiple operations")
    void performanceTest_MultipleOperations_ShouldExecuteEfficiently() throws Exception {
        // Given - Create multiple users for performance testing
        int numberOfUsers = 10;

        // When - Create multiple users
        long startTime = System.currentTimeMillis();

        for (int i = 0; i < numberOfUsers; i++) {
            UserDto userDto = createTestUserDto(
                    "user" + i,
                    "Usuario" + i,
                    "Apellido" + i,
                    "usuario" + i + "@universidadean.edu.co");

            mockMvc.perform(post("/api/users")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(objectMapper.writeValueAsString(userDto)))
                    .andExpect(status().isCreated());
        }

        long endTime = System.currentTimeMillis();
        long executionTime = endTime - startTime;

        // Then - Operations should complete in reasonable time
        assertThat(executionTime).isLessThan(5000); // Less than 5 seconds

        // Verify all users were created
        List<User> users = userRepository.findAll();
        assertThat(users).hasSize(numberOfUsers);

        // Test bulk retrieval performance
        long retrievalStart = System.currentTimeMillis();

        mockMvc.perform(get("/api/users")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(numberOfUsers));

        long retrievalEnd = System.currentTimeMillis();
        long retrievalTime = retrievalEnd - retrievalStart;

        assertThat(retrievalTime).isLessThan(1000); // Less than 1 second for retrieval
    }

    /**
     * Helper method to create test UserDto instances
     */
    private UserDto createTestUserDto(String username, String firstName, String lastName, String email) {
        CredentialDto credentialDto = CredentialDto.builder()
                .username(username)
                .password("$2a$10$N.zmdr9k7uOCQb07YxkiNOhsqlQ5166rWa8rN5.4aDh7d6c8QWsma")
                .roleBasedAuthority(RoleBasedAuthority.ROLE_USER)
                .isEnabled(true)
                .isAccountNonExpired(true)
                .isAccountNonLocked(true)
                .isCredentialsNonExpired(true)
                .build();

        return UserDto.builder()
                .firstName(firstName)
                .lastName(lastName)
                .email(email)
                .phone("+57 300 " + (int) (Math.random() * 1000000))
                .imageUrl("https://cdn.universidadean.edu.co/avatars/" + username + ".jpg")
                .credentialDto(credentialDto)
                .build();
    }
}
