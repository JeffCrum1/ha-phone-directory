"""HTTP support for Comlink outputs."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from .output_factory import create_output
from .output_models import OutputConfig


@dataclass(frozen=True)
class HTTPResource:
    """Describe an HTTP resource provided by a Comlink output."""

    path: str
    content_type: str
    render: Callable


def get_http_resource(output: Any) -> HTTPResource | None:
    """Return the HTTP resource provided by an output, if any."""

    http_path = getattr(output, "http_path", None)

    if http_path is None:
        return None

    http_content_type = getattr(
        output,
        "http_content_type",
        None,
    )

    render = getattr(
        output,
        "render",
        None,
    )

    if http_content_type is None or render is None:
        raise ValueError(
            f"HTTP output {output} does not provide a complete HTTP resource",
        )

    return HTTPResource(
        path=http_path,
        content_type=http_content_type,
        render=render,
    )


class ComlinkHTTPView(HomeAssistantView):
    """Expose a Comlink output through Home Assistant HTTP."""

    requires_auth = False

    def __init__(
        self,
        hass: HomeAssistant,
        output: Any,
        path: str,
        content_type: str,
    ) -> None:
        """Initialize the HTTP view."""

        self.hass = hass
        self.output = output
        self.url = path
        self.name = f"phone_directory:{path}"
        self.content_type = content_type

    async def get(
        self,
        request: web.Request,
    ) -> web.Response:
        """Return the current phone directory."""

        authenticate = getattr(
            self.output,
            "authenticate",
            None,
        )

        if authenticate is not None:
            authenticated = await self.hass.async_add_executor_job(
                authenticate,
                request,
            )

            if not authenticated:
                return web.Response(
                    status=401,
                    headers={
                        "WWW-Authenticate": 'Basic realm="Phone Directory"',
                    },
                )

        contacts = await self.hass.async_add_executor_job(
            self._load_contacts,
        )

        body = await self.hass.async_add_executor_job(
            self.output.render,
            contacts,
        )

        return web.Response(
            text=body,
            content_type=self.content_type,
        )

    @staticmethod
    def _load_contacts():
        """Load the current phone directory contacts."""

        from ..storage import load_contacts

        return load_contacts()


class HTTPManager:
    """Manage Comlink HTTP output registrations."""

    def __init__(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Initialize the HTTP manager."""

        self.hass = hass

    async def async_register_output(
        self,
        output_config: OutputConfig,
    ) -> None:
        """Register an output's HTTP endpoint, if it provides one."""

        output = await self.hass.async_add_executor_job(
            create_output,
            output_config,
        )

        resource = get_http_resource(output)

        if resource is None:
            return

        view = ComlinkHTTPView(
            self.hass,
            output,
            resource.path,
            resource.content_type,
        )

        self.hass.http.register_view(view)
