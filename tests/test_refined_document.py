from unittest import TestCase

from refinedoc.refined_document import RefinedDocument


class TestRefinedDocument(TestCase):

    def test__compare(self):
        rd = RefinedDocument(content=[])
        self.assertEqual(1.0, rd._compare("same", "same"))
        self.assertEqual(1.0, rd._compare("same 0", "same 1"))
        self.assertLess(rd._compare("same", "very diferrent sentence"), 0.5)

        rd.ratio_speed = 2
        self.assertEqual(1.0, rd._compare("same", "same"))
        self.assertLess(rd._compare("same", "very different sentence"), 0.5)

        rd.ratio_speed = 3
        self.assertEqual(1.0, rd._compare("same", "same"))
        self.assertLess(rd._compare("same", "very different sentence"), 0.5)

        rd.ratio_speed = 4
        with self.assertRaises(ValueError):
            rd._compare("same", "same")

    def test__compare_candidates(self):
        rd = RefinedDocument(content=[])
        self.assertEqual(
            rd._compare_candidates(
                to_compare_candidates=["same", "same", "same"], from_compare="same"
            ),
            1.0,
        )
        self.assertLess(
            rd._compare_candidates(
                to_compare_candidates=[
                    "very different sentence",
                    "lorem ipsum",
                    "there is lot of different things to test",
                ],
                from_compare="same",
            ),
            0.5,
        )

    def test__detect_similar_lines(self):
        rd = RefinedDocument(content=[])
        dsl = rd._detect_similar_lines(
            candidates=[
                "header 2",
                "subheader 2",
                "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
            ],
            positional_weights=[1.0, 0.75, 0.5],
            local_neighbours=[
                [
                    "header 3",
                    "subheader 3",
                    "ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
                ],
                [
                    "header 4",
                    "subheader 4",
                    "duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur",
                ],
            ],
        )

        self.assertListEqual(dsl, ["header 2", "subheader 2"])

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

    def test_header_roman_numerals(self):
        page0 = ["header 0", " lorem ipsum dolor sit amet"]
        page1 = ["header I", " consectetur adipiscing elit"]
        page2 = [
            "header II",
            "subheader II",
            "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
        ]
        page3 = [
            "header III",
            "subheader III",
            "ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
        ]
        page4 = [
            "header IV",
            "subheader IV",
            "duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur",
        ]
        page5 = [
            "",
            "subheader V",
            "excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum",
        ]
        page6 = [
            "header VI",
            "subheader VI",
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

        for i, header in enumerate(headers):
            if i == 2:
                self.assertEqual("header II", header[0])

            if i == 3:
                self.assertEqual("header III", header[0])
            if i == 4:
                self.assertEqual("header IV", header[0])
            if i == 6:
                self.assertEqual("header VI", header[0])

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

    def test_refine_text(self):
        document = [
            [
                "header 1",
                "subheader 1",
                "lorem ipsum dolor sit amet",
                "consectetur adipiscing elit",
                "footer 1",
            ],
            [
                "header 2",
                "subheader 2",
                "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
                "footer 2",
            ],
            [
                "header 3",
                "subheader 3",
                "ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
                "footer 3",
            ],
            [
                "header 4",
                "subheader 4",
                "duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur",
                "footer 4",
            ],
        ]

        rd = RefinedDocument(content=document)
        h_dr = rd.headers
        f_dr = rd.footers
        b_dr = rd.body

        h_ref = [
            ["header 1", "subheader 1"],
            ["header 2", "subheader 2"],
            ["header 3", "subheader 3"],
            ["header 4", "subheader 4"],
        ]

        f_ref = [
            ["footer 1"],
            ["footer 2"],
            ["footer 3"],
            ["footer 4"],
        ]

        b_ref = [
            ["lorem ipsum dolor sit amet", "consectetur adipiscing elit"],
            ["sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"],
            [
                "ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat"
            ],
            [
                "duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur"
            ],
        ]

        self.assertListEqual(h_dr, h_ref)
        self.assertListEqual(f_dr, f_ref)
        self.assertListEqual(b_dr, b_ref)

    def test_various_qty_lines(self):
        document = [
            [
                "header 1",
                "subheader 1",
                "lorem ipsum dolor sit amet",
                "consectetur adipiscing elit",
                "footer 1",
            ],
            [
                "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
            ],
            [
                "ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
            ],
            [
                "duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur",
            ],
        ]

        rd = RefinedDocument(content=document)

        h_dr = rd.headers
        f_dr = rd.footers
        b_dr = rd.body

        h_ref = [
            [],
            [],
            [],
            [],
        ]

        f_ref = [
            [],
            [],
            [],
            [],
        ]

        b_ref = [
            [
                "header 1",
                "subheader 1",
                "lorem ipsum dolor sit amet",
                "consectetur adipiscing elit",
                "footer 1",
            ],
            ["sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"],
            [
                "ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat"
            ],
            [
                "duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur"
            ],
        ]

        self.assertListEqual(h_dr, h_ref)
        self.assertListEqual(f_dr, f_ref)
        self.assertListEqual(b_dr, b_ref)

    def test_various_qty_lines2(self):
        document = [
            [
                "lorem ipsum dolor sit amet",
            ],
            [
                "header 2",
                "subheader 2",
                "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
                "footer 2",
            ],
            [
                "ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
            ],
            [
                "duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur",
            ],
        ]

        rd = RefinedDocument(content=document)

        h_dr = rd.headers
        f_dr = rd.footers
        b_dr = rd.body

        h_ref = [
            [],
            [],
            [],
            [],
        ]

        f_ref = [
            [],
            [],
            [],
            [],
        ]

        b_ref = [
            [
                "lorem ipsum dolor sit amet",
            ],
            [
                "header 2",
                "subheader 2",
                "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
                "footer 2",
            ],
            [
                "ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat"
            ],
            [
                "duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur"
            ],
        ]

        self.assertListEqual(h_dr, h_ref)
        self.assertListEqual(f_dr, f_ref)
        self.assertListEqual(b_dr, b_ref)

    def test_empty_document(self):
        document = []

        rd = RefinedDocument(content=document)

        h_dr = rd.headers
        f_dr = rd.footers
        b_dr = rd.body

        h_ref = []

        f_ref = []

        b_ref = []

        self.assertListEqual(h_dr, h_ref)
        self.assertListEqual(f_dr, f_ref)
        self.assertListEqual(b_dr, b_ref)

    def test_single_page_document(self):
        document = [
            [
                "header 1",
                "subheader 1",
                "lorem ipsum dolor sit amet",
                "consectetur adipiscing elit",
                "footer 1",
            ]
        ]

        rd = RefinedDocument(content=document)

        h_dr = rd.headers
        f_dr = rd.footers
        b_dr = rd.body

        h_ref = [[]]

        f_ref = [[]]

        b_ref = [
            [
                "header 1",
                "subheader 1",
                "lorem ipsum dolor sit amet",
                "consectetur adipiscing elit",
                "footer 1",
            ]
        ]

        self.assertListEqual(h_dr, h_ref)
        self.assertListEqual(f_dr, f_ref)
        self.assertListEqual(b_dr, b_ref)
