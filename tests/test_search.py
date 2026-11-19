import io
import unittest

from alfred_rfc.search import alfred_item, search_rfc
from rfc import parse_index


class SearchTest(unittest.TestCase):
    def test_exact_rfc_number(self):
        for query in ('9110', 'RFC9110', 'rfc 09110'):
            with self.subTest(query=query):
                (result,) = search_rfc(query, 10)
                self.assertEqual(result['text'], 'RFC9110')
                item = alfred_item(result)
                self.assertEqual(item['arg'], 'https://www.rfc-editor.org/rfc/rfc9110.html')
                self.assertEqual(item['text']['copy'], item['quicklookurl'])

    def test_keywords_and_limit(self):
        results = search_rfc('  transport   QUIC ', 3)
        self.assertEqual(len(results), 3)
        self.assertEqual(search_rfc('', 10), [])
        self.assertEqual(search_rfc('QUIC', 0), [])

    def test_xml_uses_current_status_and_preserves_abstract_text(self):
        source = io.StringIO("""
            <rfc-index xmlns="https://www.rfc-editor.org/rfc-index">
              <rfc-entry>
                <doc-id>RFC0001</doc-id><title>Example</title>
                <current-status>HISTORIC</current-status>
                <abstract><p>First <em>part</em>.</p><p>Second part.</p></abstract>
              </rfc-entry>
            </rfc-index>
        """)
        (record,) = parse_index(source)
        self.assertEqual(record['text'], 'RFC1')
        self.assertEqual(record['status'], 'HISTORIC')
        self.assertIn('Second part.', record['note_with_text'])
