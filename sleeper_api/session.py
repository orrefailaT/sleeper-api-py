from json import JSONDecodeError
from time import sleep

from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from sleeper_api.logger import APILogger


class APISession(Session):
    def __init__(
        self, raise_errors: bool, max_attempts: int = 3, throttle: float = 0, **kwargs
    ) -> None:
        self._call_count = 0
        self._error_flag = False
        self._last_call_successful = True
        self._raise_errors = raise_errors
        self._throttle = throttle
        self.logger = APILogger(**kwargs)
        super().__init__()

        status_forcelist = (429, 500, 503, 522)
        retry = Retry(
            total=max_attempts, status_forcelist=status_forcelist, raise_on_status=False
        )
        self.mount("https://", HTTPAdapter(max_retries=retry))

    def _handle_error(self, *args, **kwargs):
        self.last_call_successful = False
        self.error_flag = True
        if e := kwargs.get("exc_info"):
            self.logger.exception(*args, **kwargs)
            if self._raise_errors:
                raise e
        else:
            self.logger.error(*args, **kwargs)

    def _handle_response(self, response: Response, log_null: bool):
        url = response.request.url or ""
        status_code = response.status_code
        if status_code != 200:
            self._handle_error(url, status_code)
            return None

        try:
            data = response.json()
        except JSONDecodeError as e:
            self._handle_error(url, status_code, exc_info=e)
            return None

        self.last_call_successful = True

        if not data and log_null:
            self.logger.warning(url, status_code, "Unexpected Empty/Null Response")
        else:
            self.logger.info(url, status_code)
        return data

    def call(self, url: str, log_null: bool):
        if self._throttle:
            sleep(self._throttle)
        response = self.get(url)
        self._call_count += 1 + len(response.raw.retries.history)
        return self._handle_response(response, log_null)
