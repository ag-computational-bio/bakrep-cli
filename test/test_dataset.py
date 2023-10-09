import unittest
from bakrep.model import Dataset, Result


def result(name: str, attributes: dict):
    return Result(name, attributes, "unknown", 0)


class FilterResultsTest(unittest.TestCase):

    @staticmethod
    def example_data():
        results = [
            result("a", {"type": "abc", "mode": "xy"}),
            result("b", {"type": "hhh", "mode": "jj"}),
            result("c", {"type": "233", "mode": "xy"}),
        ]
        dataset = Dataset("abc", results)
        return (dataset, results)

    def test_results_should_be_filtered_correctly_with_single_criterion(self):
        (d, r) = self.example_data()
        filtered = d.filter([{"type": "233"}])
        self.assertEquals(filtered, [r[2]])

    def test_results_should_be_filtered_correctly_with_multiple_criteria(self):
        (d, r) = self.example_data()
        filtered = d.filter([{"type": "abc"}, {"type": "233"}])
        self.assertEquals(filtered, [r[0], r[2]])

    def test_no_filters_should_include_all(self):
        (d, r) = self.example_data()
        filtered = d.filter([])
        self.assertEquals(filtered, r)

    def test_empty_filter_should_include_all(self):
        (d, r) = self.example_data()
        filtered = d.filter([{}])
        self.assertEquals(filtered, r)


if __name__ == '__main__':
    unittest.main()
