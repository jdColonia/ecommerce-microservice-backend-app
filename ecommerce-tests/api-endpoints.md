# API Endpoints - Microservicios E-Commerce

Este documento detalla todos los endpoints disponibles en la aplicación de microservicios de e-commerce. Todos los endpoints están expuestos a través del API Gateway y el Proxy Client.

## Servicio de Usuarios

Base URL: `/api/users`

| Método HTTP | Endpoint                         | Descripción                                 |
| ----------- | -------------------------------- | ------------------------------------------- |
| GET         | `/api/users`                     | Obtiene todos los usuarios                  |
| GET         | `/api/users/{userId}`            | Obtiene un usuario por su ID                |
| GET         | `/api/users/username/{username}` | Obtiene un usuario por su nombre de usuario |
| POST        | `/api/users`                     | Crea un nuevo usuario                       |
| PUT         | `/api/users`                     | Actualiza un usuario existente              |
| PUT         | `/api/users/{userId}`            | Actualiza un usuario específico por ID      |
| DELETE      | `/api/users/{userId}`            | Elimina un usuario por ID                   |

## Servicio de Credenciales

Base URL: `/api/credentials`

| Método HTTP | Endpoint                          | Descripción                       |
| ----------- | --------------------------------- | --------------------------------- |
| GET         | `/api/credentials`                | Obtiene todas las credenciales    |
| GET         | `/api/credentials/{credentialId}` | Obtiene credenciales por ID       |
| POST        | `/api/credentials`                | Crea nuevas credenciales          |
| PUT         | `/api/credentials`                | Actualiza credenciales existentes |
| DELETE      | `/api/credentials/{credentialId}` | Elimina credenciales por ID       |

## Servicio de Direcciones

Base URL: `/api/addresses`

| Método HTTP | Endpoint                     | Descripción                       |
| ----------- | ---------------------------- | --------------------------------- |
| GET         | `/api/addresses`             | Obtiene todas las direcciones     |
| GET         | `/api/addresses/{addressId}` | Obtiene una dirección por ID      |
| POST        | `/api/addresses`             | Crea una nueva dirección          |
| PUT         | `/api/addresses`             | Actualiza una dirección existente |
| DELETE      | `/api/addresses/{addressId}` | Elimina una dirección por ID      |

## Servicio de Productos

Base URL: `/api/products`

| Método HTTP | Endpoint                    | Descripción                             |
| ----------- | --------------------------- | --------------------------------------- |
| GET         | `/api/products`             | Obtiene todos los productos             |
| GET         | `/api/products/{productId}` | Obtiene un producto por ID              |
| POST        | `/api/products`             | Crea un nuevo producto                  |
| PUT         | `/api/products`             | Actualiza un producto existente         |
| PUT         | `/api/products/{productId}` | Actualiza un producto específico por ID |
| DELETE      | `/api/products/{productId}` | Elimina un producto por ID              |

## Servicio de Categorías

Base URL: `/api/categories`

| Método HTTP | Endpoint                       | Descripción                       |
| ----------- | ------------------------------ | --------------------------------- |
| GET         | `/api/categories`              | Obtiene todas las categorías      |
| GET         | `/api/categories/{categoryId}` | Obtiene una categoría por ID      |
| POST        | `/api/categories`              | Crea una nueva categoría          |
| PUT         | `/api/categories`              | Actualiza una categoría existente |
| DELETE      | `/api/categories/{categoryId}` | Elimina una categoría por ID      |

## Servicio de Órdenes

Base URL: `/api/orders`

| Método HTTP | Endpoint                | Descripción                           |
| ----------- | ----------------------- | ------------------------------------- |
| GET         | `/api/orders`           | Obtiene todas las órdenes             |
| GET         | `/api/orders/{orderId}` | Obtiene una orden por ID              |
| POST        | `/api/orders`           | Crea una nueva orden                  |
| PUT         | `/api/orders`           | Actualiza una orden existente         |
| PUT         | `/api/orders/{orderId}` | Actualiza una orden específica por ID |
| DELETE      | `/api/orders/{orderId}` | Elimina una orden por ID              |

## Servicio de Ítems de Orden

Base URL: `/api/order-items`

| Método HTTP | Endpoint                         | Descripción                          |
| ----------- | -------------------------------- | ------------------------------------ |
| GET         | `/api/order-items`               | Obtiene todos los ítems de órdenes   |
| GET         | `/api/order-items/{orderItemId}` | Obtiene un ítem de orden por ID      |
| POST        | `/api/order-items`               | Crea un nuevo ítem de orden          |
| PUT         | `/api/order-items`               | Actualiza un ítem de orden existente |
| DELETE      | `/api/order-items/{orderItemId}` | Elimina un ítem de orden por ID      |

## Servicio de Carritos

Base URL: `/api/carts`

| Método HTTP | Endpoint              | Descripción                    |
| ----------- | --------------------- | ------------------------------ |
| GET         | `/api/carts`          | Obtiene todos los carritos     |
| GET         | `/api/carts/{cartId}` | Obtiene un carrito por ID      |
| POST        | `/api/carts`          | Crea un nuevo carrito          |
| PUT         | `/api/carts`          | Actualiza un carrito existente |
| DELETE      | `/api/carts/{cartId}` | Elimina un carrito por ID      |

## Servicio de Pagos

Base URL: `/api/payments`

| Método HTTP | Endpoint                    | Descripción                 |
| ----------- | --------------------------- | --------------------------- |
| GET         | `/api/payments`             | Obtiene todos los pagos     |
| GET         | `/api/payments/{paymentId}` | Obtiene un pago por ID      |
| POST        | `/api/payments`             | Crea un nuevo pago          |
| PUT         | `/api/payments`             | Actualiza un pago existente |
| DELETE      | `/api/payments/{paymentId}` | Elimina un pago por ID      |

## Servicio de Envíos

Base URL: `/api/shippings`

| Método HTTP | Endpoint                      | Descripción                  |
| ----------- | ----------------------------- | ---------------------------- |
| GET         | `/api/shippings`              | Obtiene todos los envíos     |
| GET         | `/api/shippings/{shippingId}` | Obtiene un envío por ID      |
| POST        | `/api/shippings`              | Crea un nuevo envío          |
| PUT         | `/api/shippings`              | Actualiza un envío existente |
| DELETE      | `/api/shippings/{shippingId}` | Elimina un envío por ID      |

## Servicio de Favoritos

Base URL: `/api/favourites`

| Método HTTP | Endpoint                                          | Descripción                                                   |
| ----------- | ------------------------------------------------- | ------------------------------------------------------------- |
| GET         | `/api/favourites`                                 | Obtiene todos los favoritos                                   |
| GET         | `/api/favourites/{userId}/{productId}/{likeDate}` | Obtiene un favorito por ID compuesto                          |
| GET         | `/api/favourites/find`                            | Obtiene un favorito usando un objeto FavouriteId en el cuerpo |
| POST        | `/api/favourites`                                 | Crea un nuevo favorito                                        |
| PUT         | `/api/favourites`                                 | Actualiza un favorito existente                               |
| DELETE      | `/api/favourites/{userId}/{productId}/{likeDate}` | Elimina un favorito por ID compuesto                          |
| DELETE      | `/api/favourites/delete`                          | Elimina un favorito usando un objeto FavouriteId en el cuerpo |

## Servicio de Autenticación

Base URL: `/api/authenticate`

| Método HTTP | Endpoint                      | Descripción                                  |
| ----------- | ----------------------------- | -------------------------------------------- |
| POST        | `/api/authenticate`           | Autentica un usuario y devuelve un token JWT |
| GET         | `/api/authenticate/jwt/{jwt}` | Valida un token JWT                          |

## Servicio de Tokens de Verificación

Base URL: `/api/verification-tokens`

| Método HTTP | Endpoint                             | Descripción                                  |
| ----------- | ------------------------------------ | -------------------------------------------- |
| GET         | `/api/verification-tokens`           | Obtiene todos los tokens de verificación     |
| GET         | `/api/verification-tokens/{tokenId}` | Obtiene un token de verificación por ID      |
| POST        | `/api/verification-tokens`           | Crea un nuevo token de verificación          |
| PUT         | `/api/verification-tokens`           | Actualiza un token de verificación existente |
| DELETE      | `/api/verification-tokens/{tokenId}` | Elimina un token de verificación por ID      |

## Notas Adicionales

- Todos los endpoints están protegidos mediante autenticación JWT, excepto el endpoint de autenticación.
- Todos los servicios implementan un conjunto estándar de operaciones CRUD.
- Los formatos de datos para solicitudes y respuestas son JSON.
- Los errores se devuelven con códigos de estado HTTP estándar y mensajes descriptivos.

## Servicios de Infraestructura

La aplicación también cuenta con los siguientes servicios de infraestructura:

- **Service Discovery (Eureka)**: Registro y descubrimiento de servicios
- **Cloud Config**: Configuración centralizada
- **API Gateway**: Puerta de entrada y enrutamiento de solicitudes
- **Zipkin**: Trazabilidad distribuida

---

Documentación generada el 30 de mayo de 2025.
