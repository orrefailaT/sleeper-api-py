import logging
from datetime import datetime
from inspect import stack
from pathlib import Path
from typing import Union


class APILogger(logging.Logger):
    def __init__(
        self,
        name: str = "sleeper_api",
        level: Union[int, str] = logging.NOTSET,
        filename: Union[str, Path, None] = None,
        **kwargs,
    ) -> None:
        if filename:
            api_handler = logging.FileHandler(filename=filename)
            self.addHandler(api_handler)
        super().__init__(name, level, **kwargs)

    def _log_message(self, **kwargs) -> str:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        extra = kwargs.pop("extra", "")
        message_parts = [
            timestamp,
            *[f'{k.replace("_", " ").title()}: {v}' for k, v in kwargs.items()],
        ]
        if extra:
            message_parts.append(extra)
        return " | ".join(message_parts)

    def info(self, url: str, status_code: int, extra: str = "") -> None:
        message = self._log_message(url=url, status_code=status_code, extra=extra)
        return super().info(message)

    def warning(self, url: str, status_code: int, extra: str = "") -> None:
        message = self._log_message(url=url, status_code=status_code, extra=extra)
        return super().warning(message)

    def error(
        self, url: str, status_code: int, extra: str = "", exc_info: bool = False
    ) -> None:
        message = self._log_message(url=url, status_code=status_code, extra=extra)
        return super().error(message, exc_info=exc_info)

    def missing(self, args: list, extra: str = "") -> None:
        function_name = stack()[1].function
        message = self._log_message(function=function_name, args=args, extra=extra)
        super().warning(message)
