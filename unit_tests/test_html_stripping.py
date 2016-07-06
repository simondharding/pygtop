from unittest import TestCase
from pygtop.shared import strip_html

class HtmlStripTest(TestCase):

    def setUp(self):
        self.name = lambda: "5<sup>AF</sup>-barns&ndash;nool<sub>5</sub>"
        self.synonyms = lambda: ["name1", "name<sup>2</sup>", "name<sub>3</sub>"]



class DecoratorTests(HtmlStripTest):

    def test_decorator_not_normally_noticable(self):
        decorated_name = strip_html(self.name)
        self.assertEqual(
         decorated_name(),
         "5<sup>AF</sup>-barns&ndash;nool<sub>5</sub>"
        )
        decorated_synonyms = strip_html(self.synonyms)
        self.assertEqual(
         decorated_synonyms(),
         ["name1", "name<sup>2</sup>", "name<sub>3</sub>"]
        )
