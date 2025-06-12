package com.selimhorri.app.business.orderItem.controller;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.util.Arrays;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.ResponseEntity;

import com.selimhorri.app.business.orderItem.model.OrderItemDto;
import com.selimhorri.app.business.orderItem.model.OrderItemId;
import com.selimhorri.app.business.orderItem.model.response.OrderItemOrderItemServiceDtoCollectionResponse;
import com.selimhorri.app.business.orderItem.service.OrderItemClientService;

@ExtendWith(MockitoExtension.class)
@DisplayName("OrderItemController - Unit Tests")
class OrderItemControllerTest {

    @Mock
    private OrderItemClientService orderItemClientService;

    @InjectMocks
    private OrderItemController orderItemController;

    private OrderItemDto testOrderItemDto;
    private OrderItemOrderItemServiceDtoCollectionResponse testCollectionResponse;

    @BeforeEach
    void setUp() {
        testOrderItemDto = OrderItemDto.builder()
                .productId(1)
                .orderId(2)
                .orderedQuantity(3)
                .build();

        testCollectionResponse = OrderItemOrderItemServiceDtoCollectionResponse.builder()
                .collection(Arrays.asList(testOrderItemDto))
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando servicio retorna items de orden - Debe retornar colección de items")
    void findAll_WhenServiceReturnsOrderItems_ShouldReturnOrderItemCollection() {
        // Arrange
        ResponseEntity<OrderItemOrderItemServiceDtoCollectionResponse> serviceResponse = ResponseEntity
                .ok(testCollectionResponse);
        when(orderItemClientService.findAll()).thenReturn(serviceResponse);

        // Act
        ResponseEntity<OrderItemOrderItemServiceDtoCollectionResponse> result = orderItemController.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertNotNull(result.getBody());
        assertEquals(1, result.getBody().getCollection().size());
        verify(orderItemClientService, times(1)).findAll();
    }

    @Test
    @DisplayName("findById - Cuando item de orden existe - Debe retornar item")
    void findById_WhenOrderItemExists_ShouldReturnOrderItem() {
        // Arrange
        String orderId = "1";
        String productId = "2";
        OrderItemId expectedOrderItemId = new OrderItemId(Integer.parseInt(productId), Integer.parseInt(orderId));
        ResponseEntity<OrderItemDto> serviceResponse = ResponseEntity.ok(testOrderItemDto);
        when(orderItemClientService.findById(expectedOrderItemId)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<OrderItemDto> result = orderItemController.findById(orderId, productId);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals(1, result.getBody().getProductId());
        assertEquals(3, result.getBody().getOrderedQuantity());
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar item de orden")
    void save_WhenValidData_ShouldSaveAndReturnOrderItem() {
        // Arrange
        ResponseEntity<OrderItemDto> serviceResponse = ResponseEntity.ok(testOrderItemDto);
        when(orderItemClientService.save(testOrderItemDto)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<OrderItemDto> result = orderItemController.save(testOrderItemDto);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals(3, result.getBody().getOrderedQuantity());
        verify(orderItemClientService, times(1)).save(testOrderItemDto);
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar item de orden")
    void update_WhenValidData_ShouldUpdateAndReturnOrderItem() {
        // Arrange
        ResponseEntity<OrderItemDto> serviceResponse = ResponseEntity.ok(testOrderItemDto);
        when(orderItemClientService.update(testOrderItemDto)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<OrderItemDto> result = orderItemController.update(testOrderItemDto);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        verify(orderItemClientService, times(1)).update(testOrderItemDto);
    }

    @Test
    @DisplayName("deleteById - Cuando item de orden existe - Debe eliminar y retornar true")
    void deleteById_WhenOrderItemExists_ShouldDeleteAndReturnTrue() {
        // Arrange
        String orderId = "1";
        String productId = "2";
        OrderItemId expectedOrderItemId = new OrderItemId(Integer.parseInt(orderId), Integer.parseInt(productId));
        ResponseEntity<Boolean> serviceResponse = ResponseEntity.ok(true);
        when(orderItemClientService.deleteById(expectedOrderItemId)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<Boolean> result = orderItemController.deleteById(orderId, productId);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertTrue(result.getBody());
    }
}
