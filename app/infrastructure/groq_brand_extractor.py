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
    def __init__(self, settings: GroqSettings | None = None) -> None:
        self._settings = settings or GroqSettings.from_env()
        self._logger = get_logger(self.__class__.__name__)

    def extract(self, text: str, monitored_brand: str) -> BrandExtractionResult:
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
        request = urllib.request.Request(
            url=self._settings.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self._settings.api_key}",
                "Content-Type": "application/json",
            },
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

    def _extract_message_content(self, response_body: str) -> str:
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
