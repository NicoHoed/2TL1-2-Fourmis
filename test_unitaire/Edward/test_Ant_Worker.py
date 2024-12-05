import unittest
from unittest import mock
from random import randint
from main import Ant, Worker, Colony, LIFE_BY_ROLE, PROBABILITY_TO_FIND_FOOD

class TestAnt(unittest.TestCase):

    def test_ant_initialization(self):
        """Test the initialization of the ant class."""
        ant = Ant(role='worker')
        self.assertEqual(ant.position, [0, 0])
        self.assertEqual(ant.role, 'worker')
        self.assertEqual(ant._Ant__life, 0)
        self.assertEqual(ant._Ant__life_span, LIFE_BY_ROLE['worker'])

    def test_die_exact_lifespan(self):
        """Tests if an ant dies at the end of its life cycle."""
        ant = Ant(role='worker')
        ant._Ant__life = LIFE_BY_ROLE['worker'] - 1
        self.assertTrue(ant.die())
        self.assertEqual(ant._Ant__life, LIFE_BY_ROLE['worker'])

    def test_die_random_death(self):
        """Tests if an ant can die after it has reached more than half its life cycle."""
        ant = Ant(role='worker')
        ant._Ant__life = LIFE_BY_ROLE['worker'] // 2 + 1
        with mock.patch('main.randint', return_value=ant._Ant__life):
            self.assertTrue(ant.die())

    def test_x_property(self):
        """Test of the getter and setter for the x position."""
        ant = Ant(role='worker')
        ant.x = 5
        self.assertEqual(ant.x, 5)
        self.assertEqual(ant.position, [5, 0])

    def test_y_property(self):
        """Test of the getter and setter for the y position."""
        ant = Ant(role='worker')
        ant.y = 10
        self.assertEqual(ant.y, 10)
        self.assertEqual(ant.position, [0, 10])

    def test_ant_string_representation(self):
        """Test of the __str__ method."""
        ant = Ant(role='queen')
        self.assertEqual(str(ant), 'queen')


class TestWorker(unittest.TestCase):

    def setUp(self):
        """Initialises colony and worker for the tests."""
        self.colony = Colony(ant_count=1)
        self.worker = Worker(self.colony)

    def test_worker_initialization(self):
        """Test the initialization of a worker."""
        self.assertEqual(self.worker.role, 'worker')
        self.assertEqual(self.worker.have_food, False)
        self.assertIs(self.worker.colony, self.colony)

    def test_find_food_success(self):
        """Tests if a worker finds food."""
        with mock.patch('main.randint', return_value=PROBABILITY_TO_FIND_FOOD + 1):  # Force succès
            self.assertTrue(self.worker.find_food())
            self.assertTrue(self.worker.have_food)

    def test_find_food_failure(self):
        """Tests if a worker does not find food."""
        with mock.patch('main.randint', return_value=PROBABILITY_TO_FIND_FOOD - 1):  # Force échec
            self.assertFalse(self.worker.find_food())
            self.assertFalse(self.worker.have_food)

    def test_drop_food(self):
        """Tests if a worker does not have food anymore."""
        self.worker.have_food = True
        self.worker.drop_food()
        self.assertFalse(self.worker.have_food)


if __name__ == '__main__':
    unittest.main()
