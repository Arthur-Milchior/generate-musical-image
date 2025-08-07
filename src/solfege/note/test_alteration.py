class TestAlterationNote(unittest.TestCase):
    def test_from_name(self):
        self.assertEquals(Alteration.from_name("𝄪"), Alteration(2))
        self.assertEquals(Alteration.from_name("#"), Alteration(1))
        with self.assertRaises(Exception):
            self.assertEquals(Alteration.from_name("###"), Alteration(1))
