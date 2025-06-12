package com.selimhorri.app.business.order.controller;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.time.LocalDateTime;
import java.util.Arrays;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.ResponseEntity;

import com.selimhorri.app.business.order.model.OrderDto;
import com.selimhorri.app.business.order.model.response.OrderOrderServiceDtoCollectionResponse;
import com.selimhorri.app.business.order.service.OrderClientService;

@ExtendWith(MockitoExtension.class)
@DisplayName("OrderController - Unit Tests")
class OrderControllerTest {

    @Mock
    private OrderClientService orderClientService;

    @InjectMocks
    private OrderController orderController;

    private OrderDto testOrderDto;
    private OrderOrderServiceDtoCollectionResponse testCollectionResponse;

    @BeforeEach
    void setUp() {
        testOrderDto = OrderDto.builder()
                .orderId(1)
                .orderDate(LocalDateTime.now())
                .orderDesc("Pedido de teléfonos móviles")
                .orderFee(1799.98)
                .build();

        testCollectionResponse = OrderOrderServiceDtoCollectionResponse.builder()
                .collection(Arrays.asList(testOrderDto))
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando servicio retorna órdenes - Debe retornar colección de órdenes")
    void findAll_WhenServiceReturnsOrders_ShouldReturnOrderCollection() {
        // Arrange
        ResponseEntity<OrderOrderServiceDtoCollectionResponse> serviceResponse = ResponseEntity
                .ok(testCollectionResponse);
        when(orderClientService.findAll()).thenReturn(serviceResponse);

        // Act
        ResponseEntity<OrderOrderServiceDtoCollectionResponse> result = orderController.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertNotNull(result.getBody());
        assertEquals(1, result.getBody().getCollection().size());
        verify(orderClientService, times(1)).findAll();
    }

    @Test
    @DisplayName("findById - Cuando orden existe - Debe retornar orden")
    void findById_WhenOrderExists_ShouldReturnOrder() {
        // Arrange
        String orderId = "1";
        ResponseEntity<OrderDto> serviceResponse = ResponseEntity.ok(testOrderDto);
        when(orderClientService.findById(orderId)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<OrderDto> result = orderController.findById(orderId);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals(1, result.getBody().getOrderId());
        assertEquals("Pedido de teléfonos móviles", result.getBody().getOrderDesc());
        verify(orderClientService, times(1)).findById(orderId);
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar orden")
    void save_WhenValidData_ShouldSaveAndReturnOrder() {
        // Arrange
        ResponseEntity<OrderDto> serviceResponse = ResponseEntity.ok(testOrderDto);
        when(orderClientService.save(testOrderDto)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<OrderDto> result = orderController.save(testOrderDto);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals("Pedido de teléfonos móviles", result.getBody().getOrderDesc());
        verify(orderClientService, times(1)).save(testOrderDto);
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar orden")
    void update_WhenValidData_ShouldUpdateAndReturnOrder() {
        // Arrange
        ResponseEntity<OrderDto> serviceResponse = ResponseEntity.ok(testOrderDto);
        when(orderClientService.update(testOrderDto)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<OrderDto> result = orderController.update(testOrderDto);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals("Pedido de teléfonos móviles", result.getBody().getOrderDesc());
        verify(orderClientService, times(1)).update(testOrderDto);
    }

    @Test
    @DisplayName("deleteById - Cuando orden existe - Debe eliminar y retornar true")
    void deleteById_WhenOrderExists_ShouldDeleteAndReturnTrue() {
        // Arrange
        String orderId = "1";
        ResponseEntity<Boolean> serviceResponse = ResponseEntity.ok(true);
        when(orderClientService.deleteById(orderId)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<Boolean> result = orderController.deleteById(orderId);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertTrue(result.getBody());
        verify(orderClientService, times(1)).deleteById(orderId);
    }
}
