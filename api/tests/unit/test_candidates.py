import unittest
from unittest.mock import MagicMock

import candidates

class TestCandidates(unittest.TestCase):

    def side_effect_createCandidate(self, candidate):
        candidate['_id'] = 1

    def setUp(self):
        candidates.db = MagicMock()
        candidates.gClient = MagicMock()
        candidates.gName = 'dbase-name'
    
    def test_createCandidate(self):
        candidates.db.candidates.insert_one.side_effect = self.side_effect_createCandidate
        newCandidate = candidates.createCandidate({'name': 'Jhon'})
        self.assertIn('_id', newCandidate)

    def test_deleteCandidate(self):
        candidates.deleteCandidate(1)
        candidates.db.candidates.delete_one.assert_called_once()

    def test_dropDatabase(self):
        candidates.dropDatabase()
        candidates.gClient.drop_database.assert_called_with(candidates.gName)

    def test_getCandidates(self):
        r = candidates.getCandidates()
        self.assertIsInstance(r, list)

    def test_updateCandidate(self):
        res = MagicMock()
        res.matched_count = 1
        candidates.db.candidates.update_one.return_value = res
        r = candidates.updateCandidate({'_id': 1})
        self.assertTrue(r)
