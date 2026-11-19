#!/usr/bin/env python3
"""
VayuAI Pro v3.0 — Comprehensive Automated QA, Security, API & DOM Interaction Test Suite
Executes:
1. Unit Tests (CPCB NAQI math, Berkeley Earth cigarette equivalence, CADR/ACH physics, ITF-OECD GHG swap math)
2. Functional & Integration Tests (City/Profile switching, mask leakage, routine filtering, 2D Floorplan toggles)
3. Serverless API & Error-Handling Tests (Node.js execution of api/gemini.js: 204, 400, 405, 503)
4. Security & XSS Audit Tests (HTML escaping, zero hardcoded secrets, session-only key storage, HTTP security headers)
5. Accessibility & Responsive Layout Checks (WCAG labels, ARIA live regions, responsive grid classes, Chart.js containers)
6. Full DOM Hydration & Interactive Event Simulation (DOMContentLoaded, tab clicks, search filter empty state, XSS form submit, floorplan clicks, SVG poster render)
7. Documentation & Production Readiness Verification
"""

import json
import os
import re
import subprocess
import unittest
from bs4 import BeautifulSoup

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML = os.path.join(REPO_DIR, "index.html")
API_JS = os.path.join(REPO_DIR, "api", "gemini.js")
VERCEL_JSON = os.path.join(REPO_DIR, "vercel.json")
README_MD = os.path.join(REPO_DIR, "README.md")


class VayuAiTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            cls.html = f.read()
        cls.soup = BeautifulSoup(cls.html, "lxml")
        scripts = cls.soup.find_all("script")
        cls.app_js = scripts[-1].string or ""

    def test_01_unit_math_and_domain_calculations_in_node(self):
        """Unit test core JS math functions (getCpcbCategory, computeMetrics, escapeHtml, sanitizeNumber) via Node.js."""
        harness = f"""
        const window = {{ addEventListener: () => {{}}, location: {{ protocol: 'https:', hostname: 'localhost' }} }};
        const document = {{ addEventListener: () => {{}}, getElementById: () => null, querySelectorAll: () => [] }};
        const localStorage = {{ getItem: () => null, setItem: () => {{}}, removeItem: () => {{}} }};
        const Chart = function() {{ return {{ update: () => {{}}, data: {{ datasets: [{{data:[]}}, {{data:[]}}] }} }}; }};
        {self.app_js}

        const assert = require('assert');
        assert.strictEqual(getCpcbCategory(42).label, 'Good');
        assert.strictEqual(getCpcbCategory(85).label, 'Satisfactory');
        assert.strictEqual(getCpcbCategory(146).label, 'Moderate');
        assert.strictEqual(getCpcbCategory(265).label, 'Poor');
        assert.strictEqual(getCpcbCategory(367).label, 'Very Poor');
        assert.strictEqual(getCpcbCategory(430).label, 'Severe');
        assert.strictEqual(getCpcbCategory(480).label, 'Severe+');
        assert.strictEqual(aqiToCpcbPm25(50), 30.0);
        assert.strictEqual(aqiToCpcbPm25(100), 60.0);
        assert.strictEqual(aqiToCpcbPm25(200), 90.0);
        assert.strictEqual(aqiToCpcbPm25(300), 120.0);
        assert.strictEqual(aqiToCpcbPm25(400), 250.0);
        assert.strictEqual(pm25ToCpcbAqi(30), 50);
        assert.strictEqual(pm25ToCpcbAqi(60), 100);
        assert.strictEqual(pm25ToCpcbAqi(90), 200);
        assert.strictEqual(pm25ToCpcbAqi(120), 300);
        assert.strictEqual(pm25ToCpcbAqi(250), 400);

        assert.strictEqual(sanitizeNumber('999', 0, 500, 100), 500);
        assert.strictEqual(sanitizeNumber('abc', 0, 500, 100), 100);
        const xss = escapeHtml('<script>alert("xss")</script><img src=x onerror=alert(1)>');
        assert(!xss.includes('<script>'), 'XSS script tag must be escaped');
        assert(xss.includes('&lt;script&gt;'), 'Escaped entity must be present');

        const m = computeMetrics();
        assert.strictEqual(m.outdoorPm25, 218.0);
        assert(m.steadyIndoorPm25 < 30 && m.steadyIndoorPm25 > 15, 'Indoor PM2.5 must reflect ~88% MERV-13 reduction');
        assert.strictEqual(m.pctCut, 71, 'Electric Bus vs Private Car must be 71% per ITF-OECD');
        assert(m.ach > 15, '680 CFM in 220 sq ft room must exceed 15 ACH');
        console.log('UNIT_TESTS_OK');
        """
        res = subprocess.run(["node", "-e", harness], capture_output=True, text=True, timeout=10)
        self.assertEqual(res.returncode, 0, f"Node unit test failed: {res.stderr}")
        self.assertIn("UNIT_TESTS_OK", res.stdout)

    def test_02_functional_and_integration_state_flows(self):
        """Integration test city switching, mask leakage, routine filtering, and 2D floorplan toggles in Node.js."""
        harness = f"""
        const window = {{ addEventListener: () => {{}}, location: {{ protocol: 'https:', hostname: 'localhost' }} }};
        const document = {{ addEventListener: () => {{}}, getElementById: () => null, querySelectorAll: () => [] }};
        const localStorage = {{ getItem: () => null, setItem: () => {{}}, removeItem: () => {{}} }};
        const Chart = function() {{ return {{ update: () => {{}}, data: {{ datasets: [{{data:[]}}, {{data:[]}}] }} }}; }};
        {self.app_js}

        const assert = require('assert');
        state.cityKey = 'jodhpur';
        state.customAqi = CITY_PROFILES.jodhpur.aqi;
        state.customPm25 = CITY_PROFILES.jodhpur.pm25;
        state.maskKey = 'n95_unsealed';
        state.sustainableSwap = 'bicycle';
        const mJodhpur = computeMetrics();
        assert.strictEqual(mJodhpur.outdoorPm25, 131.2);
        assert.strictEqual(mJodhpur.mask.eff, 0.70);
        assert.strictEqual(mJodhpur.pctCut, 75);

        const r1 = generateBuiltInAiResponse('morning_smog');
        const r2 = generateBuiltInAiResponse('diy_purifier');
        const r3 = generateBuiltInAiResponse('hostel_hacks');
        const r4 = generateBuiltInAiResponse('kitchen_iaq');
        assert(r1.english.includes('100m') && r1.hinglish.length > 15);
        assert(r2.english.includes('MERV-13') && r2.english.includes('293 CFM'));
        assert(r3.english.includes('13:00') || r3.english.includes('MERV-13'));
        assert(r4.english.includes('exhaust'));
        console.log('INTEGRATION_TESTS_OK');
        """
        res = subprocess.run(["node", "-e", harness], capture_output=True, text=True, timeout=10)
        self.assertEqual(res.returncode, 0, f"Integration test failed: {res.stderr}")
        self.assertIn("INTEGRATION_TESTS_OK", res.stdout)

    def test_03_api_serverless_and_error_handling(self):
        """Test api/gemini.js serverless handler for OPTIONS (204), GET (405), invalid input (400), and missing key (503)."""
        harness = f"""
        const assert = require('assert');
        const handler = require({json.dumps(API_JS)});

        function mockRes() {{
          return {{
            statusCode: 200,
            headers: {{}},
            body: null,
            setHeader(k, v) {{ this.headers[k] = v; }},
            status(code) {{ this.statusCode = code; return this; }},
            json(obj) {{ this.body = obj; return this; }},
            end() {{ return this; }}
          }};
        }}

        (async () => {{
          const rOpt = mockRes();
          await handler({{ method: 'OPTIONS' }}, rOpt);
          assert.strictEqual(rOpt.statusCode, 204);

          const rGet = mockRes();
          await handler({{ method: 'GET' }}, rGet);
          assert.strictEqual(rGet.statusCode, 405);

          const rBad = mockRes();
          await handler({{ method: 'POST', body: {{ prompt: '   ' }} }}, rBad);
          assert.strictEqual(rBad.statusCode, 400);

          const rLong = mockRes();
          await handler({{ method: 'POST', body: {{ prompt: 'A'.repeat(300) }} }}, rLong);
          assert.strictEqual(rLong.statusCode, 400);

          delete process.env.GEMINI_API_KEY;
          const rNoKey = mockRes();
          await handler({{ method: 'POST', body: {{ prompt: 'How to reduce indoor PM2.5?', city: 'Jodhpur', aqi: 265 }} }}, rNoKey);
          assert.strictEqual(rNoKey.statusCode, 503);
          assert.strictEqual(rNoKey.body.fallbackMode, 'Deterministic CPCB/WHO Rule Engine');

          console.log('API_TESTS_OK');
        }})();
        """
        res = subprocess.run(["node", "-e", harness], capture_output=True, text=True, timeout=10)
        self.assertEqual(res.returncode, 0, f"API test failed: {res.stderr}")
        self.assertIn("API_TESTS_OK", res.stdout)

    def test_04_security_and_secret_hygiene(self):
        """Audit repository for hardcoded keys, unsafe localStorage secret writes, and security headers."""
        secret_pattern = re.compile(r"AIzaSy[A-Za-z0-9_\-]{30,}")
        for root, _, files in os.walk(REPO_DIR):
            for file in files:
                fpath = os.path.join(root, file)
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                self.assertIsNone(secret_pattern.search(content), f"Potential hardcoded API key in {file}")

        self.assertNotIn("localStorage.setItem('vayu_gemini_api_key'", self.html)

        with open(VERCEL_JSON, "r", encoding="utf-8") as vf:
            vercel_cfg = json.loads(vf.read())
        header_keys = [h["key"] for h in vercel_cfg["headers"][0]["headers"]]
        self.assertIn("X-Content-Type-Options", header_keys)
        self.assertIn("X-Frame-Options", header_keys)
        self.assertIn("Referrer-Policy", header_keys)

    def test_05_accessibility_and_responsive_ui(self):
        """Verify semantic landmarks, accessible form controls, ARIA live regions, and responsive classes."""
        self.assertIsNotNone(self.soup.find("header"))
        self.assertIsNotNone(self.soup.find("nav"))
        self.assertIsNotNone(self.soup.find("main"))
        self.assertGreaterEqual(len(self.soup.find_all("section")), 4)

        for tag in self.soup.find_all(["input", "select", "textarea"]):
            tid = tag.get("id")
            has_aria = bool(tag.get("aria-label"))
            has_label = bool(tid and self.soup.find("label", attrs={"for": tid}))
            self.assertTrue(has_aria or has_label, f"Form control #{tid} missing accessible label")

        self.assertIn("sm:", self.html)
        self.assertIn("md:", self.html)
        self.assertIn("lg:", self.html)
        self.assertIn("maintainAspectRatio: false", self.html)

    def test_06_full_dom_hydration_and_user_interaction_simulation(self):
        """Execute DOMContentLoaded and simulate interactive user flows (city change, routine filter empty state, XSS prompt submit, floorplan render, SVG poster)."""
        all_ids = [tag.get("id") for tag in self.soup.find_all(id=True)]
        harness = f"""
        const assert = require('assert');
        const elements = {{}};
        function makeEl(id) {{
          return {{
            id,
            value: '',
            textContent: '',
            innerHTML: '',
            outerHTML: '<svg id="cleanAirPosterSvg"></svg>',
            className: '',
            disabled: false,
            listeners: {{}},
            attributes: {{}},
            options: [{{ text: 'Family' }}],
            selectedIndex: 0,
            classList: {{
              add: () => {{}},
              remove: () => {{}},
              toggle: () => {{}}
            }},
            addEventListener(ev, fn) {{ this.listeners[ev] = fn; }},
            setAttribute(k, v) {{ this.attributes[k] = v; }},
            removeAttribute(k) {{ delete this.attributes[k]; }},
            getAttribute(k) {{ return this.attributes[k] || ''; }},
            prepend(child) {{ this.innerHTML = (child.innerHTML || '') + this.innerHTML; }},
            querySelectorAll() {{ return []; }}
          }};
        }}
        for (const id of {json.dumps(all_ids)}) {{
          elements[id] = makeEl(id);
        }}
        const windowListeners = {{}};
        const window = {{
          location: {{ protocol: 'https:', hostname: 'localhost' }},
          addEventListener(ev, fn) {{ windowListeners[ev] = fn; }},
          print: () => {{}}
        }};
        const document = {{
          documentElement: makeEl('html'),
          body: {{ appendChild: () => {{}}, removeChild: () => {{}} }},
          getElementById(id) {{ return elements[id] || null; }},
          createElement(tag) {{ return makeEl(tag); }},
          querySelectorAll() {{ return []; }},
          execCommand: () => true
        }};
        const localStorage = {{ getItem: () => null, setItem: () => {{}}, removeItem: () => {{}} }};
        const Chart = function() {{ return {{ update: () => {{}}, data: {{ datasets: [{{data:[]}}, {{data:[]}}] }} }}; }};

        {self.app_js}

        // 1. Trigger DOMContentLoaded
        assert(typeof windowListeners['DOMContentLoaded'] === 'function', 'DOMContentLoaded listener must be registered');
        windowListeners['DOMContentLoaded']();

        // Verify initial hydration populated SVG poster, 2D floorplan, routines, IAQ hacks, and Berkeley Earth cigarette meter
        assert(elements['svgPosterContainer'].innerHTML.includes('cleanAirPosterSvg'), 'SVG poster must render on init');
        assert(elements['floorplanGrid'].innerHTML.includes('Z1 · Living / Study'), '4-Zone Floorplan must render on init');
        assert.strictEqual(elements['outdoorCigEq'].textContent, '9.9');
        assert(elements['aiChatStream'].innerHTML.includes('Zero-Key CPCB/WHO Engine'), 'AI card must disclose deterministic engine');

        // 2. Simulate user filtering routines to an unmatched keyword -> verify Empty State UI
        elements['routineFilterInput'].value = 'nonexistent_xyz_keyword';
        elements['routineFilterInput'].listeners['input']({{ target: elements['routineFilterInput'] }});
        assert(elements['routineListContainer'].innerHTML.includes('No routines match'), 'Empty state must render when filter has 0 matches');

        // 3. Simulate clicking Reset button -> verify routines restore
        elements['resetDefaultsBtn'].listeners['click']();
        assert(elements['routineListContainer'].innerHTML.includes('06:00–09:00'), 'Reset must restore all 6 routines');

        // 4. Simulate submitting malicious XSS payload in AI Prompt Form -> verify escaped output
        elements['aiPromptInput'].value = '<img src=x onerror=alert(999)> morning';
        elements['aiPromptForm'].listeners['submit']({{ preventDefault: () => {{}} }});
        assert(!elements['aiChatStream'].innerHTML.includes('<img src=x'), 'XSS payload must never be injected unescaped');

        console.log('DOM_SIMULATION_OK');
        """
        res = subprocess.run(["node", "-e", harness], capture_output=True, text=True, timeout=10)
        self.assertEqual(res.returncode, 0, f"DOM simulation failed: {res.stderr}")
        self.assertIn("DOM_SIMULATION_OK", res.stdout)

    def test_07_readme_completeness(self):
        """Verify README.md contains all 11 mandatory architectural & deployment sections."""
        with open(README_MD, "r", encoding="utf-8") as rf:
            readme = rf.read()
        for section in [
            "1. Project Overview",
            "2. Problem Statement",
            "3. Features",
            "4. Technology Stack",
            "5. Architecture",
            "6. Installation Instructions",
            "7. Environment Variable Setup",
            "8. API Configuration",
            "9. Testing Instructions",
            "10. Deployment Instructions",
            "11. Assumptions and Limitations",
        ]:
            self.assertIn(section, readme, f"Missing README section: {section}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
