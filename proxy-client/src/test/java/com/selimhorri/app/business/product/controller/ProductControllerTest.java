package com.selimhorri.app.business.product.controller;

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

import com.selimhorri.app.business.product.model.ProductDto;
import com.selimhorri.app.business.product.model.response.ProductProductServiceCollectionDtoResponse;
import com.selimhorri.app.business.product.service.ProductClientService;

@ExtendWith(MockitoExtension.class)
@DisplayName("ProductController - Unit Tests")
class ProductControllerTest {

    @Mock
    private ProductClientService productClientService;

    @InjectMocks
    private ProductController productController;

    private ProductDto testProductDto;
    private ProductProductServiceCollectionDtoResponse testCollectionResponse;

    @BeforeEach
    void setUp() {
        testProductDto = ProductDto.builder()
                .productId(1)
                .productTitle("Smartphone Samsung Galaxy")
                .imageUrl("https://example.com/smartphone.jpg")
                .sku("SAMS-GAL-001")
                .priceUnit(899.99)
                .quantity(50)
                .build();

        testCollectionResponse = ProductProductServiceCollectionDtoResponse.builder()
                .collection(Arrays.asList(testProductDto))
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando servicio retorna productos - Debe retornar colección de productos")
    void findAll_WhenServiceReturnsProducts_ShouldReturnProductCollection() {
        // Arrange
        ResponseEntity<ProductProductServiceCollectionDtoResponse> serviceResponse = ResponseEntity
                .ok(testCollectionResponse);
        when(productClientService.findAll()).thenReturn(serviceResponse);

        // Act
        ResponseEntity<ProductProductServiceCollectionDtoResponse> result = productController.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertNotNull(result.getBody());
        assertEquals(1, result.getBody().getCollection().size());
        verify(productClientService, times(1)).findAll();
    }

    @Test
    @DisplayName("findAll - Cuando servicio lanza excepción - Debe propagar excepción")
    void findAll_WhenServiceThrowsException_ShouldPropagateException() {
        // Arrange
        when(productClientService.findAll())
                .thenThrow(new RuntimeException("Product service unavailable"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> productController.findAll());

        assertEquals("Product service unavailable", exception.getMessage());
        verify(productClientService, times(1)).findAll();
    }

    @Test
    @DisplayName("findById - Cuando producto existe - Debe retornar producto")
    void findById_WhenProductExists_ShouldReturnProduct() {
        // Arrange
        String productId = "1";
        ResponseEntity<ProductDto> serviceResponse = ResponseEntity.ok(testProductDto);
        when(productClientService.findById(productId)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<ProductDto> result = productController.findById(productId);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals(1, result.getBody().getProductId());
        assertEquals("Smartphone Samsung Galaxy", result.getBody().getProductTitle());
        verify(productClientService, times(1)).findById(productId);
    }

    @Test
    @DisplayName("findById - Cuando producto no existe - Debe propagar excepción del servicio")
    void findById_WhenProductNotExists_ShouldPropagateServiceException() {
        // Arrange
        String productId = "999";
        when(productClientService.findById(productId))
                .thenThrow(new RuntimeException("Product not found"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> productController.findById(productId));

        assertEquals("Product not found", exception.getMessage());
        verify(productClientService, times(1)).findById(productId);
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar producto")
    void save_WhenValidData_ShouldSaveAndReturnProduct() {
        // Arrange
        ResponseEntity<ProductDto> serviceResponse = ResponseEntity.ok(testProductDto);
        when(productClientService.save(testProductDto)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<ProductDto> result = productController.save(testProductDto);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals("Smartphone Samsung Galaxy", result.getBody().getProductTitle());
        verify(productClientService, times(1)).save(testProductDto);
    }

    @Test
    @DisplayName("save - Cuando servicio lanza excepción - Debe propagar excepción")
    void save_WhenServiceThrowsException_ShouldPropagateException() {
        // Arrange
        when(productClientService.save(testProductDto))
                .thenThrow(new RuntimeException("Product save failed"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> productController.save(testProductDto));

        assertEquals("Product save failed", exception.getMessage());
        verify(productClientService, times(1)).save(testProductDto);
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar producto")
    void update_WhenValidData_ShouldUpdateAndReturnProduct() {
        // Arrange
        ResponseEntity<ProductDto> serviceResponse = ResponseEntity.ok(testProductDto);
        when(productClientService.update(testProductDto)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<ProductDto> result = productController.update(testProductDto);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals("Smartphone Samsung Galaxy", result.getBody().getProductTitle());
        verify(productClientService, times(1)).update(testProductDto);
    }

    @Test
    @DisplayName("update con productId - Cuando datos válidos - Debe actualizar y retornar producto")
    void updateWithProductId_WhenValidData_ShouldUpdateAndReturnProduct() {
        // Arrange
        String productId = "1";
        ResponseEntity<ProductDto> serviceResponse = ResponseEntity.ok(testProductDto);
        when(productClientService.update(productId, testProductDto)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<ProductDto> result = productController.update(productId, testProductDto);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals("Smartphone Samsung Galaxy", result.getBody().getProductTitle());
        verify(productClientService, times(1)).update(productId, testProductDto);
    }

    @Test
    @DisplayName("update con productId - Cuando producto no existe - Debe propagar excepción")
    void updateWithProductId_WhenProductNotExists_ShouldPropagateException() {
        // Arrange
        String productId = "999";
        when(productClientService.update(productId, testProductDto))
                .thenThrow(new RuntimeException("Product not found for update"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> productController.update(productId, testProductDto));

        assertEquals("Product not found for update", exception.getMessage());
        verify(productClientService, times(1)).update(productId, testProductDto);
    }

    @Test
    @DisplayName("deleteById - Cuando producto existe - Debe eliminar y retornar true")
    void deleteById_WhenProductExists_ShouldDeleteAndReturnTrue() {
        // Arrange
        String productId = "1";
        ResponseEntity<Boolean> serviceResponse = ResponseEntity.ok(true);
        when(productClientService.deleteById(productId)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<Boolean> result = productController.deleteById(productId);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertTrue(result.getBody());
        verify(productClientService, times(1)).deleteById(productId);
    }

    @Test
    @DisplayName("deleteById - Cuando producto no existe - Debe propagar excepción")
    void deleteById_WhenProductNotExists_ShouldPropagateException() {
        // Arrange
        String productId = "999";
        when(productClientService.deleteById(productId))
                .thenThrow(new RuntimeException("Product not found for deletion"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> productController.deleteById(productId));

        assertEquals("Product not found for deletion", exception.getMessage());
        verify(productClientService, times(1)).deleteById(productId);
    }

    @Test
    @DisplayName("save - Cuando precio es cero - Debe manejar correctamente")
    void save_WhenPriceIsZero_ShouldHandleCorrectly() {
        // Arrange
        ProductDto zeroPrice = ProductDto.builder()
                .productId(2)
                .productTitle("Producto Gratuito")
                .priceUnit(0.0)
                .quantity(100)
                .build();

        ResponseEntity<ProductDto> serviceResponse = ResponseEntity.ok(zeroPrice);
        when(productClientService.save(zeroPrice)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<ProductDto> result = productController.save(zeroPrice);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals(0.0, result.getBody().getPriceUnit());
        assertEquals("Producto Gratuito", result.getBody().getProductTitle());
        verify(productClientService, times(1)).save(zeroPrice);
    }

    @Test
    @DisplayName("save - Cuando cantidad es negativa - Debe manejar según servicio")
    void save_WhenQuantityIsNegative_ShouldHandleAccordingToService() {
        // Arrange
        ProductDto negativeQuantity = ProductDto.builder()
                .productId(3)
                .productTitle("Producto Agotado")
                .priceUnit(50.0)
                .quantity(-5)
                .build();

        ResponseEntity<ProductDto> serviceResponse = ResponseEntity.ok(negativeQuantity);
        when(productClientService.save(negativeQuantity)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<ProductDto> result = productController.save(negativeQuantity);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        assertEquals(-5, result.getBody().getQuantity());
        verify(productClientService, times(1)).save(negativeQuantity);
    }

    @Test
    @DisplayName("findById - Cuando productId es null - Debe manejar como parámetro válido")
    void findById_WhenProductIdIsNull_ShouldHandleAsValidParameter() {
        // Arrange
        String productId = null;
        ResponseEntity<ProductDto> serviceResponse = ResponseEntity.ok(testProductDto);
        when(productClientService.findById(productId)).thenReturn(serviceResponse);

        // Act
        ResponseEntity<ProductDto> result = productController.findById(productId);

        // Assert
        assertNotNull(result);
        assertEquals(200, result.getStatusCodeValue());
        verify(productClientService, times(1)).findById(productId);
    }

    @Test
    @DisplayName("save - Cuando productDto es null - Debe propagar excepción del servicio")
    void save_WhenProductDtoIsNull_ShouldPropagateServiceException() {
        // Arrange
        when(productClientService.save(null))
                .thenThrow(new RuntimeException("ProductDto cannot be null"));

        // Act & Assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> productController.save(null));

        assertEquals("ProductDto cannot be null", exception.getMessage());
        verify(productClientService, times(1)).save(null);
    }
}
