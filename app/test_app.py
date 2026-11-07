"""Demo-path regressions. Run: python -m unittest app.test_app."""
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest
from app.presentation import proposal_html, statuses

ROOT = Path(__file__).resolve().parents[1]


class FundingDeskTest(unittest.TestCase):
    def open(self):
        at = AppTest.from_file(str(ROOT / 'app/app.py')).run()
        self.assertFalse(at.exception)
        return at

    def test_historical_and_sources(self):
        at = self.open()
        r = at.session_state['evaluated_result']
        self.assertFalse(r['is_what_if'])
        self.assertEqual(r['permanent_need']['value'], 150211)
        self.assertEqual(r['temporary_need']['value'], 220000)
        self.assertIsNone(r['advance_savings']['net'])
        self.assertEqual(at.session_state['evaluated_scenario']['overrides'], {})
        rendered = '\n'.join(x.value for x in at.markdown)
        self.assertIn('Historical (as of 2026-11-07)', rendered)
        self.assertIn('https://habitatoc.org/', rendered)
        self.assertIn('https://santa-ana.gov/', rendered)

    def test_rate_months_cost_and_draft_refresh(self):
        at = self.open()
        at.toggle(key='what_if').set_value(True).run()
        at.selectbox(key='willing').select('Yes')
        at.selectbox(key='consent').select('Yes')
        at.checkbox(key='cost_known').check().run()
        self.assertEqual(at.session_state['evaluated_result']['advance_savings']['net'], 2950)
        at.button[0].click().run()
        self.assertFalse(at.exception)
        draft = at.session_state['proposal_html']
        self.assertIn('GIFT, NOT REPAID', draft)
        self.assertIn('REPAYABLE', draft)
        self.assertIn('WHAT-IF', draft)
        self.assertNotIn('$370,211', draft)  # No gift-plus-principal fundraising total.
        at.number_input(key='rate').set_value(2.0).run()
        self.assertEqual(at.session_state['evaluated_result']['advance_savings']['net'], 750)
        self.assertNotIn('proposal_html', at.session_state)
        at.number_input(key='months').set_value(12).run()
        self.assertEqual(at.session_state['evaluated_result']['advance_savings']['net'], 3500)
        at.toggle(key='what_if').set_value(False).run()
        self.assertFalse(at.session_state['evaluated_result']['is_what_if'])
        self.assertEqual(at.session_state['evaluated_scenario']['overrides'], {})

    def test_feasibility_distinguishes_zero_unknown_and_unverified(self):
        at = self.open()
        at.toggle(key='what_if').set_value(True).run()
        at.selectbox(key='line_verified').select('Yes').run()
        at.number_input(key='room').set_value(0)
        at.selectbox(key='willing').select('No').run()
        self.assertEqual(at.session_state['evaluated_result']['recommendation']['verdict'], 'no_bridge')
        at.selectbox(key='line_verified').select('Unknown').run()
        self.assertEqual(at.session_state['evaluated_result']['options'][0]['feasible'], 'unknown')
        at.selectbox(key='line_verified').select('No').run()
        self.assertFalse(at.session_state['evaluated_scenario']['overrides']['existing_line_available']['verified_current'])
        self.assertEqual(at.session_state['evaluated_result']['options'][0]['feasible'], 'unknown')

    def test_contingency_and_zero_duration(self):
        at = self.open()
        at.toggle(key='what_if').set_value(True).run()
        at.checkbox(key='cont_known').check().run()
        at.number_input(key='cont').set_value(200000)
        at.number_input(key='months').set_value(0).run()
        r = at.session_state['evaluated_result']
        self.assertEqual(r['permanent_need']['value'], 0)
        self.assertFalse(r['permanent_need']['upper_bound'])
        self.assertEqual(r['options'][0]['interest_cost'], 0)
        self.assertEqual(r['temporary_need']['value'], 220000)

    def test_fixture_never_calls_engine(self):
        at = self.open()
        with patch('engine.proposal.evaluate', side_effect=AssertionError('fixture must be static')):
            at.checkbox(key='fixture').check().run()
            self.assertFalse(at.exception)
            self.assertEqual(at.session_state['evaluated_result'], json.loads((ROOT / 'contracts/example_result.json').read_text()))
            at.button[0].click().run()
            self.assertFalse(at.exception)
            self.assertIn('upper bound', at.session_state['proposal_html'])
            self.assertIn('CONTRACT FIXTURE', at.session_state['proposal_html'])

    def test_legacy_fixture_status_fallback_and_html_escaping(self):
        case = json.loads((ROOT / 'contracts/example_case.json').read_text())
        r = json.loads((ROOT / 'contracts/example_result.json').read_text())
        s = statuses(r, case['facts'])
        self.assertEqual(s['a'], 'assumption')
        self.assertEqual(s['net'], 'unknown')
        case['title'] = '<script>alert(1)</script>'
        output = proposal_html(case, {}, r, case['facts'])
        self.assertNotIn('<script>', output)
        self.assertIn('&lt;script&gt;', output)


if __name__ == '__main__':
    unittest.main()
