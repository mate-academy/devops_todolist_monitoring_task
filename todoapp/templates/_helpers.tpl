{{- define "todoapp.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{- define "todoapp.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "todoapp.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "todoapp.labels" -}}
app.kubernetes.io/name: {{ include "todoapp.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}
