# Multi-stage build para optimización
FROM maven:3.8.4-openjdk-11-slim AS build
WORKDIR /app

# Copiar solo los archivos de dependencias primero (para cache de Docker)
COPY pom.xml ./
COPY api-gateway/pom.xml ./api-gateway/
RUN mvn dependency:go-offline -B -f api-gateway/pom.xml

# Copiar código fuente y compilar
COPY api-gateway/src ./api-gateway/src
RUN mvn clean package -DskipTests -f api-gateway/pom.xml

# Imagen final optimizada
FROM openjdk:11-jre-slim

# Instalar curl para el healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Argumentos de build
ARG PROJECT_VERSION=0.1.0
ARG ENVIRONMENT=dev
ARG USER_ID=1001
ARG GROUP_ID=1001

# Variables de entorno configurables
ENV SPRING_PROFILES_ACTIVE=${ENVIRONMENT}
ENV JAVA_OPTS="-Xmx512m -Xms256m -XX:+UseG1GC -XX:+UseContainerSupport"
ENV SERVER_PORT=8222

# Crear usuario no-root para seguridad
RUN groupadd -g ${GROUP_ID} appuser && \
    useradd -r -u ${USER_ID} -g appuser appuser

# Crear directorio de aplicación
RUN mkdir -p /home/app && \
    chown -R appuser:appuser /home/app

WORKDIR /home/app
USER appuser

# Copiar JAR desde stage de build
COPY --from=build --chown=appuser:appuser /app/api-gateway/target/api-gateway-v${PROJECT_VERSION}.jar api-gateway.jar

# Exponer puertos
EXPOSE ${SERVER_PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:${SERVER_PORT}/actuator/health || exit 1

# Punto de entrada optimizado
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -Dspring.profiles.active=$SPRING_PROFILES_ACTIVE -Dserver.port=$SERVER_PORT -Dmanagement.server.port=$SERVER_PORT -jar api-gateway.jar"]