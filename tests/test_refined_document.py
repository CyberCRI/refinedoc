from unittest import TestCase

from src.refinedoc.enumeration import TargetedPart
from src.refinedoc.refined_document import RefinedDocument


class TestRefinedDocument(TestCase):

    def test__compare(self):
        self.fail()

    def test__compare_candidates(self):
        self.fail()

    def test__detect_similar_lines(self):
        self.fail()

    def test_header(self):
        page0 = ["header 0", " lorem ipsum dolor sit amet"]
        page1 = ["header 1", " consectetur adipiscing elit"]
        page2 = [
            "header 2",
            "subheader 2",
            "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
        ]
        page3 = [
            "header 3",
            "subheader 3",
            "ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
        ]
        page4 = [
            "header 4",
            "subheader 4",
            "duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur",
        ]
        page5 = [
            "",
            "subheader 5",
            "excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum",
        ]
        page6 = [
            "header 6",
            "subheader 6",
            "sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium",
        ]
        content = [
            page0,
            page1,
            page2,
            page3,
            page4,
            page5,
            page6,
        ]
        rd = RefinedDocument(content=content)
        headers = rd.headers

        pages_with_header = [0, 1, 2, 3, 4, 6]
        pages_with_subheader = [2, 3, 4, 5, 6]
        for i, header in enumerate(headers):
            if i in pages_with_header:
                self.assertEqual(f"header {i}", header[0])
            if i in pages_with_subheader:
                self.assertEqual(f"subheader {i}", header[-1])

    def test_separate_footer(self):
        page0 = ["lorem ipsum dolor sit amet", "conescturs", "", "footer 0"]
        page1 = ["consectetur adipiscing elit", "blablabla", "", "footer 1"]
        page2 = [
            "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
            "sud flu bla blu bli",
            "surfooter 2",
            "footer 2",
        ]
        page3 = [
            "ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
            "such a test wololo",
            "surfooter 3",
            "footer 3",
        ]
        page4 = [
            "duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur",
            "unitest are annoying",
            "surfooter 4",
            "footer 4",
        ]
        page5 = [
            "excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum",
            "just here for the test",
            "surfooter 5",
            "",
        ]
        page6 = [
            "sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium",
            "always the same",
            "surfooter 6",
            "footer 6",
        ]
        content = [
            page0,
            page1,
            page2,
            page3,
            page4,
            page5,
            page6,
        ]
        rd = RefinedDocument(content=content)
        footers = rd.footers
        pages_with_footer = [0, 1, 2, 3, 4, 6]
        pages_with_subfooter = [2, 3, 4, 5, 6]

        for i, footer in enumerate(footers):
            if i in pages_with_footer:
                self.assertEqual(f"footer {i}", footer[-1])
            if i in pages_with_subfooter:
                self.assertEqual(f"surfooter {i}", footer[0])
