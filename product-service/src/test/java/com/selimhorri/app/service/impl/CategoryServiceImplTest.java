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

import com.selimhorri.app.domain.Category;
import com.selimhorri.app.dto.CategoryDto;
import com.selimhorri.app.exception.wrapper.CategoryNotFoundException;
import com.selimhorri.app.repository.CategoryRepository;

@ExtendWith(MockitoExtension.class)
@DisplayName("CategoryServiceImpl - Unit Tests")
class CategoryServiceImplTest {

    @Mock
    private CategoryRepository categoryRepository;

    @InjectMocks
    private CategoryServiceImpl categoryService;

    private Category testCategory;
    private CategoryDto testCategoryDto;
    private Category parentCategory;
    private CategoryDto parentCategoryDto;

    @BeforeEach
    void setUp() {
        parentCategory = Category.builder()
                .categoryId(1)
                .categoryTitle("Electronics")
                .imageUrl("https://example.com/electronics.jpg")
                .build();

        testCategory = Category.builder()
                .categoryId(2)
                .categoryTitle("Smartphones")
                .imageUrl("https://example.com/smartphones.jpg")
                .parentCategory(parentCategory)
                .build();

        parentCategoryDto = CategoryDto.builder()
                .categoryId(1)
                .categoryTitle("Electronics")
                .imageUrl("https://example.com/electronics.jpg")
                .build();

        testCategoryDto = CategoryDto.builder()
                .categoryId(2)
                .categoryTitle("Smartphones")
                .imageUrl("https://example.com/smartphones.jpg")
                .parentCategoryDto(parentCategoryDto)
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando existen categorías - Debe retornar lista de CategoryDto")
    void findAll_WhenCategoriesExist_ShouldReturnCategoryDtoList() {
        // Arrange
        List<Category> categories = Arrays.asList(testCategory, parentCategory);
        when(categoryRepository.findAll()).thenReturn(categories);

        // Act
        List<CategoryDto> result = categoryService.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(2, result.size());
        verify(categoryRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("findAll - Cuando no existen categorías - Debe retornar lista vacía")
    void findAll_WhenNoCategoriesExist_ShouldReturnEmptyList() {
        // Arrange
        when(categoryRepository.findAll()).thenReturn(Arrays.asList());

        // Act
        List<CategoryDto> result = categoryService.findAll();

        // Assert
        assertNotNull(result);
        assertTrue(result.isEmpty());
        verify(categoryRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("findById - Cuando categoría existe - Debe retornar CategoryDto")
    void findById_WhenCategoryExists_ShouldReturnCategoryDto() {
        // Arrange
        Integer categoryId = 2;
        when(categoryRepository.findById(categoryId)).thenReturn(Optional.of(testCategory));

        // Act
        CategoryDto result = categoryService.findById(categoryId);

        // Assert
        assertNotNull(result);
        assertEquals(testCategory.getCategoryId(), result.getCategoryId());
        assertEquals(testCategory.getCategoryTitle(), result.getCategoryTitle());
        assertEquals(testCategory.getImageUrl(), result.getImageUrl());
        verify(categoryRepository, times(1)).findById(categoryId);
    }

    @Test
    @DisplayName("findById - Cuando categoría no existe - Debe lanzar CategoryNotFoundException")
    void findById_WhenCategoryNotExists_ShouldThrowCategoryNotFoundException() {
        // Arrange
        Integer categoryId = 999;
        when(categoryRepository.findById(categoryId)).thenReturn(Optional.empty());

        // Act & Assert
        CategoryNotFoundException exception = assertThrows(
                CategoryNotFoundException.class,
                () -> categoryService.findById(categoryId));

        assertTrue(exception.getMessage().contains("Category with id: 999 not found"));
        verify(categoryRepository, times(1)).findById(categoryId);
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar CategoryDto")
    void save_WhenValidData_ShouldSaveAndReturnCategoryDto() {
        // Arrange
        when(categoryRepository.save(any(Category.class))).thenReturn(testCategory);

        // Act
        CategoryDto result = categoryService.save(testCategoryDto);

        // Assert
        assertNotNull(result);
        assertEquals(testCategory.getCategoryId(), result.getCategoryId());
        assertEquals(testCategory.getCategoryTitle(), result.getCategoryTitle());
        verify(categoryRepository, times(1)).save(any(Category.class));
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar CategoryDto")
    void update_WhenValidData_ShouldUpdateAndReturnCategoryDto() {
        // Arrange
        testCategoryDto.setCategoryTitle("Updated Smartphones");

        Category updatedCategory = Category.builder()
                .categoryId(2)
                .categoryTitle("Updated Smartphones")
                .imageUrl("https://example.com/smartphones.jpg")
                .parentCategory(parentCategory)
                .build();

        when(categoryRepository.save(any(Category.class))).thenReturn(updatedCategory);

        // Act
        CategoryDto result = categoryService.update(testCategoryDto);

        // Assert
        assertNotNull(result);
        assertEquals("Updated Smartphones", result.getCategoryTitle());
        verify(categoryRepository, times(1)).save(any(Category.class));
    }

    @Test
    @DisplayName("update con ID - Cuando categoría existe - Debe actualizar correctamente")
    void updateWithId_WhenCategoryExists_ShouldUpdateCorrectly() {
        // Arrange
        Integer categoryId = 2;
        when(categoryRepository.findById(categoryId)).thenReturn(Optional.of(testCategory));
        when(categoryRepository.save(any(Category.class))).thenReturn(testCategory);

        // Act
        CategoryDto result = categoryService.update(categoryId, testCategoryDto);

        // Assert
        assertNotNull(result);
        assertEquals(testCategory.getCategoryId(), result.getCategoryId());
        verify(categoryRepository, times(1)).findById(categoryId);
        verify(categoryRepository, times(1)).save(any(Category.class));
    }

    @Test
    @DisplayName("deleteById - Cuando categoría existe - Debe eliminar sin excepción")
    void deleteById_WhenCategoryExists_ShouldDeleteWithoutException() {
        // Arrange
        Integer categoryId = 2;
        doNothing().when(categoryRepository).deleteById(categoryId);

        // Act & Assert
        assertDoesNotThrow(() -> categoryService.deleteById(categoryId));
        verify(categoryRepository, times(1)).deleteById(categoryId);
    }

    @Test
    @DisplayName("save - Cuando título es muy largo - Debe manejar correctamente")
    void save_WhenTitleIsTooLong_ShouldHandleCorrectly() {
        // Arrange
        String longTitle = "A".repeat(300);
        testCategoryDto.setCategoryTitle(longTitle);
        testCategory.setCategoryTitle(longTitle);

        when(categoryRepository.save(any(Category.class))).thenReturn(testCategory);

        // Act
        CategoryDto result = categoryService.save(testCategoryDto);

        // Assert
        assertNotNull(result);
        assertEquals(longTitle, result.getCategoryTitle());
        verify(categoryRepository, times(1)).save(any(Category.class));
    }

    @Test
    @DisplayName("findById - Cuando categoría tiene jerarquía compleja - Debe mapear correctamente")
    void findById_WhenCategoryHasComplexHierarchy_ShouldMapCorrectly() {
        // Arrange
        Integer categoryId = 2;
        when(categoryRepository.findById(categoryId)).thenReturn(Optional.of(testCategory));

        // Act
        CategoryDto result = categoryService.findById(categoryId);

        // Assert
        assertNotNull(result);
        assertNotNull(result.getParentCategoryDto());
        assertEquals(parentCategory.getCategoryId(), result.getParentCategoryDto().getCategoryId());
        assertEquals(parentCategory.getCategoryTitle(), result.getParentCategoryDto().getCategoryTitle());
        verify(categoryRepository, times(1)).findById(categoryId);
    }
}
