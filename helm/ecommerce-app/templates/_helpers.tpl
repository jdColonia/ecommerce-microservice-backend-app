{{/*
Expand the name of the chart.
*/}}
{{- define "ecommerce-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "ecommerce-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "ecommerce-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "ecommerce-app.labels" -}}
helm.sh/chart: {{ include "ecommerce-app.chart" . }}
{{ include "ecommerce-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "ecommerce-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "ecommerce-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "ecommerce-app.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "ecommerce-app.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Common environment variables
*/}}
{{- define "ecommerce-app.commonEnv" -}}
- name: SPRING_PROFILES_ACTIVE
  value: {{ .Values.global.environment | quote }}
- name: SPRING_ZIPKIN_BASE_URL
  value: "http://{{ .Release.Name }}-zipkin:9411/"
- name: EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
  value: "http://{{ .Release.Name }}-service-discovery:8761/eureka/"
- name: SPRING_CONFIG_IMPORT
  value: "optional:configserver:http://{{ .Release.Name }}-cloud-config:9296/"
- name: JAVA_OPTS
  value: "-Xmx512m -Xms256m -XX:+UseG1GC -XX:+UseContainerSupport"
{{- end }}
