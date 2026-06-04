"""Groq-based implementation of the brand extraction contract."""

import json
import urllib.error
import urllib.request

from app.application.schemas import BrandExtractionOutput
from app.domain.entities import BrandExtractionResult
from app.domain.interfaces import BrandExtractor
from app.infrastructure.prompts import build_extraction_messages
from app.infrastructure.settings import GroqSettings
from app.shared.exceptions import GroqConnectionError, InvalidLLMResponseError
from app.shared.logger import get_logger


class GroqBrandExtractor(BrandExtractor):
    """Extract brands by calling Groq's chat completions endpoint.

    This implementation is responsible for building the request payload, sending the HTTP
    request, and validating the returned JSON against the application output schema.

    Attributes:
        _settings (GroqSettings): Runtime settings used for request configuration.
        _logger (Logger): Logger used to record request lifecycle events and errors.
    """

    def __init__(self, settings: GroqSettings | None = None) -> None:
        self._settings = settings or GroqSettings.from_env()
        self._logger = get_logger(self.__class__.__name__)

    def extract(self, text: str, monitored_brand: str) -> BrandExtractionResult:
        """Extract brands for the provided text using the Groq API.

        Args:
            text (str): Source text that will be analyzed.
            monitored_brand (str): Brand that must be checked explicitly.

        Returns:
            BrandExtractionResult: Domain entity containing the extractor result.

        Raises:
            GroqConnectionError: If the HTTP request cannot be completed successfully.
            InvalidLLMResponseError: If the API response is empty, malformed, or invalid.
        """

        self._logger.info("Starting Groq brand extraction.")
        payload = self._build_payload(text=text, monitored_brand=monitored_brand)
        response_content = self._send_request(payload)
        output = self._parse_output(response_content)
        self._logger.info("Groq brand extraction finished.")
        return BrandExtractionResult(
            monitored_brand_found=output.monitored_brand_found,
            other_brands=tuple(output.other_brands),
        )

    def _build_payload(self, text: str, monitored_brand: str) -> dict[str, object]:
        """Build the request payload expected by the Groq API.

        Args:
            text (str): Source text that will be analyzed.
            monitored_brand (str): Brand that must be checked explicitly.

        Returns:
            dict[str, object]: Serialized payload ready for JSON encoding.
        """

        return {
            "model": self._settings.model,
            "temperature": self._settings.temperature,
            "messages": build_extraction_messages(
                text=text,
                monitored_brand=monitored_brand,
            ),
            "response_format": {
                "type": "json_object",
            },
        }

    def _send_request(self, payload: dict[str, object]) -> str:
        """Send the extraction request to Groq and return the message content.

        Args:
            payload (dict[str, object]): Serialized request payload.

        Returns:
            str: Raw textual content returned by the model.

        Raises:
            GroqConnectionError: If the request fails at the HTTP or network layer.
            InvalidLLMResponseError: If the response envelope cannot be interpreted.
        """

        request = urllib.request.Request(
            url=self._settings.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers=self._build_headers(),
            method="POST",
        )

        self._logger.info("Calling Groq API.")
        self._logger.debug(
            "Groq request prepared for model '%s'.", self._settings.model
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=self._settings.timeout_seconds,
            ) as response:
                response_body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            self._logger.error("Groq API returned HTTP %s.", exc.code)
            raise GroqConnectionError(
                f"Groq API request failed with status {exc.code}: {details}"
            ) from exc
        except urllib.error.URLError as exc:
            self._logger.error("Groq API connection failed.")
            raise GroqConnectionError("Could not connect to Groq API.") from exc

        return self._extract_message_content(response_body)

    def _build_headers(self) -> dict[str, str]:
        """Build HTTP headers for the Groq API request.

        Returns:
            dict[str, str]: Headers required by the chat completions endpoint.
        """

        return {
            "Authorization": f"Bearer {self._settings.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self._settings.user_agent,
        }

    def _extract_message_content(self, response_body: str) -> str:
        """Extract the assistant message content from a raw API response.

        Args:
            response_body (str): Raw JSON body returned by the Groq API.

        Returns:
            str: Model message content extracted from the response envelope.

        Raises:
            InvalidLLMResponseError: If the response envelope is malformed or empty.
        """

        try:
            response_data = json.loads(response_body)
            content = response_data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            self._logger.error("Groq API returned an unexpected response envelope.")
            raise InvalidLLMResponseError(
                "Groq API returned an unexpected response structure."
            ) from exc

        if not isinstance(content, str) or not content.strip():
            self._logger.error("Groq API returned an empty message content.")
            raise InvalidLLMResponseError(
                "Groq API returned an empty response content."
            )

        return content

    def _parse_output(self, response_content: str) -> BrandExtractionOutput:
        """Validate the model response against the application output schema.

        Args:
            response_content (str): Raw model content expected to represent JSON output.

        Returns:
            BrandExtractionOutput: Parsed and validated output model.

        Raises:
            InvalidLLMResponseError: If the model output is not valid JSON or schema-compliant.
        """

        try:
            return BrandExtractionOutput.model_validate_json(response_content)
        except ValueError:
            pass

        try:
            parsed_json = json.loads(response_content)
        except json.JSONDecodeError as exc:
            self._logger.error("Groq response is not valid JSON.")
            raise InvalidLLMResponseError("Groq response is not valid JSON.") from exc

        try:
            return BrandExtractionOutput.model_validate(parsed_json)
        except Exception as exc:
            self._logger.error("Groq response does not match the expected schema.")
            raise InvalidLLMResponseError(
                "Groq response does not match the expected schema."
            ) from exc
