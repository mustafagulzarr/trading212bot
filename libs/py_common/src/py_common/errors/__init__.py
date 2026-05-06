class DomainError(Exception):
    """Base domain error."""


class ConfigurationError(DomainError):
    """Configuration validation or loading error."""


class ComplianceError(DomainError):
    """Compliance gate failure."""


class BrokerUnavailableError(DomainError):
    """Raised when broker is unavailable."""
