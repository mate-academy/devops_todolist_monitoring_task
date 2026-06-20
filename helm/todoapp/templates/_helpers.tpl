{{- define "todoapp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "todoapp.fullname" -}}
{{- default .Chart.Name .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "todoapp.labels" -}}
app: {{ include "todoapp.name" . }}
app.kubernetes.io/name: {{ include "todoapp.name" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}

{{- define "todoapp.selectorLabels" -}}
app: {{ include "todoapp.name" . }}
{{- end -}}
