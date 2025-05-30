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

import com.selimhorri.app.domain.Payment;
import com.selimhorri.app.domain.PaymentStatus;
import com.selimhorri.app.dto.OrderDto;
import com.selimhorri.app.dto.PaymentDto;
import com.selimhorri.app.exception.wrapper.PaymentNotFoundException;
import com.selimhorri.app.repository.PaymentRepository;

@ExtendWith(MockitoExtension.class)
@DisplayName("PaymentServiceImpl - Unit Tests")
class PaymentServiceImplTest {

    @Mock
    private PaymentRepository paymentRepository;

    @Mock
    private RestTemplate restTemplate;

    @InjectMocks
    private PaymentServiceImpl paymentService;

    private Payment testPayment;
    private PaymentDto testPaymentDto;
    private OrderDto testOrderDto;

    @BeforeEach
    void setUp() {
        // Arrange - Configurar datos de prueba
        testOrderDto = OrderDto.builder()
                .orderId(1)
                .build();

        testPayment = Payment.builder()
                .paymentId(1)
                .orderId(1)
                .isPayed(true)
                .paymentStatus(PaymentStatus.COMPLETED)
                .build();

        testPaymentDto = PaymentDto.builder()
                .paymentId(1)
                .isPayed(true)
                .paymentStatus(PaymentStatus.COMPLETED)
                .orderDto(testOrderDto)
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando existen pagos - Debe retornar lista de PaymentDto")
    void findAll_WhenPaymentsExist_ShouldReturnPaymentDtoList() {
        // Arrange
        List<Payment> payments = Arrays.asList(testPayment);
        when(paymentRepository.findAll()).thenReturn(payments);
        when(restTemplate.getForObject(anyString(), eq(OrderDto.class))).thenReturn(testOrderDto);

        // Act
        List<PaymentDto> result = paymentService.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals(testPayment.getPaymentId(), result.get(0).getPaymentId());
        assertEquals(testPayment.getIsPayed(), result.get(0).getIsPayed());
        assertEquals(testPayment.getPaymentStatus(), result.get(0).getPaymentStatus());
        verify(paymentRepository, times(1)).findAll();
        verify(restTemplate, times(1)).getForObject(anyString(), eq(OrderDto.class));
    }

    @Test
    @DisplayName("findAll - Cuando no existen pagos - Debe retornar lista vacía")
    void findAll_WhenNoPaymentsExist_ShouldReturnEmptyList() {
        // Arrange
        when(paymentRepository.findAll()).thenReturn(Arrays.asList());

        // Act
        List<PaymentDto> result = paymentService.findAll();

        // Assert
        assertNotNull(result);
        assertTrue(result.isEmpty());
        verify(paymentRepository, times(1)).findAll();
        verify(restTemplate, never()).getForObject(anyString(), eq(OrderDto.class));
    }

    @Test
    @DisplayName("findById - Cuando pago existe - Debe retornar PaymentDto")
    void findById_WhenPaymentExists_ShouldReturnPaymentDto() {
        // Arrange
        Integer paymentId = 1;
        when(paymentRepository.findById(paymentId)).thenReturn(Optional.of(testPayment));
        when(restTemplate.getForObject(anyString(), eq(OrderDto.class))).thenReturn(testOrderDto);

        // Act
        PaymentDto result = paymentService.findById(paymentId);

        // Assert
        assertNotNull(result);
        assertEquals(testPayment.getPaymentId(), result.getPaymentId());
        assertEquals(testPayment.getIsPayed(), result.getIsPayed());
        assertEquals(testPayment.getPaymentStatus(), result.getPaymentStatus());
        assertEquals(testOrderDto.getOrderId(), result.getOrderDto().getOrderId());
        verify(paymentRepository, times(1)).findById(paymentId);
        verify(restTemplate, times(1)).getForObject(anyString(), eq(OrderDto.class));
    }

    @Test
    @DisplayName("findById - Cuando pago no existe - Debe lanzar PaymentNotFoundException")
    void findById_WhenPaymentNotExists_ShouldThrowPaymentNotFoundException() {
        // Arrange
        Integer paymentId = 999;
        when(paymentRepository.findById(paymentId)).thenReturn(Optional.empty());

        // Act & Assert
        PaymentNotFoundException exception = assertThrows(
                PaymentNotFoundException.class,
                () -> paymentService.findById(paymentId));

        assertTrue(exception.getMessage().contains("Payment with id: 999 not found"));
        verify(paymentRepository, times(1)).findById(paymentId);
        verify(restTemplate, never()).getForObject(anyString(), eq(OrderDto.class));
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar PaymentDto")
    void save_WhenValidData_ShouldSaveAndReturnPaymentDto() {
        // Arrange
        when(paymentRepository.save(any(Payment.class))).thenReturn(testPayment);

        // Act
        PaymentDto result = paymentService.save(testPaymentDto);

        // Assert
        assertNotNull(result);
        assertEquals(testPayment.getPaymentId(), result.getPaymentId());
        assertEquals(testPayment.getIsPayed(), result.getIsPayed());
        assertEquals(testPayment.getPaymentStatus(), result.getPaymentStatus());
        verify(paymentRepository, times(1)).save(any(Payment.class));
    }

    @Test
    @DisplayName("save - Cuando pago no está pagado - Debe guardar correctamente")
    void save_WhenPaymentNotPaid_ShouldSaveCorrectly() {
        // Arrange
        testPaymentDto.setIsPayed(false);
        testPayment.setIsPayed(false);
        when(paymentRepository.save(any(Payment.class))).thenReturn(testPayment);

        // Act
        PaymentDto result = paymentService.save(testPaymentDto);

        // Assert
        assertNotNull(result);
        assertFalse(result.getIsPayed());
        verify(paymentRepository, times(1)).save(any(Payment.class));
    }

    @Test
    @DisplayName("save - Cuando estado es NOT_STARTED - Debe guardar correctamente")
    void save_WhenStatusNotStarted_ShouldSaveCorrectly() {
        // Arrange
        testPaymentDto.setPaymentStatus(PaymentStatus.NOT_STARTED);
        testPayment.setPaymentStatus(PaymentStatus.NOT_STARTED);
        when(paymentRepository.save(any(Payment.class))).thenReturn(testPayment);

        // Act
        PaymentDto result = paymentService.save(testPaymentDto);

        // Assert
        assertNotNull(result);
        assertEquals(PaymentStatus.NOT_STARTED, result.getPaymentStatus());
        verify(paymentRepository, times(1)).save(any(Payment.class));
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar PaymentDto")
    void update_WhenValidData_ShouldUpdateAndReturnPaymentDto() {
        // Arrange
        testPaymentDto.setIsPayed(false);
        testPaymentDto.setPaymentStatus(PaymentStatus.IN_PROGRESS);

        Payment updatedPayment = Payment.builder()
                .paymentId(1)
                .orderId(1)
                .isPayed(false)
                .paymentStatus(PaymentStatus.IN_PROGRESS)
                .build();

        when(paymentRepository.save(any(Payment.class))).thenReturn(updatedPayment);

        // Act
        PaymentDto result = paymentService.update(testPaymentDto);

        // Assert
        assertNotNull(result);
        assertFalse(result.getIsPayed());
        assertEquals(PaymentStatus.IN_PROGRESS, result.getPaymentStatus());
        verify(paymentRepository, times(1)).save(any(Payment.class));
    }

    @Test
    @DisplayName("update - Cuando se marca como pagado - Debe actualizar correctamente")
    void update_WhenMarkedAsPaid_ShouldUpdateCorrectly() {
        // Arrange
        testPaymentDto.setIsPayed(true);
        testPaymentDto.setPaymentStatus(PaymentStatus.COMPLETED);

        Payment updatedPayment = Payment.builder()
                .paymentId(1)
                .orderId(1)
                .isPayed(true)
                .paymentStatus(PaymentStatus.COMPLETED)
                .build();

        when(paymentRepository.save(any(Payment.class))).thenReturn(updatedPayment);

        // Act
        PaymentDto result = paymentService.update(testPaymentDto);

        // Assert
        assertNotNull(result);
        assertTrue(result.getIsPayed());
        assertEquals(PaymentStatus.COMPLETED, result.getPaymentStatus());
        verify(paymentRepository, times(1)).save(any(Payment.class));
    }

    @Test
    @DisplayName("deleteById - Cuando pago existe - Debe eliminar sin excepción")
    void deleteById_WhenPaymentExists_ShouldDeleteWithoutException() {
        // Arrange
        Integer paymentId = 1;
        doNothing().when(paymentRepository).deleteById(paymentId);

        // Act & Assert
        assertDoesNotThrow(() -> paymentService.deleteById(paymentId));
        verify(paymentRepository, times(1)).deleteById(paymentId);
    }

    @Test
    @DisplayName("deleteById - Cuando se intenta eliminar - Debe llamar al repositorio")
    void deleteById_WhenCalled_ShouldCallRepository() {
        // Arrange
        Integer paymentId = 999;
        doNothing().when(paymentRepository).deleteById(paymentId);

        // Act
        paymentService.deleteById(paymentId);

        // Assert
        verify(paymentRepository, times(1)).deleteById(paymentId);
    }
}
