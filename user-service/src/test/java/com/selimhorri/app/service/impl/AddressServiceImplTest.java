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

import com.selimhorri.app.domain.Address;
import com.selimhorri.app.domain.User;
import com.selimhorri.app.dto.AddressDto;
import com.selimhorri.app.dto.UserDto;
import com.selimhorri.app.exception.wrapper.AddressNotFoundException;
import com.selimhorri.app.repository.AddressRepository;

@ExtendWith(MockitoExtension.class)
@DisplayName("AddressServiceImpl - Unit Tests")
class AddressServiceImplTest {

    @Mock
    private AddressRepository addressRepository;

    @InjectMocks
    private AddressServiceImpl addressService;

    private Address testAddress;
    private AddressDto testAddressDto;
    private User testUser;

    @BeforeEach
    void setUp() {
        testUser = User.builder()
                .userId(1)
                .firstName("John")
                .lastName("Doe")
                .email("john.doe@test.com")
                .phone("+1234567890")
                .build();

        testAddress = Address.builder()
                .addressId(1)
                .fullAddress("123 Main Street")
                .postalCode("12345")
                .city("Test City")
                .user(testUser)
                .build();

        testAddressDto = AddressDto.builder()
                .addressId(1)
                .fullAddress("123 Main Street")
                .postalCode("12345")
                .city("Test City")
                .userDto(UserDto.builder()
                        .userId(1)
                        .firstName("John")
                        .lastName("Doe")
                        .email("john.doe@test.com")
                        .phone("+1234567890")
                        .build())
                .build();
    }

    @Test
    @DisplayName("findAll - Cuando existen direcciones - Debe retornar lista de AddressDto")
    void findAll_WhenAddressesExist_ShouldReturnAddressDtoList() {
        // Arrange
        List<Address> addresses = Arrays.asList(testAddress);
        when(addressRepository.findAll()).thenReturn(addresses);

        // Act
        List<AddressDto> result = addressService.findAll();

        // Assert
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals(testAddress.getAddressId(), result.get(0).getAddressId());
        assertEquals(testAddress.getFullAddress(), result.get(0).getFullAddress());
        assertEquals(testAddress.getCity(), result.get(0).getCity());
        verify(addressRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("findAll - Cuando no existen direcciones - Debe retornar lista vacía")
    void findAll_WhenNoAddressesExist_ShouldReturnEmptyList() {
        // Arrange
        when(addressRepository.findAll()).thenReturn(Arrays.asList());

        // Act
        List<AddressDto> result = addressService.findAll();

        // Assert
        assertNotNull(result);
        assertTrue(result.isEmpty());
        verify(addressRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("findById - Cuando dirección existe - Debe retornar AddressDto")
    void findById_WhenAddressExists_ShouldReturnAddressDto() {
        // Arrange
        Integer addressId = 1;
        when(addressRepository.findById(addressId)).thenReturn(Optional.of(testAddress));

        // Act
        AddressDto result = addressService.findById(addressId);

        // Assert
        assertNotNull(result);
        assertEquals(testAddress.getAddressId(), result.getAddressId());
        assertEquals(testAddress.getFullAddress(), result.getFullAddress());
        assertEquals(testAddress.getPostalCode(), result.getPostalCode());
        assertEquals(testAddress.getCity(), result.getCity());
        verify(addressRepository, times(1)).findById(addressId);
    }

    @Test
    @DisplayName("findById - Cuando dirección no existe - Debe lanzar AddressNotFoundException")
    void findById_WhenAddressNotExists_ShouldThrowAddressNotFoundException() {
        // Arrange
        Integer addressId = 999;
        when(addressRepository.findById(addressId)).thenReturn(Optional.empty());

        // Act & Assert
        AddressNotFoundException exception = assertThrows(
                AddressNotFoundException.class,
                () -> addressService.findById(addressId));

        assertTrue(exception.getMessage().contains("Address with id: 999 not found"));
        verify(addressRepository, times(1)).findById(addressId);
    }

    @Test
    @DisplayName("save - Cuando datos válidos - Debe guardar y retornar AddressDto")
    void save_WhenValidData_ShouldSaveAndReturnAddressDto() {
        // Arrange
        when(addressRepository.save(any(Address.class))).thenReturn(testAddress);

        // Act
        AddressDto result = addressService.save(testAddressDto);

        // Assert
        assertNotNull(result);
        assertEquals(testAddress.getAddressId(), result.getAddressId());
        assertEquals(testAddress.getFullAddress(), result.getFullAddress());
        assertEquals(testAddress.getCity(), result.getCity());
        verify(addressRepository, times(1)).save(any(Address.class));
    }

    @Test
    @DisplayName("update - Cuando datos válidos - Debe actualizar y retornar AddressDto")
    void update_WhenValidData_ShouldUpdateAndReturnAddressDto() {
        // Arrange
        testAddressDto.setFullAddress("456 Updated Street");
        testAddressDto.setCity("Updated City");

        Address updatedAddress = Address.builder()
                .addressId(1)
                .fullAddress("456 Updated Street")
                .postalCode("12345")
                .city("Updated City")
                .user(testUser)
                .build();

        when(addressRepository.save(any(Address.class))).thenReturn(updatedAddress);

        // Act
        AddressDto result = addressService.update(testAddressDto);

        // Assert
        assertNotNull(result);
        assertEquals("456 Updated Street", result.getFullAddress());
        assertEquals("Updated City", result.getCity());
        verify(addressRepository, times(1)).save(any(Address.class));
    }

    @Test
    @DisplayName("update con ID - Cuando dirección existe - Debe actualizar correctamente")
    void updateWithId_WhenAddressExists_ShouldUpdateCorrectly() {
        // Arrange
        Integer addressId = 1;
        when(addressRepository.findById(addressId)).thenReturn(Optional.of(testAddress));
        when(addressRepository.save(any(Address.class))).thenReturn(testAddress);

        // Act
        AddressDto result = addressService.update(addressId, testAddressDto);

        // Assert
        assertNotNull(result);
        assertEquals(testAddress.getAddressId(), result.getAddressId());
        verify(addressRepository, times(1)).findById(addressId);
        verify(addressRepository, times(1)).save(any(Address.class));
    }

    @Test
    @DisplayName("update con ID - Cuando dirección no existe - Debe lanzar AddressNotFoundException")
    void updateWithId_WhenAddressNotExists_ShouldThrowAddressNotFoundException() {
        // Arrange
        Integer addressId = 999;
        when(addressRepository.findById(addressId)).thenReturn(Optional.empty());

        // Act & Assert
        AddressNotFoundException exception = assertThrows(
                AddressNotFoundException.class,
                () -> addressService.update(addressId, testAddressDto));

        assertTrue(exception.getMessage().contains("Address with id: 999 not found"));
        verify(addressRepository, times(1)).findById(addressId);
        verify(addressRepository, never()).save(any(Address.class));
    }

    @Test
    @DisplayName("deleteById - Cuando dirección existe - Debe eliminar sin excepción")
    void deleteById_WhenAddressExists_ShouldDeleteWithoutException() {
        // Arrange
        Integer addressId = 1;
        doNothing().when(addressRepository).deleteById(addressId);

        // Act & Assert
        assertDoesNotThrow(() -> addressService.deleteById(addressId));
        verify(addressRepository, times(1)).deleteById(addressId);
    }

    @Test
    @DisplayName("save - Con dirección sin usuario - Debe guardar correctamente")
    void save_WithAddressWithoutUser_ShouldSaveCorrectly() {
        // Arrange
        AddressDto addressDtoWithoutUser = AddressDto.builder()
                .fullAddress("789 No User Street")
                .postalCode("67890")
                .city("No User City")
                .userDto(null)
                .build();

        Address addressWithoutUser = Address.builder()
                .addressId(2)
                .fullAddress("789 No User Street")
                .postalCode("67890")
                .city("No User City")
                .user(null)
                .build();

        when(addressRepository.save(any(Address.class))).thenReturn(addressWithoutUser);

        // Act
        AddressDto result = addressService.save(addressDtoWithoutUser);

        // Assert
        assertNotNull(result);
        assertEquals("789 No User Street", result.getFullAddress());
        assertNull(result.getUserDto());
        verify(addressRepository, times(1)).save(any(Address.class));
    }
}
