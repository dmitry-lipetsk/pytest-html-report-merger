import time


class TestResultSet1:
    def test_1(self):
        time.sleep(1)
        assert True

    def test_2(self):
        time.sleep(2)
        lval = []
        # generate an index error and fail the test
        lval[3]


class TestResultSet2:
    def test_3(self):
        time.sleep(3)
        assert False

    def test_4(self):
        time.sleep(2)


class TestResultSet4:
    def test_5(self):
        time.sleep(4)
        assert True
