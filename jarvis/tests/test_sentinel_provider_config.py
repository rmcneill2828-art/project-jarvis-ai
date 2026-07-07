import pytest

from sentinel import (
    CredentialReference,
    ProviderConfiguration,
    ProviderConfigurationRegistry,
    RetryPolicy,
)


def test_credential_reference_accepts_environment_variable() -> None:
    reference = CredentialReference(environment_variable="OPENAI_API_KEY")

    assert reference.environment_variable == "OPENAI_API_KEY"


def test_credential_reference_rejects_empty_environment_variable() -> None:
    with pytest.raises(ValueError, match="Credential environment variable must not be empty."):
        CredentialReference(environment_variable=" ")


def test_retry_policy_accepts_valid_values() -> None:
    policy = RetryPolicy(max_attempts=3, backoff_seconds=0.5)

    assert policy.max_attempts == 3
    assert policy.backoff_seconds == 0.5


def test_retry_policy_rejects_invalid_attempt_count() -> None:
    with pytest.raises(ValueError, match="Retry policy max attempts must be at least one."):
        RetryPolicy(max_attempts=0)


def test_retry_policy_rejects_negative_backoff() -> None:
    with pytest.raises(ValueError, match="Retry policy backoff seconds must not be negative."):
        RetryPolicy(backoff_seconds=-0.1)


def test_provider_configuration_accepts_valid_configuration() -> None:
    configuration = ProviderConfiguration(
        provider_name="openai",
        default_capability="text-generation",
        default_model="gpt-4.1-mini",
        endpoint="https://api.openai.com/v1",
        timeout_seconds=15.0,
        retry_policy=RetryPolicy(max_attempts=2, backoff_seconds=0.25),
        credential=CredentialReference(environment_variable="OPENAI_API_KEY"),
        metadata={"tier": "external"},
    )

    assert configuration.provider_name == "openai"
    assert configuration.enabled is True
    assert configuration.default_model == "gpt-4.1-mini"
    assert configuration.metadata["tier"] == "external"


def test_provider_configuration_rejects_empty_provider_name() -> None:
    with pytest.raises(ValueError, match="Provider configuration name must not be empty."):
        ProviderConfiguration(provider_name=" ")


def test_provider_configuration_rejects_empty_default_capability() -> None:
    with pytest.raises(
        ValueError,
        match="Provider configuration default capability must not be empty.",
    ):
        ProviderConfiguration(provider_name="openai", default_capability=" ")


def test_provider_configuration_rejects_invalid_timeout() -> None:
    with pytest.raises(
        ValueError,
        match="Provider configuration timeout seconds must be greater than zero.",
    ):
        ProviderConfiguration(provider_name="openai", timeout_seconds=0)


def test_provider_configuration_metadata_is_immutable() -> None:
    configuration = ProviderConfiguration(
        provider_name="openai",
        metadata={"tier": "external"},
    )

    with pytest.raises(TypeError):
        configuration.metadata["tier"] = "changed"


def test_provider_configuration_registry_registers_configuration() -> None:
    registry = ProviderConfigurationRegistry()
    configuration = ProviderConfiguration(provider_name="openai")

    registered = registry.register(configuration)

    assert registered is configuration
    assert registry.configurations() == (configuration,)


def test_provider_configuration_registry_replaces_configuration() -> None:
    registry = ProviderConfigurationRegistry()
    first = ProviderConfiguration(provider_name="openai", default_model="first")
    replacement = ProviderConfiguration(provider_name="openai", default_model="second")

    registry.register(first)
    registry.register(replacement)

    assert registry.get("openai") is replacement
    assert registry.configurations() == (replacement,)


def test_provider_configuration_registry_retrieves_configuration() -> None:
    registry = ProviderConfigurationRegistry()
    configuration = ProviderConfiguration(provider_name="local-echo")

    registry.register(configuration)

    assert registry.get("local-echo") is configuration


def test_provider_configuration_registry_rejects_empty_lookup_name() -> None:
    registry = ProviderConfigurationRegistry()

    with pytest.raises(ValueError, match="Provider configuration lookup name must not be empty."):
        registry.get(" ")


def test_provider_configuration_registry_rejects_unknown_provider() -> None:
    registry = ProviderConfigurationRegistry()

    with pytest.raises(LookupError, match="No provider configuration registered for: missing."):
        registry.get("missing")


def test_provider_configuration_registry_returns_enabled_configurations_only() -> None:
    registry = ProviderConfigurationRegistry()
    enabled = ProviderConfiguration(provider_name="openai", enabled=True)
    disabled = ProviderConfiguration(provider_name="experimental", enabled=False)

    registry.register(enabled)
    registry.register(disabled)

    assert registry.enabled() == (enabled,)
