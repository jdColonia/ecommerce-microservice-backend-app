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

import com.selimhorri.app.domain.Product;
import com.selimhorri.app.domain.Category;
import com.selimhorri.app.dto.ProductDto;
import com.selimhorri.app.dto.CategoryDto;
import com.selimhorri.app.exception.wrapper.ProductNotFoundException;
import com.selimhorri.app.repository.ProductRepository;

@ExtendWith(MockitoExtension.class)
@DisplayName("ProductServiceImpl - Unit Tests")
class ProductServiceImplTest {

    @Mock
    private ProductRepository productRepository;

    @InjectMocks
    private ProductServiceImpl productService;

    private Product testProduct;
    private ProductDto testProductDto;
    private Category testCategory;
    private CategoryDto testCategoryDto;

    @BeforeEach
    void setUp() {
        testCategory = Category.builder()
                .categoryId(1)
                .categoryTitle("Electronics")
                .imageUrl("https://example.com/electronics.jpg")
                .build();

        testProduct = Product.builder()
                .productId(1)
                .productTitle("iPhone 13")
                .imageUrl("https://example.com/iphone13.jpg")
                .sku("IPHONE13-001")
                .priceUnit(999.99)
                .quantity(50)
                .category(testCategory)
                .build();

        testCategoryDto = CategoryDto.builder()
                .categoryId(1)
                .categoryTitle("Electronics")
                .imageUrl("https://example.com/electronics.jpg")
                .build();

        testProductDto = ProductDto.builder()
                .productId(1)
                .productTitle("iPhone 13")
                .imageUrl("https://example.com/iphone13.jpg")
                .sku("IPHONE13-001")
                .priceUnit(999.99)
                .quantity(50)
                .categoryDto(testCategoryDto)
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando existen productos - Debe retornar lista de ProductDto")
    void findAll_WhenProductsExist_ShouldReturnProductDtoList() {
        // Arrange
        List<Product> products = Arrays.asList(testProduct);
        when(productRepository.findAll()).thenReturn(products);

        // Act
        List<ProductDto> result = productService.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals(testProduct.getProductId(), result.get(0).getProductId());
        assertEquals(testProduct.getProductTitle(), result.get(0).getProductTitle());
        assertEquals(testProduct.getSku(), result.get(0).getSku());
        assertEquals(testProduct.getPriceUnit(), result.get(0).getPriceUnit());
        verify(productRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("findAll - Cuando no existen productos - Debe retornar lista vacía")
    void findAll_WhenNoProductsExist_ShouldReturnEmptyList() {
        // Arrange
        when(productRepository.findAll()).thenReturn(Arrays.asList());

        // Act
        List<ProductDto> result = productService.findAll();

        // Assert
        assertNotNull(result);
        assertTrue(result.isEmpty());
        verify(productRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("findById - Cuando producto existe - Debe retornar ProductDto")
    void findById_WhenProductExists_ShouldReturnProductDto() {
        // Arrange
        Integer productId = 1;
        when(productRepository.findById(productId)).thenReturn(Optional.of(testProduct));

        // Act
        ProductDto result = productService.findById(productId);

        // Assert
        assertNotNull(result);
        assertEquals(testProduct.getProductId(), result.getProductId());
        assertEquals(testProduct.getProductTitle(), result.getProductTitle());
        assertEquals(testProduct.getSku(), result.getSku());
        assertEquals(testProduct.getPriceUnit(), result.getPriceUnit());
        assertEquals(testProduct.getQuantity(), result.getQuantity());
        verify(productRepository, times(1)).findById(productId);
    }

    @Test
    @DisplayName("findById - Cuando producto no existe - Debe lanzar ProductNotFoundException")
    void findById_WhenProductNotExists_ShouldThrowProductNotFoundException() {
        // Arrange
        Integer productId = 999;
        when(productRepository.findById(productId)).thenReturn(Optional.empty());

        // Act & Assert
        ProductNotFoundException exception = assertThrows(
                ProductNotFoundException.class,
                () -> productService.findById(productId));

        assertTrue(exception.getMessage().contains("Product with id: 999 not found"));
        verify(productRepository, times(1)).findById(productId);
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar ProductDto")
    void save_WhenValidData_ShouldSaveAndReturnProductDto() {
        // Arrange
        when(productRepository.save(any(Product.class))).thenReturn(testProduct);

        // Act
        ProductDto result = productService.save(testProductDto);

        // Assert
        assertNotNull(result);
        assertEquals(testProduct.getProductId(), result.getProductId());
        assertEquals(testProduct.getProductTitle(), result.getProductTitle());
        assertEquals(testProduct.getSku(), result.getSku());
        assertEquals(testProduct.getPriceUnit(), result.getPriceUnit());
        verify(productRepository, times(1)).save(any(Product.class));
    }

    @Test
    @DisplayName("save - Cuando precio es cero - Debe guardar correctamente")
    void save_WhenPriceIsZero_ShouldSaveCorrectly() {
        // Arrange
        testProductDto.setPriceUnit(0.0);
        testProduct.setPriceUnit(0.0);
        when(productRepository.save(any(Product.class))).thenReturn(testProduct);

        // Act
        ProductDto result = productService.save(testProductDto);

        // Assert
        assertNotNull(result);
        assertEquals(0.0, result.getPriceUnit());
        verify(productRepository, times(1)).save(any(Product.class));
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar ProductDto")
    void update_WhenValidData_ShouldUpdateAndReturnProductDto() {
        // Arrange
        testProductDto.setProductTitle("iPhone 14");
        testProductDto.setPriceUnit(1199.99);

        Product updatedProduct = Product.builder()
                .productId(1)
                .productTitle("iPhone 14")
                .imageUrl("https://example.com/iphone13.jpg")
                .sku("IPHONE13-001")
                .priceUnit(1199.99)
                .quantity(50)
                .category(testCategory)
                .build();

        when(productRepository.save(any(Product.class))).thenReturn(updatedProduct);

        // Act
        ProductDto result = productService.update(testProductDto);

        // Assert
        assertNotNull(result);
        assertEquals("iPhone 14", result.getProductTitle());
        assertEquals(1199.99, result.getPriceUnit());
        verify(productRepository, times(1)).save(any(Product.class));
    }

    @Test
    @DisplayName("update con ID - Cuando producto existe - Debe actualizar correctamente")
    void updateWithId_WhenProductExists_ShouldUpdateCorrectly() {
        // Arrange
        Integer productId = 1;
        when(productRepository.findById(productId)).thenReturn(Optional.of(testProduct));
        when(productRepository.save(any(Product.class))).thenReturn(testProduct);

        // Act
        ProductDto result = productService.update(productId, testProductDto);

        // Assert
        assertNotNull(result);
        assertEquals(testProduct.getProductId(), result.getProductId());
        verify(productRepository, times(1)).findById(productId);
        verify(productRepository, times(1)).save(any(Product.class));
    }

    @Test
    @DisplayName("deleteById - Cuando producto existe - Debe eliminar correctamente")
    void deleteById_WhenProductExists_ShouldDeleteCorrectly() {
        // Arrange
        Integer productId = 1;
        when(productRepository.findById(productId)).thenReturn(Optional.of(testProduct));
        doNothing().when(productRepository).delete(any(Product.class));

        // Act & Assert
        assertDoesNotThrow(() -> productService.deleteById(productId));
        verify(productRepository, times(1)).findById(productId);
        verify(productRepository, times(1)).delete(any(Product.class));
    }

    @Test
    @DisplayName("deleteById - Cuando producto no existe - Debe lanzar ProductNotFoundException")
    void deleteById_WhenProductNotExists_ShouldThrowProductNotFoundException() {
        // Arrange
        Integer productId = 999;
        when(productRepository.findById(productId)).thenReturn(Optional.empty());

        // Act & Assert
        ProductNotFoundException exception = assertThrows(
                ProductNotFoundException.class,
                () -> productService.deleteById(productId));

        assertTrue(exception.getMessage().contains("Product with id: 999 not found"));
        verify(productRepository, times(1)).findById(productId);
        verify(productRepository, never()).delete(any(Product.class));
    }

    @Test
    @DisplayName("save - Cuando cantidad es límite máximo - Debe manejar correctamente")
    void save_WhenQuantityIsMaxLimit_ShouldHandleCorrectly() {
        // Arrange
        testProductDto.setQuantity(Integer.MAX_VALUE);
        testProduct.setQuantity(Integer.MAX_VALUE);
        when(productRepository.save(any(Product.class))).thenReturn(testProduct);

        // Act
        ProductDto result = productService.save(testProductDto);

        // Assert
        assertNotNull(result);
        assertEquals(Integer.MAX_VALUE, result.getQuantity());
        verify(productRepository, times(1)).save(any(Product.class));
    }
}
