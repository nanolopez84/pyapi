import unittest
import uuid
from bson import ObjectId
from unittest.mock import MagicMock

from candidates_service import CandidatesService

class TestCandidates(unittest.TestCase):

    def side_effect_createCandidate(self, candidate):
        candidate['_id'] = 1

    def setUp(self):
        self.candidates_service = CandidatesService('test-' + str(uuid.uuid1())[:8], MagicMock())

    def tearDown(self):
        self.candidates_service._client.close()
    
    def test_createCandidate(self):
        self.candidates_service._db.candidates.insert_one.side_effect = self.side_effect_createCandidate
        newCandidate = self.candidates_service.create_candidate({'name': 'Jhon'})
        self.assertIn('_id', newCandidate)

    def test_deleteCandidate(self):
        self.candidates_service.delete_candidate(ObjectId())
        self.candidates_service._db.candidates.delete_one.assert_called_once()

    def test_dropDatabase(self):
        self.candidates_service.drop_database()
        self.candidates_service._client.drop_database.assert_called_with(self.candidates_service._name)

    def test_getCandidates(self):
        r = self.candidates_service.get_candidates()
        self.assertIsInstance(r, list)

    def test_updateCandidate(self):
        res = MagicMock()
        res.matched_count = 1
        self.candidates_service._db.candidates.update_one.return_value = res
        r = self.candidates_service.update_candidate({'_id': ObjectId()})
        self.assertTrue(r)
