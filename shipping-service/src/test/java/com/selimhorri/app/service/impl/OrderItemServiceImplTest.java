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

import com.selimhorri.app.domain.OrderItem;
import com.selimhorri.app.domain.id.OrderItemId;
import com.selimhorri.app.dto.OrderDto;
import com.selimhorri.app.dto.OrderItemDto;
import com.selimhorri.app.dto.ProductDto;
import com.selimhorri.app.exception.wrapper.OrderItemNotFoundException;
import com.selimhorri.app.repository.OrderItemRepository;

@ExtendWith(MockitoExtension.class)
@DisplayName("OrderItemServiceImpl - Unit Tests")
class OrderItemServiceImplTest {

    @Mock
    private OrderItemRepository orderItemRepository;

    @Mock
    private RestTemplate restTemplate;

    @InjectMocks
    private OrderItemServiceImpl orderItemService;

    private OrderItem testOrderItem;
    private OrderItemDto testOrderItemDto;
    private OrderItemId testOrderItemId;
    private ProductDto testProductDto;
    private OrderDto testOrderDto;

    @BeforeEach
    void setUp() {
        testOrderItemId = new OrderItemId(1, 1);

        testProductDto = ProductDto.builder()
                .productId(1)
                .build();

        testOrderDto = OrderDto.builder()
                .orderId(1)
                .build();

        testOrderItem = OrderItem.builder()
                .productId(1)
                .orderId(1)
                .orderedQuantity(5)
                .build();

        testOrderItemDto = OrderItemDto.builder()
                .productId(1)
                .orderId(1)
                .orderedQuantity(5)
                .productDto(testProductDto)
                .orderDto(testOrderDto)
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando existen elementos de orden - Debe retornar lista de OrderItemDto")
    void findAll_WhenOrderItemsExist_ShouldReturnOrderItemDtoList() {
        // Arrange
        List<OrderItem> orderItems = Arrays.asList(testOrderItem);
        when(orderItemRepository.findAll()).thenReturn(orderItems);
        when(restTemplate.getForObject(contains("product-service"), eq(ProductDto.class))).thenReturn(testProductDto);
        when(restTemplate.getForObject(contains("order-service"), eq(OrderDto.class))).thenReturn(testOrderDto);

        // Act
        List<OrderItemDto> result = orderItemService.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals(testOrderItem.getProductId(), result.get(0).getProductId());
        assertEquals(testOrderItem.getOrderId(), result.get(0).getOrderId());
        assertEquals(testOrderItem.getOrderedQuantity(), result.get(0).getOrderedQuantity());
        verify(orderItemRepository, times(1)).findAll();
        verify(restTemplate, times(1)).getForObject(contains("product-service"), eq(ProductDto.class));
        verify(restTemplate, times(1)).getForObject(contains("order-service"), eq(OrderDto.class));
    }

    @Test
    @DisplayName("findAll - Cuando no existen elementos de orden - Debe retornar lista vacía")
    void findAll_WhenNoOrderItemsExist_ShouldReturnEmptyList() {
        // Arrange
        when(orderItemRepository.findAll()).thenReturn(Arrays.asList());

        // Act
        List<OrderItemDto> result = orderItemService.findAll();

        // Assert
        assertNotNull(result);
        assertTrue(result.isEmpty());
        verify(orderItemRepository, times(1)).findAll();
        verify(restTemplate, never()).getForObject(anyString(), eq(ProductDto.class));
        verify(restTemplate, never()).getForObject(anyString(), eq(OrderDto.class));
    }

    @Test
    @DisplayName("findById - Cuando elemento de orden existe - Debe retornar OrderItemDto")
    void findById_WhenOrderItemExists_ShouldReturnOrderItemDto() {
        // Arrange
        when(orderItemRepository.findById(any())).thenReturn(Optional.of(testOrderItem));
        when(restTemplate.getForObject(contains("product-service"), eq(ProductDto.class))).thenReturn(testProductDto);
        when(restTemplate.getForObject(contains("order-service"), eq(OrderDto.class))).thenReturn(testOrderDto);

        // Act
        OrderItemDto result = orderItemService.findById(testOrderItemId);

        // Assert
        assertNotNull(result);
        assertEquals(testOrderItem.getProductId(), result.getProductId());
        assertEquals(testOrderItem.getOrderId(), result.getOrderId());
        assertEquals(testOrderItem.getOrderedQuantity(), result.getOrderedQuantity());
        verify(orderItemRepository, times(1)).findById(any());
        verify(restTemplate, times(1)).getForObject(contains("product-service"), eq(ProductDto.class));
        verify(restTemplate, times(1)).getForObject(contains("order-service"), eq(OrderDto.class));
    }

    @Test
    @DisplayName("findById - Cuando elemento de orden no existe - Debe lanzar OrderItemNotFoundException")
    void findById_WhenOrderItemNotExists_ShouldThrowOrderItemNotFoundException() {
        // Arrange
        when(orderItemRepository.findById(any())).thenReturn(Optional.empty());

        // Act & Assert
        OrderItemNotFoundException exception = assertThrows(
                OrderItemNotFoundException.class,
                () -> orderItemService.findById(testOrderItemId));

        assertTrue(exception.getMessage().contains("OrderItem with id:"));
        verify(orderItemRepository, times(1)).findById(any());
        verify(restTemplate, never()).getForObject(anyString(), eq(ProductDto.class));
        verify(restTemplate, never()).getForObject(anyString(), eq(OrderDto.class));
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar OrderItemDto")
    void save_WhenValidData_ShouldSaveAndReturnOrderItemDto() {
        // Arrange
        when(orderItemRepository.save(any(OrderItem.class))).thenReturn(testOrderItem);

        // Act
        OrderItemDto result = orderItemService.save(testOrderItemDto);

        // Assert
        assertNotNull(result);
        assertEquals(testOrderItem.getProductId(), result.getProductId());
        assertEquals(testOrderItem.getOrderId(), result.getOrderId());
        assertEquals(testOrderItem.getOrderedQuantity(), result.getOrderedQuantity());
        verify(orderItemRepository, times(1)).save(any(OrderItem.class));
    }

    @Test
    @DisplayName("save - Cuando cantidad es cero - Debe guardar correctamente")
    void save_WhenQuantityIsZero_ShouldSaveCorrectly() {
        // Arrange
        testOrderItemDto.setOrderedQuantity(0);
        testOrderItem.setOrderedQuantity(0);
        when(orderItemRepository.save(any(OrderItem.class))).thenReturn(testOrderItem);

        // Act
        OrderItemDto result = orderItemService.save(testOrderItemDto);

        // Assert
        assertNotNull(result);
        assertEquals(0, result.getOrderedQuantity());
        verify(orderItemRepository, times(1)).save(any(OrderItem.class));
    }

    @Test
    @DisplayName("save - Cuando cantidad es mayor - Debe guardar correctamente")
    void save_WhenLargeQuantity_ShouldSaveCorrectly() {
        // Arrange
        testOrderItemDto.setOrderedQuantity(100);
        testOrderItem.setOrderedQuantity(100);
        when(orderItemRepository.save(any(OrderItem.class))).thenReturn(testOrderItem);

        // Act
        OrderItemDto result = orderItemService.save(testOrderItemDto);

        // Assert
        assertNotNull(result);
        assertEquals(100, result.getOrderedQuantity());
        verify(orderItemRepository, times(1)).save(any(OrderItem.class));
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar OrderItemDto")
    void update_WhenValidData_ShouldUpdateAndReturnOrderItemDto() {
        // Arrange
        testOrderItemDto.setOrderedQuantity(10);

        OrderItem updatedOrderItem = OrderItem.builder()
                .productId(1)
                .orderId(1)
                .orderedQuantity(10)
                .build();

        when(orderItemRepository.save(any(OrderItem.class))).thenReturn(updatedOrderItem);

        // Act
        OrderItemDto result = orderItemService.update(testOrderItemDto);

        // Assert
        assertNotNull(result);
        assertEquals(10, result.getOrderedQuantity());
        verify(orderItemRepository, times(1)).save(any(OrderItem.class));
    }

    @Test
    @DisplayName("update - Cuando se actualiza cantidad a cero - Debe actualizar correctamente")
    void update_WhenQuantityUpdatedToZero_ShouldUpdateCorrectly() {
        // Arrange
        testOrderItemDto.setOrderedQuantity(0);

        OrderItem updatedOrderItem = OrderItem.builder()
                .productId(1)
                .orderId(1)
                .orderedQuantity(0)
                .build();

        when(orderItemRepository.save(any(OrderItem.class))).thenReturn(updatedOrderItem);

        // Act
        OrderItemDto result = orderItemService.update(testOrderItemDto);

        // Assert
        assertNotNull(result);
        assertEquals(0, result.getOrderedQuantity());
        verify(orderItemRepository, times(1)).save(any(OrderItem.class));
    }

    @Test
    @DisplayName("deleteById - Cuando elemento de orden existe - Debe eliminar sin excepción")
    void deleteById_WhenOrderItemExists_ShouldDeleteWithoutException() {
        // Arrange
        doNothing().when(orderItemRepository).deleteById(testOrderItemId);

        // Act & Assert
        assertDoesNotThrow(() -> orderItemService.deleteById(testOrderItemId));
        verify(orderItemRepository, times(1)).deleteById(testOrderItemId);
    }

    @Test
    @DisplayName("deleteById - Cuando se intenta eliminar - Debe llamar al repositorio")
    void deleteById_WhenCalled_ShouldCallRepository() {
        // Arrange
        OrderItemId orderItemId = new OrderItemId(999, 999);
        doNothing().when(orderItemRepository).deleteById(orderItemId);

        // Act
        orderItemService.deleteById(orderItemId);

        // Assert
        verify(orderItemRepository, times(1)).deleteById(orderItemId);
    }
}
