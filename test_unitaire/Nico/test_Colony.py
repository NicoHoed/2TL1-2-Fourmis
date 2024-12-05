import unittest
from unittest.mock import Mock
from lib.threat import Threat  # Si nécessaire, importez également Threat
from config import *  # Importez les constantes nécessaires
import sys
import os

# ------------
# PAS FINI
# ------------

# chemin de la racine du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from main import Colony, Worker, Soldier, Queen, Nest


class TestColony(unittest.TestCase):

    def setUp(self):
        """Configure une colonie avec un état de départ standard pour chaque test."""
        self.colony = Colony(ant_count=5, food_stock=50, nest_capacity=10)

    def test_initialization(self):
        """Teste que la colonie est correctement initialisée."""
        self.assertTrue(self.colony.live)
        self.assertEqual(len(self.colony.ant), 4)  # 1 reine + 4 ouvrières
        self.assertEqual(self.colony.nest.food_stock, 50)
        self.assertEqual(self.colony.nest.ant_capacity, 10)
        self.assertIsInstance(self.colony.queen, Queen)
        self.assertEqual(self.colony.nest.level, 1)

    def test_add_ant(self):
        """Teste l'ajout de nouvelles fourmis à la colonie."""
        initial_ant_count = len(self.colony.ant)
        self.colony.ant = Worker(self.colony)  # Ajoute un ouvrier
        self.assertEqual(len(self.colony.ant), initial_ant_count + 1)

        # Teste la limite de capacité
        for _ in range(self.colony.nest.ant_capacity):
            self.colony.ant = Worker(self.colony)
        self.assertEqual(len(self.colony.ant), self.colony.nest.ant_capacity)

    def test_manage_resources(self):
        # Initialisation de la colonie avec des valeurs connues
        colony = Colony(ant_count=5, food_stock=50)  # 1 reine, 4 workers
        expected_food = 50 - (1 * 5 + 4 * 1)  # Reine: 5, Workers: 1 chacun

        # Appel de la méthode
        colony.manage_ressources()

        # Vérification
        self.assertEqual(colony.nest.food_stock, expected_food)

        print(f"Initial food stock: {colony.nest.food_stock}")
        print(f"Food consumed: {food_consumed}")

    def test_expand_nest(self):
        """Teste l'expansion du nid lorsque la capacité est presque atteinte."""
        # Remplit la colonie presque jusqu'à sa capacité
        for _ in range(self.colony.nest.ant_capacity - 10):
            self.colony.ant = Worker(self.colony)

        initial_capacity = self.colony.nest.ant_capacity
        self.colony.manage_expansion_nest()
        self.assertGreaterEqual(self.colony.nest.ant_capacity, initial_capacity)

    def test_react_to_threat(self):
        """Teste la réaction de la colonie à une menace."""
        mock_threat = Threat(type="Spider", health=50, strength=10)
        initial_ant_count = len(self.colony.ant)
        result = self.colony.react_to_threat(mock_threat)

        # Vérifie que la menace est gérée correctement
        self.assertIn("a Spider attack the colony", result)
        self.assertLessEqual(len(self.colony.ant), initial_ant_count)  # Certaines fourmis peuvent mourir

    def test_destruction_of_nest(self):
        """Teste la destruction de la colonie."""
        self.colony.destruct_nest()
        self.assertFalse(self.colony.live)

    def test_colony_info(self):
        """Teste que les informations sur la colonie sont correctement calculées."""
        info = self.colony.info()
        nb_worker = sum(1 for ant in self.colony.ant if ant.role == 'worker')
        nb_soldier = sum(1 for ant in self.colony.ant if ant.role == 'soldier')

        self.assertEqual(info[0], len(self.colony.ant))
        self.assertEqual(info[1], self.colony.nest.ant_capacity)
        self.assertEqual(info[2], self.colony.nest.food_stock)
        self.assertEqual(info[3], self.colony.nest.food_capacity)
        self.assertEqual(info[4], self.colony.nest.level)
        self.assertEqual(info[5], nb_worker)
        self.assertEqual(info[6], nb_soldier)

if __name__ == "__main__":
    unittest.main()
