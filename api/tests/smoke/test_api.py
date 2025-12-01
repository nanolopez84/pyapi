import unittest
import requests
from pprint import pprint

VERSION = 'v1'
BASE_URL = 'http://localhost:5000/api/' + VERSION

class TestApi(unittest.TestCase):

    def test_create_candidate(self):
        candidate = {'name': 'John', 'age': 35}
        r = requests.post(BASE_URL + '/candidate', json=candidate)
        self.assertEqual(r.status_code, 201, 'Should create a candidate')
        self.assertIn('_id', r.json(), 'New candidate should have _id')

    def test_delete_candidate(self):
        candidate = {'name': 'John', 'age': 35}
        r = requests.post(BASE_URL + '/candidate', json=candidate)
        candidate = r.json()

        r = requests.delete(BASE_URL + '/candidate/' + str(candidate['_id']), json=candidate)
        self.assertEqual(r.status_code, 204, 'Should delete the candidate')

        r = requests.get(BASE_URL + '/candidates')
        allCandidates = r.json()
        result = False
        try:
            fetchedCandidate = next(c for c in allCandidates if c['_id'] == candidate['_id'])
            result = True
        except StopIteration:
            pass
        self.assertEqual(result, False, 'Should not find the deleted candidate')

    def test_get_candidates(self):
        r = requests.get(BASE_URL + '/candidates')
        self.assertEqual(r.status_code, 200, 'Should get all candidates')

    def test_update_candidate(self):
        candidate = {'name': 'John', 'age': 35}
        r = requests.post(BASE_URL + '/candidate', json=candidate)
        candidate = r.json()

        candidate_id = candidate['_id']
        candidate['name'] = 'Jonathan'
        del candidate['_id']
        r = requests.patch(BASE_URL + '/candidate/' + candidate_id, json=candidate)
        self.assertEqual(r.status_code, 200, 'Should find the candidate')

        r = requests.get(BASE_URL + '/candidates')
        allCandidates = r.json()
        fetchedCandidate = next(c for c in allCandidates if c['_id'] == candidate_id)
        self.assertEqual(fetchedCandidate['name'], candidate['name'], 'Should update the candidate')

if __name__ == '__main__':
    unittest.main()
