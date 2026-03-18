# Kafka Topic Schemas for Smart TV Telemetry

## Topic: tv.events.playback
Captures all playback-related events from smart TV devices.
Partition key: device_id
Retention: 7 days
Schema:
- event_type: string (PlayerSessionStarted, PlayerSessionEnded, BufferingEvent)
- user_id: string
- device_id: string
- content_id: string
- timestamp: ISO8601
- app_version: string
- platform: string (rokutv, androidtv, firetv)

## Topic: tv.events.errors
Captures crash reports and application errors.
Partition key: device_id
Retention: 30 days
Schema:
- event_type: string (CrashReport, ContentNotFound, AuthFailure)
- device_id: string
- app_version: string
- error_code: string
- stack_trace: string (optional)
- timestamp: ISO8601

## Topic: tv.devices.heartbeat
Captures periodic device health signals.
Partition key: device_id
Retention: 3 days
Schema:
- device_id: string
- firmware_version: string
- memory_usage_mb: integer
- cpu_usage_pct: float
- network_type: string (wifi, ethernet)
- timestamp: ISO8601

## Topic: tv.events.recommendations
Captures recommendation engine events.
Partition key: user_id
Retention: 14 days
Schema:
- user_id: string
- recommended_content_ids: list[string]
- algorithm_version: string
- response_time_ms: integer
- timestamp: ISO8601