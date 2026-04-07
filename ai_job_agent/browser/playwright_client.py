from playwright.sync_api import sync_playwright
from utils.logger import logger


class BrowserClient:

    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()

    def open(self, url):
        logger.info(f"Opening URL: {url}")
        self.page.goto(url, timeout=60000)

        # WAIT FOR PAGE LOAD (IMPORTANT)
        self.page.wait_for_load_state("domcontentloaded")
        logger.info("Page loaded")

        # try clicking apply buttons (Greenhouse/Lever)
        try:
            if self.page.query_selector("text=Apply"):
                self.page.click("text=Apply")
                self.page.wait_for_timeout(2000)
                logger.info("[ACTION] Clicked Apply button")
        except:
            pass

    def get_form_fields(self):
        logger.info("Extracting form fields...")

        try:
            self.page.wait_for_timeout(3000)  # allow dynamic load

            inputs = self.page.query_selector_all("input, textarea, select")

            fields = []
            for inp in inputs:
                name = inp.get_attribute("name") or inp.get_attribute("id")
                input_type = inp.get_attribute("type")

                if name:
                    fields.append({
                        "name": name,
                        "type": input_type
                    })

            logger.info(f"Total fields found: {len(fields)}")
            return fields

        except Exception as e:
            logger.error(f"Field extraction failed: {e}")
            return []

    def fill_field(self, field, value):
        name = field["name"]
        field_type = field["type"]

        try:
            if field_type in ["text", "email", "tel"]:
                selector = f'input[name="{name}"]'
                self.page.fill(selector, value)
                logger.info(f"Filled {name}")

            elif field_type == "radio":
                selector = f'input[name="{name}"]'
                self.page.check(selector)

            elif field_type == "checkbox":
                selector = f'input[name="{name}"]'
                self.page.check(selector)

        except Exception:
            logger.warning(f"Could not fill {name}")

    def submit(self):
        try:
            if self.page.query_selector('button[type="submit"]'):
                self.page.click('button[type="submit"]')
            elif self.page.query_selector('input[type="submit"]'):
                self.page.click('input[type="submit"]')

            logger.info("Form submitted")

        except Exception:
            logger.warning("Submit button not found")

    def close(self):
        self.browser.close()
        self.playwright.stop()