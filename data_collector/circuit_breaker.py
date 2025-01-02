import time

class CircuitBreaker:
    def __init__(self, failure_threshold, recovery_timeout):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # Stati possibili: CLOSED, OPEN, HALF_OPEN

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if self._timeout_expired():
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpenException("Circuit Breaker is OPEN. Call denied.")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
        self.failures = 0
        self.last_failure_time = None

    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.state == "HALF_OPEN" or self.failures >= self.failure_threshold:
            self.state = "OPEN"

    def _timeout_expired(self):
        if self.last_failure_time is None:
            return False
        return (time.time() - self.last_failure_time) > self.recovery_timeout
    
class CircuitBreakerOpenException(Exception):
    def __init__(self, message="Circuit Breaker is OPEN. Call denied."):
        super().__init__(message)
