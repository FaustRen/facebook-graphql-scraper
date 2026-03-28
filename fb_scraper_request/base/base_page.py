# -*- coding:utf-8 -*-
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service


class BasePage:
    def __init__(self, driver_path: str, open_browser: bool = False):
        chrome_options = self._build_options(open_browser)
        normalized_driver_path = self._normalize_path(driver_path)

        if self._looks_like_chrome_binary(normalized_driver_path):
            chrome_options.binary_location = normalized_driver_path
            service = Service()
        elif normalized_driver_path:
            service = Service(normalized_driver_path)
        else:
            service = Service()

        self.driver = self._build_driver(service=service, chrome_options=chrome_options)
        self.driver.maximize_window()

    @staticmethod
    def _build_options(open_browser: bool) -> ChromeOptions:
        options = ChromeOptions()
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-blink-features=AutomationControlled")
        if not open_browser:
            options.add_argument("--headless=new")
        options.add_argument("--blink-settings=imagesEnabled=false")
        return options

    @staticmethod
    def _normalize_path(path: str | None) -> str | None:
        if not path:
            return None
        # In notebook strings users often escape spaces (e.g. "Google\ Chrome").
        return path.replace("\\ ", " ").strip()

    @staticmethod
    def _looks_like_chrome_binary(path: str | None) -> bool:
        if not path:
            return False
        normalized = path.lower()
        return normalized.endswith("/google chrome") or normalized.endswith("/chrome")

    @staticmethod
    def _build_driver(service: Service, chrome_options: ChromeOptions):
        from seleniumwire import webdriver

        try:
            return webdriver.Chrome(service=service, options=chrome_options)
        except AttributeError as exc:
            if "VERSION_CHOICES" not in str(exc):
                raise
            # Some selenium-wire/pyOpenSSL combinations expose this at runtime.
            BasePage._patch_seleniumwire_tls_version_choices()
            return webdriver.Chrome(service=service, options=chrome_options)

    @staticmethod
    def _patch_seleniumwire_tls_version_choices() -> None:
        from OpenSSL import SSL
        from seleniumwire.thirdparty.mitmproxy.net import tls

        if hasattr(tls, "VERSION_CHOICES"):
            return

        basic_options = SSL.OP_CIPHER_SERVER_PREFERENCE
        if hasattr(SSL, "OP_NO_COMPRESSION"):
            basic_options |= SSL.OP_NO_COMPRESSION

        default_method = getattr(SSL, "SSLv23_METHOD", getattr(SSL, "TLS_METHOD", None))
        default_options = basic_options
        if hasattr(SSL, "OP_NO_SSLv2"):
            default_options |= SSL.OP_NO_SSLv2
        if hasattr(SSL, "OP_NO_SSLv3"):
            default_options |= SSL.OP_NO_SSLv3

        version_choices = {
            "all": (default_method, basic_options),
            "secure": (default_method, default_options),
        }

        for name in ("TLSv1", "TLSv1_1", "TLSv1_2"):
            method_name = f"{name}_METHOD"
            method = getattr(SSL, method_name, None)
            if method is not None:
                version_choices[name] = (method, basic_options)

        tls.VERSION_CHOICES = version_choices
