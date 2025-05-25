# Multi-stage build
FROM maven:3.8.4-openjdk-11-slim AS build
WORKDIR /app

# Cache de dependencias
COPY pom.xml ./
COPY product-service/pom.xml ./product-service/
RUN mvn dependency:go-offline -B -f product-service/pom.xml

# Compilar aplicación
COPY product-service/src ./product-service/src
RUN mvn clean package -DskipTests -f product-service/pom.xml

# Imagen final
FROM openjdk:11-jre-slim

# Instalar curl para el healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Argumentos de build
ARG PROJECT_VERSION=0.1.0
ARG ENVIRONMENT=dev
ARG USER_ID=1001
ARG GROUP_ID=1001

# Variables de entorno
ENV SPRING_PROFILES_ACTIVE=${ENVIRONMENT}
ENV JAVA_OPTS="-Xmx512m -Xms256m -XX:+UseG1GC -XX:+UseContainerSupport"
ENV SERVER_PORT=8500

# Usuario no-root
RUN groupadd -g ${GROUP_ID} appuser && \
    useradd -r -u ${USER_ID} -g appuser appuser

# Directorio de aplicación
RUN mkdir -p /home/app && \
    chown -R appuser:appuser /home/app

WORKDIR /home/app
USER appuser

# Copiar JAR
COPY --from=build --chown=appuser:appuser /app/product-service/target/product-service-v${PROJECT_VERSION}.jar product-service.jar

# Exponer puertos
EXPOSE ${SERVER_PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:${SERVER_PORT}/actuator/health || exit 1

# Punto de entrada
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -Dspring.profiles.active=$SPRING_PROFILES_ACTIVE -Dserver.port=$SERVER_PORT -Dmanagement.server.port=$SERVER_PORT -jar product-service.jar"]