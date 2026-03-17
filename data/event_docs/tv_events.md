# Smart TV Telemetry Events

## PlayerSessionStarted
Fired when a user begins a playback session.
Fields: user_id, device_id, content_id, timestamp, platform, app_version
Common issues: Missing device_id indicates device registration failure.

## BufferingEvent
Fired when playback is interrupted due to buffering.
Fields: user_id, device_id, content_id, buffer_duration_ms, bitrate, timestamp
Common issues: High buffer_duration_ms (>3000ms) indicates network degradation.

## CrashReport
Fired when the smart TV app crashes unexpectedly.
Fields: device_id, app_version, error_code, stack_trace, timestamp
Common issues: Repeated crashes on same app_version indicate a bad release.

## ContentNotFound
Fired when requested content cannot be located.
Fields: user_id, content_id, error_code, timestamp
Common issues: Spike in ContentNotFound events may indicate CDN issues.

## DeviceHeartbeat
Fired every 60 seconds to confirm device is online.
Fields: device_id, firmware_version, memory_usage_mb, cpu_usage_pct, timestamp
Common issues: Missing heartbeats for >5 minutes indicate device offline.