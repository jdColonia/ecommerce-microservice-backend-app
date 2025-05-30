# Documentación de Pruebas Unitarias - Microservicios E-commerce

## Resumen Ejecutivo

Esta documentación presenta un conjunto completo de **pruebas unitarias** para 6 microservicios del sistema de e-commerce, siguiendo las mejores prácticas de testing con JUnit 5 y Mockito.

### Servicios Cubiertos

- **favourite-service**: Gestión de productos favoritos
- **order-service**: Gestión de pedidos y órdenes
- **payment-service**: Procesamiento de estados de pago
- **product-service**: Catálogo de productos y categorías
- **shipping-service**: Gestión de elementos de orden
- **user-service**: Gestión de usuarios

## Estadísticas de Cobertura

| Servicio          | Pruebas Implementadas | Estado        | Archivos de Prueba                                                   |
| ----------------- | --------------------- | ------------- | -------------------------------------------------------------------- |
| favourite-service | 11 pruebas            | ✅ Verificado | FavouriteServiceImplTest.java                                        |
| order-service     | 12 pruebas            | ✅ Verificado | OrderServiceImplTest.java                                            |
| payment-service   | 11 pruebas            | ✅ Verificado | PaymentServiceImplTest.java                                          |
| product-service   | 24 pruebas            | ✅ Verificado | ProductServiceImplTest.java (12) + CategoryServiceImplTest.java (12) |
| shipping-service  | 11 pruebas            | ✅ Verificado | OrderItemServiceImplTest.java                                        |
| user-service      | 10 pruebas            | ✅ Verificado | UserServiceImplTest.java                                             |

**Total Verificado**: **79 pruebas unitarias** implementadas y funcionales  
**Estado del Proyecto**: **100% de servicios verificados** ✅

## Estructura y Convenciones

### Convención de Nomenclatura

Todas las pruebas siguen el patrón:

```
MethodName_WhenCondition_ExpectedBehavior
```

**Ejemplos Reales:**

- `findById_WhenUserExists_ShouldReturnUserDto` (user-service)
- `save_WhenValidData_ShouldSaveAndReturnProductDto` (product-service)
- `findById_WhenCategoryNotExists_ShouldThrowCategoryNotFoundException` (product-service)
- `findByUsername_WhenUserNotExists_ShouldThrowUserObjectNotFoundException` (user-service)

### Patrón AAA (Arrange-Act-Assert)

```java
@Test
@DisplayName("save - Cuando datos válidos - Debe guardar y retornar UserDto")
void save_WhenValidData_ShouldSaveAndReturnUserDto() {
    // Arrange - Configurar datos de prueba
    when(userRepository.save(any(User.class))).thenReturn(testUser);

    // Act - Ejecutar método bajo prueba
    UserDto result = userService.save(testUserDto);

    // Assert - Verificar resultados
    assertNotNull(result);
    assertEquals(testUser.getUserId(), result.getUserId());
    verify(userRepository, times(1)).save(any(User.class));
}
```

## Tipos de Pruebas Implementadas

### 1. **Pruebas de Caso Feliz (Happy Path)**

- Operaciones CRUD con datos válidos
- Flujos de negocio normales
- **Ejemplo**: `findById_WhenUserExists_ShouldReturnUserDto`

### 2. **Pruebas de Casos de Error**

- Manejo de excepciones personalizadas
- Datos no encontrados
- **Ejemplo**: `findById_WhenUserNotExists_ShouldThrowUserObjectNotFoundException`

### 3. **Pruebas de Casos Límite (Edge Cases)**

- Valores extremos y casos especiales
- Listas vacías
- **Ejemplos**:
  - `save_WhenFeeIsZero_ShouldSaveCorrectly`
  - `update_WhenQuantityUpdatedToZero_ShouldUpdateCorrectly`

### 4. **Pruebas de Integración con RestTemplate**

- Verificación de llamadas a servicios externos
- Manejo de DTOs relacionados
- **Ejemplo**: Favourite y OrderItem que consumen User/Product services

## Tecnologías y Frameworks Utilizados

### Framework de Testing

- **JUnit 5**: Framework principal de testing
- **Mockito**: Framework de mocking para dependencias
- **Spring Boot Test**: Soporte para testing de Spring Boot
- **@ExtendWith(MockitoExtension.class)**: Integración JUnit 5 + Mockito

### Herramientas de Cobertura

- **Maven Surefire**: Ejecución de pruebas unitarias
- **JaCoCo**: Análisis de cobertura de código

## Comandos de Ejecución

### Ejecutar Todas las Pruebas Unitarias

```bash
mvn clean test
```

### Ejecutar Pruebas por Servicio Específico

```bash
# Todos los servicios están verificados ✅
mvn test -pl order-service
mvn test -pl payment-service
mvn test -pl favourite-service
mvn test -pl shipping-service
mvn test -pl product-service
mvn test -pl user-service
```

### Ejecutar Prueba Específica

```bash
mvn test -Dtest=OrderServiceImplTest
mvn test -Dtest=PaymentServiceImplTest#save_WhenValidData_ShouldSaveAndReturnPaymentDto
```

### Generar Reporte de Cobertura

```bash
mvn clean test jacoco:report
```

## Detalles por Servicio

### ❤️ **favourite-service** (11 pruebas)

**Funcionalidades cubiertas:**

- Clave compuesta: `userId` + `productId` + `likeDate`
- Gestión de fechas de "like"
- Integración con User y Product services
- Mapeo complejo con UserDto y ProductDto

**Métodos probados:**

- `findAll()`, `findById()`, `save()`, `update()`, `deleteById()`

### 🎯 **order-service** (12 pruebas)

**Funcionalidades cubiertas:**

- CRUD completo de órdenes
- Métodos `update()` con y sin ID
- Casos edge: fee = 0, actualización parcial
- Integración con Cart/CartDto

**Métodos probados:**

- `findAll()`, `findById()`, `save()`, `update()`, `deleteById()`

### 💳 **payment-service** (11 pruebas)

**Funcionalidades cubiertas:**

- Estados de pago (`NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`)
- Campo `isPayed` boolean
- Relación con órdenes via `orderId`
- Integración con RestTemplate para OrderDto

**Métodos probados:**

- `findAll()`, `findById()`, `save()`, `update()`, `deleteById()`

### 📦 **product-service** (24 pruebas total)

#### ProductServiceImpl (12 pruebas)

**Funcionalidades cubiertas:**

- CRUD completo de productos
- Gestión de inventario (quantity)
- Precios y SKUs
- Relación con categorías
- Casos edge: precio = 0, cantidad máxima

#### CategoryServiceImpl (12 pruebas)

**Funcionalidades cubiertas:**

- Jerarquía de categorías (parent-child)
- Gestión de imágenes
- Casos edge: títulos largos, categorías raíz
- Mapeo de relaciones complejas

**Métodos probados:**

- `findAll()`, `findById()`, `save()`, `update()`, `deleteById()`

### 🛒 **shipping-service** (11 pruebas)

**Nota importante:** Este servicio maneja `OrderItem`, no envíos.

**Funcionalidades cubiertas:**

- Clave compuesta: `productId` + `orderId`
- Gestión de cantidades ordenadas
- Integración con Product y Order services
- Casos edge: cantidad = 0, cantidades grandes

**Métodos probados:**

- `findAll()`, `findById()`, `save()`, `update()`, `deleteById()`

### 👤 **user-service** (10 pruebas)

**Funcionalidades cubiertas:**

- Gestión completa de usuarios con credenciales
- Autenticación por username
- Roles y autoridades (`RoleBasedAuthority`)
- Campos de seguridad (enabled, expired, locked)
- Relación User-Credential

**Métodos probados:**

- `findAll()`, `findById()`, `save()`, `update()`, `deleteById()`, `findByUsername()`

## Patrones de Testing Identificados

### 1. **Manejo de Claves Compuestas**

```java
// FavouriteId y OrderItemId requieren múltiples campos
FavouriteId testId = new FavouriteId(1, 1, LocalDateTime.now());
OrderItemId testId = new OrderItemId(1, 1);
```

### 2. **Mock de RestTemplate**

```java
@Mock
private RestTemplate restTemplate;

// En las pruebas
when(restTemplate.getForObject(contains("user-service"), eq(UserDto.class)))
    .thenReturn(testUserDto);
```

### 3. **Verificación de Interacciones**

```java
// Verificar llamadas correctas
verify(repository, times(1)).save(any(Entity.class));
verify(restTemplate, never()).getForObject(anyString(), eq(SomeDto.class));
```

### 4. **Casos Edge Consistentes**

- Valores en cero (fee, quantity)
- Listas vacías
- Entidades no encontradas
- Actualización parcial de campos

## Funcionalidades Críticas Cubiertas

### 1. **Sistema de Favoritos** ✅

- Gestión de productos favoritos por usuario
- Timestamps de interacciones
- Integración con catálogo de productos

### 2. **Gestión de Órdenes** ✅

- Creación y modificación de pedidos
- Cálculo de fees y totales
- Integración con carritos de compra

### 3. **Procesamiento de Pagos** ✅

- Estados de transacciones
- Validación de pagos completados
- Trazabilidad por orden

### 4. **Catálogo de Productos** ✅

- CRUD completo de productos
- Gestión de inventario y precios
- Jerarquía de categorías
- Relaciones producto-categoría
- SKUs y gestión de stock

### 5. **Gestión de Elementos de Orden** ✅

- Cantidades de productos ordenados
- Relación producto-orden
- Validación de cantidades

### 6. **Autenticación y Usuarios** ✅

- Gestión completa de usuarios
- Sistema de credenciales y roles
- Autenticación por username
- Campos de seguridad y autorización
