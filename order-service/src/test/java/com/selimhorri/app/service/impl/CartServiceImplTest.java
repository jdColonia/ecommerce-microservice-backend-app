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
import org.springframework.web.client.RestTemplate;

import com.selimhorri.app.constant.AppConstant;
import com.selimhorri.app.domain.Cart;
import com.selimhorri.app.dto.CartDto;
import com.selimhorri.app.dto.UserDto;
import com.selimhorri.app.exception.wrapper.CartNotFoundException;
import com.selimhorri.app.repository.CartRepository;

@ExtendWith(MockitoExtension.class)
@DisplayName("CartServiceImpl - Unit Tests")
class CartServiceImplTest {

    @Mock
    private CartRepository cartRepository;
    
    @Mock
    private RestTemplate restTemplate;

    @InjectMocks
    private CartServiceImpl cartService;

    private Cart testCart;
    private CartDto testCartDto;
    private UserDto testUserDto;

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

        testCart = Cart.builder()
                .cartId(1)
                .userId(1)
                .build();

        testCartDto = CartDto.builder()
                .cartId(1)
                .userId(1)
                .userDto(UserDto.builder().userId(1).build())
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando existen carritos - Debe retornar lista de CartDto enriquecida con UserDto")
    void findAll_WhenCartsExist_ShouldReturnEnrichedCartDtoList() {
        // Arrange
        List<Cart> carts = Arrays.asList(testCart);
        when(cartRepository.findAll()).thenReturn(carts);
        when(restTemplate.getForObject(
                AppConstant.DiscoveredDomainsApi.USER_SERVICE_API_URL + "/1",
                UserDto.class)).thenReturn(testUserDto);

        // Act
        List<CartDto> result = cartService.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals(testCart.getCartId(), result.get(0).getCartId());
        assertEquals(testCart.getUserId(), result.get(0).getUserId());
        assertEquals(testUserDto.getFirstName(), result.get(0).getUserDto().getFirstName());
        verify(cartRepository, times(1)).findAll();
        verify(restTemplate, times(1)).getForObject(
                AppConstant.DiscoveredDomainsApi.USER_SERVICE_API_URL + "/1",
                UserDto.class);
    }

    @Test
    @DisplayName("findAll - Cuando no existen carritos - Debe retornar lista vacía")
    void findAll_WhenNoCartsExist_ShouldReturnEmptyList() {
        // Arrange
        when(cartRepository.findAll()).thenReturn(Arrays.asList());

        // Act
        List<CartDto> result = cartService.findAll();

        // Assert
        assertNotNull(result);
        assertTrue(result.isEmpty());
        verify(cartRepository, times(1)).findAll();
        verify(restTemplate, never()).getForObject(anyString(), eq(UserDto.class));
    }

    @Test
    @DisplayName("findAll - Cuando RestTemplate lanza excepción - Debe propagar excepción")
    void findAll_WhenRestTemplateThrowsException_ShouldPropagateException() {
        // Arrange
        List<Cart> carts = Arrays.asList(testCart);
        when(cartRepository.findAll()).thenReturn(carts);
        when(restTemplate.getForObject(
                AppConstant.DiscoveredDomainsApi.USER_SERVICE_API_URL + "/1",
                UserDto.class)).thenThrow(new RuntimeException("Service unavailable"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> cartService.findAll());

        assertEquals("Service unavailable", exception.getMessage());
        verify(cartRepository, times(1)).findAll();
        verify(restTemplate, times(1)).getForObject(
                AppConstant.DiscoveredDomainsApi.USER_SERVICE_API_URL + "/1",
                UserDto.class);
    }

    @Test
    @DisplayName("findById - Cuando carrito existe - Debe retornar CartDto enriquecido con UserDto")
    void findById_WhenCartExists_ShouldReturnEnrichedCartDto() {
        // Arrange
        Integer cartId = 1;
        when(cartRepository.findById(cartId)).thenReturn(Optional.of(testCart));
        when(restTemplate.getForObject(
                AppConstant.DiscoveredDomainsApi.USER_SERVICE_API_URL + "/1",
                UserDto.class)).thenReturn(testUserDto);

        // Act
        CartDto result = cartService.findById(cartId);

        // Assert
        assertNotNull(result);
        assertEquals(testCart.getCartId(), result.getCartId());
        assertEquals(testCart.getUserId(), result.getUserId());
        assertEquals(testUserDto.getFirstName(), result.getUserDto().getFirstName());
        verify(cartRepository, times(1)).findById(cartId);
        verify(restTemplate, times(1)).getForObject(
                AppConstant.DiscoveredDomainsApi.USER_SERVICE_API_URL + "/1",
                UserDto.class);
    }

    @Test
    @DisplayName("findById - Cuando carrito no existe - Debe lanzar CartNotFoundException")
    void findById_WhenCartNotExists_ShouldThrowCartNotFoundException() {
        // Arrange
        Integer cartId = 999;
        when(cartRepository.findById(cartId)).thenReturn(Optional.empty());

        // Act & Assert
        CartNotFoundException exception = assertThrows(
                CartNotFoundException.class,
                () -> cartService.findById(cartId));

        assertTrue(exception.getMessage().contains("Cart with id: 999 not found"));
        verify(cartRepository, times(1)).findById(cartId);
        verify(restTemplate, never()).getForObject(anyString(), eq(UserDto.class));
    }

    @Test
    @DisplayName("findById - Cuando RestTemplate lanza excepción - Debe propagar excepción")
    void findById_WhenRestTemplateThrowsException_ShouldPropagateException() {
        // Arrange
        Integer cartId = 1;
        when(cartRepository.findById(cartId)).thenReturn(Optional.of(testCart));
        when(restTemplate.getForObject(
                AppConstant.DiscoveredDomainsApi.USER_SERVICE_API_URL + "/1",
                UserDto.class)).thenThrow(new RuntimeException("Service unavailable"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> cartService.findById(cartId));

        assertEquals("Service unavailable", exception.getMessage());
        verify(cartRepository, times(1)).findById(cartId);
        verify(restTemplate, times(1)).getForObject(
                AppConstant.DiscoveredDomainsApi.USER_SERVICE_API_URL + "/1",
                UserDto.class);
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar CartDto")
    void save_WhenValidData_ShouldSaveAndReturnCartDto() {
        // Arrange
        when(cartRepository.save(any(Cart.class))).thenReturn(testCart);

        // Act
        CartDto result = cartService.save(testCartDto);

        // Assert
        assertNotNull(result);
        assertEquals(testCart.getCartId(), result.getCartId());
        assertEquals(testCart.getUserId(), result.getUserId());
        verify(cartRepository, times(1)).save(any(Cart.class));
        verify(restTemplate, never()).getForObject(anyString(), eq(UserDto.class));
    }

    @Test
    @DisplayName("save - Cuando cartDto es null - Debe lanzar excepción")
    void save_WhenCartDtoIsNull_ShouldThrowException() {
        // Arrange
        CartDto nullCartDto = null;

        // Act & Assert
        assertThrows(
                NullPointerException.class,
                () -> cartService.save(nullCartDto));

        verify(cartRepository, never()).save(any(Cart.class));
    }

    @Test
    @DisplayName("save - Cuando userId es null - Debe guardar correctamente")
    void save_WhenUserIdIsNull_ShouldSaveCorrectly() {
        // Arrange
        CartDto cartDtoWithoutUser = CartDto.builder()
                .cartId(1)
                .userId(null)
                .build();
        Cart savedCart = Cart.builder()
                .cartId(1)
                .userId(null)
                .build();
        when(cartRepository.save(any(Cart.class))).thenReturn(savedCart);

        // Act
        CartDto result = cartService.save(cartDtoWithoutUser);

        // Assert
        assertNotNull(result);
        assertEquals(1, result.getCartId());
        assertNull(result.getUserId());
        verify(cartRepository, times(1)).save(any(Cart.class));
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar CartDto")
    void update_WhenValidData_ShouldUpdateAndReturnCartDto() {
        // Arrange
        CartDto updateDto = CartDto.builder()
                .cartId(1)
                .userId(2)
                .build();

        Cart updatedCart = Cart.builder()
                .cartId(1)
                .userId(2)
                .build();

        when(cartRepository.save(any(Cart.class))).thenReturn(updatedCart);

        // Act
        CartDto result = cartService.update(updateDto);

        // Assert
        assertNotNull(result);
        assertEquals(1, result.getCartId());
        assertEquals(2, result.getUserId());
        verify(cartRepository, times(1)).save(any(Cart.class));
    }

    @Test
    @DisplayName("update - Cuando se actualiza solo userId - Debe mantener cartId")
    void update_WhenOnlyUserIdUpdated_ShouldKeepCartId() {
        // Arrange
        CartDto updateDto = CartDto.builder()
                .cartId(1)
                .userId(99)
                .build();

        Cart expectedCart = Cart.builder()
                .cartId(1)
                .userId(99)
                .build();

        when(cartRepository.save(any(Cart.class))).thenReturn(expectedCart);

        // Act
        CartDto result = cartService.update(updateDto);

        // Assert
        assertNotNull(result);
        assertEquals(1, result.getCartId());
        assertEquals(99, result.getUserId());
        verify(cartRepository, times(1)).save(any(Cart.class));
    }

    @Test
    @DisplayName("update con cartId - Cuando carrito existe - Debe actualizar y retornar CartDto")
    void updateWithCartId_WhenCartExists_ShouldUpdateAndReturnCartDto() {
        // Arrange
        Integer cartId = 1;
        CartDto updateDto = CartDto.builder()
                .cartId(1)
                .userId(5)
                .build();

        when(cartRepository.findById(cartId)).thenReturn(Optional.of(testCart));
        when(restTemplate.getForObject(
                AppConstant.DiscoveredDomainsApi.USER_SERVICE_API_URL + "/1",
                UserDto.class)).thenReturn(testUserDto);

        Cart updatedCart = Cart.builder()
                .cartId(1)
                .userId(1)
                .build();
        when(cartRepository.save(any(Cart.class))).thenReturn(updatedCart);

        // Act
        CartDto result = cartService.update(cartId, updateDto);

        // Assert
        assertNotNull(result);
        assertEquals(1, result.getCartId());
        assertEquals(1, result.getUserId());
        verify(cartRepository, times(1)).findById(cartId);
        verify(cartRepository, times(1)).save(any(Cart.class));
        verify(restTemplate, times(1)).getForObject(
                AppConstant.DiscoveredDomainsApi.USER_SERVICE_API_URL + "/1",
                UserDto.class);
    }

    @Test
    @DisplayName("update con cartId - Cuando carrito no existe - Debe lanzar CartNotFoundException")
    void updateWithCartId_WhenCartNotExists_ShouldThrowCartNotFoundException() {
        // Arrange
        Integer cartId = 999;
        CartDto updateDto = CartDto.builder()
                .cartId(999)
                .userId(5)
                .build();

        when(cartRepository.findById(cartId)).thenReturn(Optional.empty());

        // Act & Assert
        CartNotFoundException exception = assertThrows(
                CartNotFoundException.class,
                () -> cartService.update(cartId, updateDto));

        assertTrue(exception.getMessage().contains("Cart with id: 999 not found"));
        verify(cartRepository, times(1)).findById(cartId);
        verify(cartRepository, never()).save(any(Cart.class));
        verify(restTemplate, never()).getForObject(anyString(), eq(UserDto.class));
    }

    @Test
    @DisplayName("deleteById - Cuando carrito existe - Debe eliminar sin excepción")
    void deleteById_WhenCartExists_ShouldDeleteWithoutException() {
        // Arrange
        Integer cartId = 1;
        doNothing().when(cartRepository).deleteById(cartId);

        // Act & Assert
        assertDoesNotThrow(() -> cartService.deleteById(cartId));
        verify(cartRepository, times(1)).deleteById(cartId);
    }

    @Test
    @DisplayName("deleteById - Cuando repository lanza excepción - Debe propagar excepción")
    void deleteById_WhenRepositoryThrowsException_ShouldPropagateException() {
        // Arrange
        Integer cartId = 1;
        doThrow(new RuntimeException("Database error")).when(cartRepository).deleteById(cartId);

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> cartService.deleteById(cartId));

        assertEquals("Database error", exception.getMessage());
        verify(cartRepository, times(1)).deleteById(cartId);
    }

    @Test
    @DisplayName("findAll - Cuando múltiples carritos con diferentes usuarios - Debe enriquecer todos correctamente")
    void findAll_WhenMultipleCartsWithDifferentUsers_ShouldEnrichAllCorrectly() {
        // Arrange
        Cart cart1 = Cart.builder().cartId(1).userId(1).build();
        Cart cart2 = Cart.builder().cartId(2).userId(2).build();
        List<Cart> carts = Arrays.asList(cart1, cart2);

        UserDto user1 = UserDto.builder().userId(1).firstName("Usuario1").build();
        UserDto user2 = UserDto.builder().userId(2).firstName("Usuario2").build();

        when(cartRepository.findAll()).thenReturn(carts);
        when(restTemplate.getForObject(
                AppConstant.DiscoveredDomainsApi.USER_SERVICE_API_URL + "/1",
                UserDto.class)).thenReturn(user1);
        when(restTemplate.getForObject(
                AppConstant.DiscoveredDomainsApi.USER_SERVICE_API_URL + "/2",
                UserDto.class)).thenReturn(user2);

        // Act
        List<CartDto> result = cartService.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(2, result.size());
        
        CartDto resultCart1 = result.stream()
                .filter(c -> c.getCartId().equals(1))
                .findFirst()
                .orElse(null);
        assertNotNull(resultCart1);
        assertEquals("Usuario1", resultCart1.getUserDto().getFirstName());

        CartDto resultCart2 = result.stream()
                .filter(c -> c.getCartId().equals(2))
                .findFirst()
                .orElse(null);
        assertNotNull(resultCart2);
        assertEquals("Usuario2", resultCart2.getUserDto().getFirstName());

        verify(cartRepository, times(1)).findAll();
        verify(restTemplate, times(1)).getForObject(
                AppConstant.DiscoveredDomainsApi.USER_SERVICE_API_URL + "/1",
                UserDto.class);
        verify(restTemplate, times(1)).getForObject(
                AppConstant.DiscoveredDomainsApi.USER_SERVICE_API_URL + "/2",
                UserDto.class);
    }
}
