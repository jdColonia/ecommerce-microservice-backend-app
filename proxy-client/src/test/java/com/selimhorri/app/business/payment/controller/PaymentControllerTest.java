package com.selimhorri.app.business.payment.controller;

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

import com.selimhorri.app.business.payment.model.PaymentDto;
import com.selimhorri.app.business.payment.model.PaymentStatus;
import com.selimhorri.app.business.payment.model.response.PaymentPaymentServiceDtoCollectionResponse;
import com.selimhorri.app.business.payment.service.PaymentClientService;

@ExtendWith(MockitoExtension.class)
@DisplayName("PaymentController - Unit Tests")
class PaymentControllerTest {

    @Mock
    private PaymentClientService paymentClientService;

    @InjectMocks
    private PaymentController paymentController;

    private PaymentDto testPaymentDto;
    private PaymentPaymentServiceDtoCollectionResponse testCollectionResponse;

    @BeforeEach
    void setUp() {
        testPaymentDto = PaymentDto.builder()
                .paymentId(1)
                .isPayed(true)
                .paymentStatus(PaymentStatus.COMPLETED)
                .build();

        testCollectionResponse = PaymentPaymentServiceDtoCollectionResponse.builder()
                .collection(Arrays.asList(testPaymentDto))
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando servicio retorna pagos - Debe retornar colección de pagos")
    void findAll_WhenServiceReturnsPayments_ShouldReturnPaymentCollection() {
        // Arrange
        ResponseEntity<PaymentPaymentServiceDtoCollectionResponse> serviceResponse = ResponseEntity
                .ok(testCollectionResponse);
        when(paymentClientService.findAll()).thenReturn(serviceResponse);

        // Act
        ResponseEntity<PaymentPaymentServiceDtoCollectionResponse> result = paymentController.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertNotNull(result.getBody());
        assertEquals(1, result.getBody().getCollection().size());
        verify(paymentClientService, times(1)).findAll();
    }

    @Test
    @DisplayName("findById - Cuando pago existe - Debe retornar pago")
    void findById_WhenPaymentExists_ShouldReturnPayment() {
        // Arrange
        String paymentId = "1";
        ResponseEntity<PaymentDto> serviceResponse = ResponseEntity.ok(testPaymentDto);
        when(paymentClientService.findById(paymentId)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<PaymentDto> result = paymentController.findById(paymentId);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals(1, result.getBody().getPaymentId());
        assertEquals(PaymentStatus.COMPLETED, result.getBody().getPaymentStatus());
        verify(paymentClientService, times(1)).findById(paymentId);
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar pago")
    void save_WhenValidData_ShouldSaveAndReturnPayment() {
        // Arrange
        ResponseEntity<PaymentDto> serviceResponse = ResponseEntity.ok(testPaymentDto);
        when(paymentClientService.save(testPaymentDto)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<PaymentDto> result = paymentController.save(testPaymentDto);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals(PaymentStatus.COMPLETED, result.getBody().getPaymentStatus());
        verify(paymentClientService, times(1)).save(testPaymentDto);
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar pago")
    void update_WhenValidData_ShouldUpdateAndReturnPayment() {
        // Arrange
        ResponseEntity<PaymentDto> serviceResponse = ResponseEntity.ok(testPaymentDto);
        when(paymentClientService.update(testPaymentDto)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<PaymentDto> result = paymentController.update(testPaymentDto);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals(PaymentStatus.COMPLETED, result.getBody().getPaymentStatus());
        verify(paymentClientService, times(1)).update(testPaymentDto);
    }

    @Test
    @DisplayName("deleteById - Cuando pago existe - Debe eliminar y retornar true")
    void deleteById_WhenPaymentExists_ShouldDeleteAndReturnTrue() {
        // Arrange
        String paymentId = "1";
        ResponseEntity<Boolean> serviceResponse = ResponseEntity.ok(true);
        when(paymentClientService.deleteById(paymentId)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<Boolean> result = paymentController.deleteById(paymentId);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertTrue(result.getBody());
        verify(paymentClientService, times(1)).deleteById(paymentId);
    }
}
