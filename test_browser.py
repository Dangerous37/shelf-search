from server import make_server
import os
import threading
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright


class BrowserAcceptance(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.server = make_server(self.temp.name)
        self.addCleanup(self.server.server_close)
        thread = threading.Thread(target=self.server.serve_forever)
        thread.start()
        self.addCleanup(thread.join)
        self.addCleanup(self.server.shutdown)
        driver = sync_playwright().start()
        self.addCleanup(driver.stop)
        browser = driver.chromium.launch(channel=os.getenv("TEST_BROWSER_CHANNEL") or None)
        self.addCleanup(browser.close)
        self.page = browser.new_page()
        self.url = "http://127.0.0.1:" + str(self.server.server_port)
        self.page.goto(self.url)

    def test_ranking_facets_and_keyboard(self):
        page = self.page
        page.get_by_role("searchbox").fill("auditoria")
        links = page.get_by_role("link")
        self.assertEqual(links.count(), 2)
        self.assertEqual(links.first.inner_text(), "Auditoría de importaciones")
        page.keyboard.press("Tab")
        page.keyboard.press("Tab")
        page.keyboard.press("Enter")
        page.wait_for_url("**/#audit" if "?" not in page.url else "**#audit")
        page.get_by_text("Reconcile source records and review import exceptions.", exact=True).wait_for()
        page.get_by_role("combobox").select_option("Reservas")
        self.assertEqual(links.count(), 0)
        page.reload()
        self.assertEqual(page.get_by_role("combobox").input_value(), "Reservas")
        self.assertEqual(page.get_by_role("status").inner_text(), "0 resultados")
