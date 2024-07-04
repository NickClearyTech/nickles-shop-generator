{{/*
Expand the name of the chart.
*/}}
{{- define "shopgen.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "shopgen.fullname" -}}
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
{{- define "shopgen.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common webserver labels
*/}}
{{- define "shopgen.common-labels" -}}
helm.sh/chart: {{ include "shopgen.chart" . }}
{{ include "shopgen.common-selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector webserver labels
*/}}
{{- define "shopgen.common-selectorLabels" -}}
app.kubernetes.io/name: {{ include "shopgen.name" . }}-webserver
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Workers labels
*/}}
{{- define "shopgen.worker-labels" -}}
helm.sh/chart: {{ include "shopgen.chart" . }}
{{ include "shopgen.worker-selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector workers labels
*/}}
{{- define "shopgen.worker-selectorLabels" -}}
app.kubernetes.io/name: {{ include "shopgen.name" . }}-worker
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "shopgen.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "shopgen.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
