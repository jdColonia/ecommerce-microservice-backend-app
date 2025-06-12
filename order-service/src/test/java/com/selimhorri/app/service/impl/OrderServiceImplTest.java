package com.selimhorri.app.service.impl;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

import java.time.LocalDateTime;
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

import com.selimhorri.app.domain.Cart;
import com.selimhorri.app.domain.Order;
import com.selimhorri.app.dto.CartDto;
import com.selimhorri.app.dto.OrderDto;
import com.selimhorri.app.exception.wrapper.OrderNotFoundException;
import com.selimhorri.app.repository.OrderRepository;

@ExtendWith(MockitoExtension.class)
@DisplayName("OrderServiceImpl - Unit Tests")
class OrderServiceImplTest {

    @Mock
    private OrderRepository orderRepository;

    @InjectMocks
    private OrderServiceImpl orderService;

    private Order testOrder;
    private OrderDto testOrderDto;
    private Cart testCart;
    private CartDto testCartDto;

    @BeforeEach
    void setUp() {
        testCart = Cart.builder()
                .cartId(1)
                .build();

        testCartDto = CartDto.builder()
                .cartId(1)
                .build();

        testOrder = Order.builder()
                .orderId(1)
                .orderDate(LocalDateTime.now())
                .orderDesc("Test order description")
                .orderFee(29.99)
                .cart(testCart)
                .build();

        testOrderDto = OrderDto.builder()
                .orderId(1)
                .orderDate(LocalDateTime.now())
                .orderDesc("Test order description")
                .orderFee(29.99)
                .cartDto(testCartDto)
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando existen órdenes - Debe retornar lista de OrderDto")
    void findAll_WhenOrdersExist_ShouldReturnOrderDtoList() {
        // Arrange
        List<Order> orders = Arrays.asList(testOrder);
        when(orderRepository.findAll()).thenReturn(orders);

        // Act
        List<OrderDto> result = orderService.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals(testOrder.getOrderId(), result.get(0).getOrderId());
        assertEquals(testOrder.getOrderDesc(), result.get(0).getOrderDesc());
        verify(orderRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("findAll - Cuando no existen órdenes - Debe retornar lista vacía")
    void findAll_WhenNoOrdersExist_ShouldReturnEmptyList() {
        // Arrange
        when(orderRepository.findAll()).thenReturn(Arrays.asList());

        // Act
        List<OrderDto> result = orderService.findAll();

        // Assert
        assertNotNull(result);
        assertTrue(result.isEmpty());
        verify(orderRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("findById - Cuando orden existe - Debe retornar OrderDto")
    void findById_WhenOrderExists_ShouldReturnOrderDto() {
        // Arrange
        Integer orderId = 1;
        when(orderRepository.findById(orderId)).thenReturn(Optional.of(testOrder));

        // Act
        OrderDto result = orderService.findById(orderId);

        // Assert
        assertNotNull(result);
        assertEquals(testOrder.getOrderId(), result.getOrderId());
        assertEquals(testOrder.getOrderDesc(), result.getOrderDesc());
        assertEquals(testOrder.getOrderFee(), result.getOrderFee());
        verify(orderRepository, times(1)).findById(orderId);
    }

    @Test
    @DisplayName("findById - Cuando orden no existe - Debe lanzar OrderNotFoundException")
    void findById_WhenOrderNotExists_ShouldThrowOrderNotFoundException() {
        // Arrange
        Integer orderId = 999;
        when(orderRepository.findById(orderId)).thenReturn(Optional.empty());

        // Act & Assert
        OrderNotFoundException exception = assertThrows(
                OrderNotFoundException.class,
                () -> orderService.findById(orderId));

        assertTrue(exception.getMessage().contains("Order with id: 999 not found"));
        verify(orderRepository, times(1)).findById(orderId);
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar OrderDto")
    void save_WhenValidData_ShouldSaveAndReturnOrderDto() {
        // Arrange
        when(orderRepository.save(any(Order.class))).thenReturn(testOrder);

        // Act
        OrderDto result = orderService.save(testOrderDto);

        // Assert
        assertNotNull(result);
        assertEquals(testOrder.getOrderId(), result.getOrderId());
        assertEquals(testOrder.getOrderDesc(), result.getOrderDesc());
        assertEquals(testOrder.getOrderFee(), result.getOrderFee());
        verify(orderRepository, times(1)).save(any(Order.class));
    }

    @Test
    @DisplayName("save - Cuando fee es cero - Debe guardar correctamente")
    void save_WhenFeeIsZero_ShouldSaveCorrectly() {
        // Arrange
        testOrderDto.setOrderFee(0.0);
        testOrder.setOrderFee(0.0);
        when(orderRepository.save(any(Order.class))).thenReturn(testOrder);

        // Act
        OrderDto result = orderService.save(testOrderDto);

        // Assert
        assertNotNull(result);
        assertEquals(0.0, result.getOrderFee());
        verify(orderRepository, times(1)).save(any(Order.class));
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar OrderDto")
    void update_WhenValidData_ShouldUpdateAndReturnOrderDto() {
        // Arrange
        testOrderDto.setOrderDesc("Updated order description");
        testOrderDto.setOrderFee(49.99);

        Order updatedOrder = Order.builder()
                .orderId(1)
                .orderDate(LocalDateTime.now())
                .orderDesc("Updated order description")
                .orderFee(49.99)
                .cart(testCart)
                .build();

        when(orderRepository.save(any(Order.class))).thenReturn(updatedOrder);

        // Act
        OrderDto result = orderService.update(testOrderDto);

        // Assert
        assertNotNull(result);
        assertEquals("Updated order description", result.getOrderDesc());
        assertEquals(49.99, result.getOrderFee());
        verify(orderRepository, times(1)).save(any(Order.class));
    }

    @Test
    @DisplayName("update con orderId - Cuando orden existe - Debe actualizar y retornar OrderDto")
    void updateWithOrderId_WhenOrderExists_ShouldUpdateAndReturnOrderDto() {
        // Arrange
        Integer orderId = 1;
        OrderDto updateDto = OrderDto.builder()
                .orderId(1)
                .orderDate(LocalDateTime.now())
                .orderDesc("Updated description with orderId")
                .orderFee(75.50)
                .cartDto(testCartDto)
                .build();

        Order updatedOrder = Order.builder()
                .orderId(1)
                .orderDate(LocalDateTime.now())
                .orderDesc("Updated description with orderId")
                .orderFee(75.50)
                .cart(testCart)
                .build();

        when(orderRepository.findById(orderId)).thenReturn(Optional.of(testOrder));
        when(orderRepository.save(any(Order.class))).thenReturn(updatedOrder);

        // Act
        OrderDto result = orderService.update(orderId, updateDto);

        // Assert
        assertNotNull(result);
        assertEquals("Updated description with orderId", result.getOrderDesc());
        assertEquals(75.50, result.getOrderFee());
        verify(orderRepository, times(1)).findById(orderId);
        verify(orderRepository, times(1)).save(any(Order.class));
    }

    @Test
    @DisplayName("update con orderId - Cuando orden no existe - Debe lanzar OrderNotFoundException")
    void updateWithOrderId_WhenOrderNotExists_ShouldThrowOrderNotFoundException() {
        // Arrange
        Integer orderId = 999;
        OrderDto updateDto = OrderDto.builder()
                .orderId(999)
                .orderDesc("Updated description")
                .orderFee(50.0)
                .cartDto(testCartDto)
                .build();

        when(orderRepository.findById(orderId)).thenReturn(Optional.empty());

        // Act & Assert
        OrderNotFoundException exception = assertThrows(
                OrderNotFoundException.class,
                () -> orderService.update(orderId, updateDto));

        assertTrue(exception.getMessage().contains("Order with id: 999 not found"));
        verify(orderRepository, times(1)).findById(orderId);
        verify(orderRepository, never()).save(any(Order.class));
    }

    @Test
    @DisplayName("update - Cuando se actualiza solo la descripción - Debe mantener otros campos")
    void update_WhenOnlyDescriptionUpdated_ShouldKeepOtherFields() {
        // Arrange
        OrderDto updateDto = OrderDto.builder()
                .orderId(1)
                .orderDate(testOrderDto.getOrderDate())
                .orderDesc("Only description changed")
                .orderFee(testOrderDto.getOrderFee())
                .cartDto(testCartDto)
                .build();

        Order expectedOrder = Order.builder()
                .orderId(1)
                .orderDate(testOrder.getOrderDate())
                .orderDesc("Only description changed")
                .orderFee(testOrder.getOrderFee())
                .cart(testCart)
                .build();

        when(orderRepository.save(any(Order.class))).thenReturn(expectedOrder);

        // Act
        OrderDto result = orderService.update(updateDto);

        // Assert
        assertNotNull(result);
        assertEquals("Only description changed", result.getOrderDesc());
        assertEquals(testOrder.getOrderFee(), result.getOrderFee());
        assertEquals(testOrder.getOrderId(), result.getOrderId());
        verify(orderRepository, times(1)).save(any(Order.class));
    }

    @Test
    @DisplayName("update - Cuando se actualiza fee a cero - Debe actualizar correctamente")
    void update_WhenFeeUpdatedToZero_ShouldUpdateCorrectly() {
        // Arrange
        OrderDto updateDto = OrderDto.builder()
                .orderId(1)
                .orderDate(testOrderDto.getOrderDate())
                .orderDesc(testOrderDto.getOrderDesc())
                .orderFee(0.0)
                .cartDto(testCartDto)
                .build();

        Order expectedOrder = Order.builder()
                .orderId(1)
                .orderDate(testOrder.getOrderDate())
                .orderDesc(testOrder.getOrderDesc())
                .orderFee(0.0)
                .cart(testCart)
                .build();

        when(orderRepository.save(any(Order.class))).thenReturn(expectedOrder);

        // Act
        OrderDto result = orderService.update(updateDto);

        // Assert
        assertNotNull(result);
        assertEquals(0.0, result.getOrderFee());
        assertEquals(testOrder.getOrderDesc(), result.getOrderDesc());
        verify(orderRepository, times(1)).save(any(Order.class));
    }

    @Test
    @DisplayName("deleteById - Cuando orden existe - Debe eliminar sin excepción")
    void deleteById_WhenOrderExists_ShouldDeleteWithoutException() {
        // Arrange
        Integer orderId = 1;
        when(orderRepository.findById(orderId)).thenReturn(Optional.of(testOrder));
        doNothing().when(orderRepository).delete(any(Order.class));

        // Act & Assert
        assertDoesNotThrow(() -> orderService.deleteById(orderId));
        verify(orderRepository, times(1)).findById(orderId);
        verify(orderRepository, times(1)).delete(any(Order.class));
    }
}
