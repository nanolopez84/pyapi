import unittest
import uuid
from pprint import pprint

import candidates

class TestService(unittest.TestCase):

    def setUp(self):
        tmpName = 'test-' + str(uuid.uuid1())[:8]
        candidates.init(tmpName)

    def tearDown(self):
        candidates.dropDatabase()

    def test_create_candidate(self):
        candidate = {'name': 'John'}
        candidates.createCandidate(candidate)
        self.assertIn('_id', candidate, 'New candidate should have _id')

    def test_delete_candidate(self):
        candidate = {'name': 'John'}
        candidates.createCandidate(candidate)
        candidates.deleteCandidate(candidate['_id'])
        allCandidates = candidates.getCandidates()
        result = False
        try:
            fetchedCandidate = next(c for c in allCandidates if c['_id'] == candidate['_id'])
        except StopIteration:
            result = True
        self.assertEqual(result, True, 'Should delete the candidate')

    def test_get_candidates(self):
        allCandidates = candidates.getCandidates()
        self.assertIsInstance(allCandidates, list, 'Should get all candidates')

    def test_update_candidate(self):
        candidate = {'name': 'John'}
        candidates.createCandidate(candidate)
        candidate['name'] = 'Jonathan'
        candidates.updateCandidate(candidate)
        allCandidates = candidates.getCandidates()
        fetchedCandidate = next(c for c in allCandidates if c['_id'] == candidate['_id'])
        self.assertEqual(fetchedCandidate['name'], candidate['name'], 'Should update the candidate')

if __name__ == '__main__':
    unittest.main()
