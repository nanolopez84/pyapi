import pymongo
import unittest
import uuid
from pprint import pprint

from candidates_service import CandidatesService

class TestService(unittest.TestCase):

    def setUp(self):
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        temp_name = 'test-' + str(uuid.uuid1())[:8]
        self.candidates_service = CandidatesService(temp_name, mongo_client)

    def tearDown(self):
        self.candidates_service.drop_database()

    def test_create_candidate(self):
        candidate = {'name': 'John'}
        self.candidates_service.create_candidate(candidate)
        self.assertIn('_id', candidate, 'New candidate should have _id')

    def test_delete_candidate(self):
        candidate = {'name': 'John'}
        self.candidates_service.create_candidate(candidate)
        self.candidates_service.delete_candidate(candidate['_id'])
        allCandidates = self.candidates_service.get_candidates()
        result = False
        try:
            fetchedCandidate = next(c for c in allCandidates if c['_id'] == candidate['_id'])
        except StopIteration:
            result = True
        self.assertEqual(result, True, 'Should delete the candidate')

    def test_get_candidates(self):
        allCandidates = self.candidates_service.get_candidates()
        self.assertIsInstance(allCandidates, list, 'Should get all candidates')

    def test_update_candidate(self):
        candidate = {'name': 'John', 'age': 40}
        self.candidates_service.create_candidate(candidate)
        candidate['name'] = 'Jonathan'
        self.candidates_service.update_candidate(candidate)
        allCandidates = self.candidates_service.get_candidates()
        fetchedCandidate = next(c for c in allCandidates if c['_id'] == candidate['_id'])
        self.assertEqual(fetchedCandidate['name'], candidate['name'], 'Should update the candidate')

if __name__ == '__main__':
    unittest.main()
