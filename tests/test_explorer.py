"""Tests for the DTree Explorer package: the bridge agrees with the library, the local
server answers, and the two page variants are built as intended."""

import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from dtree import DTree  # noqa: E402

import build  # noqa: E402
from dtree_explorer import __main__ as app  # noqa: E402
from dtree_explorer import bridge  # noqa: E402


class TestBridge(unittest.TestCase):
    def test_examples_match_the_library(self):
        for name, text in build.examples().items():
            d = json.loads(bridge.encode(text))
            self.assertEqual(d["errors"], [], name)
            t = DTree()
            for line in text.splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    t.add_line(line)
            self.assertEqual(d["final"]["q1"], t.q1, name)
            self.assertEqual(d["final"]["q2"], t.q2, name)
            self.assertEqual(d["steps"][-1]["q1"], t.q1, name)

    def test_paper_examples(self):
        ex = build.examples()
        fig1 = json.loads(bridge.encode(ex["Paper, Figure 1"]))["final"]
        self.assertEqual(fig1["q1"], [str(i) for i in range(1, 13)])
        self.assertEqual(fig1["q2"], ["1", "2", "9", "12", "10", "11", "4", "5", "7", "8", "6", "3"])
        a = json.loads(bridge.encode(ex["Paper, Sec. 4.1, Case A: v before 6"]))["final"]
        self.assertEqual(a["q1"][4:7], ["5", "v", "6"])                  # v directly before 6 in Q1
        self.assertEqual(a["q2"][-3:], ["6", "v", "3"])                  # after 6's subtree in Q2
        for v in "ABC":
            files = [k for k in ex if f"Variant {v}:" in k][0]
            ops = [k for k in ex if f"Variant {v} with" in k][0]
            f1, f2 = json.loads(bridge.encode(ex[files]))["final"], json.loads(bridge.encode(ex[ops]))["final"]
            self.assertEqual((f1["q1"], f1["q2"]), (f2["q1"], f2["q2"]), v)

    def test_errors_and_limit(self):
        d = json.loads(bridge.encode("A: B\nX: Y\nA > Z\nnonsense\nB > C"))
        self.assertEqual([s["op"] for s in d["steps"]], ["A:B", "B>C"])
        self.assertEqual(len(d["errors"]), 3)
        big = "\n".join(["n0: n1"] + [f"n{i // 2}: n{i}" for i in range(2, 400)])
        d = json.loads(bridge.encode(big))
        self.assertFalse(d["stepwise"])
        self.assertNotIn("q1", d["steps"][0])
        self.assertEqual(len(d["final"]["q1"]), 400)


class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = app.serve(0)
        cls.url = f"http://127.0.0.1:{cls.httpd.server_address[1]}/"
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def test_page_info_encode(self):
        html = urllib.request.urlopen(self.url).read().decode()
        self.assertIn("<title>DTree Explorer</title>", html)
        info = json.loads(urllib.request.urlopen(self.url + "api/info").read())
        self.assertIn("dtree", info)
        req = urllib.request.Request(self.url + "api/encode", data="A: B; C\nB: D".encode(), method="POST")
        d = json.loads(urllib.request.urlopen(req).read())
        self.assertEqual(d["final"]["q1"], ["A", "B", "D", "C"])

    def test_foreign_host_refused(self):
        req = urllib.request.Request(self.url + "api/info", headers={"Host": "evil.example"})
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen(req)
        self.assertEqual(cm.exception.code, 403)


class TestPages(unittest.TestCase):
    def test_variants(self):
        plain, site = build.page(), build.page(build.SITE["counter"], build.SITE["privacy"])
        for html in (plain, site):
            self.assertNotRegex(html, r"__[A-Z_]+__")
            self.assertNotIn("googletagmanager", html)                     # no Google Analytics anywhere
        self.assertNotIn(build.SITE["counter"], plain)                    # package copy: no visit counting
        self.assertIn(build.SITE["counter"], site)

    def test_save(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "explorer.html")
            self.assertEqual(app.main(["--save", path]), 0)
            with open(path, encoding="utf-8") as fh:
                self.assertIn("DTree Explorer", fh.read())


if __name__ == "__main__":
    unittest.main()
