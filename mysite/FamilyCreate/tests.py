from django.test import TestCase
from django.test import Client
import unittest

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_det(self):
        urls = ("/register","/login","/createFamily","/connect_family_key", "/connect_family_pas", "/room/24")
        for i in urls:
            response = self.client.get(i)
            self.assertEqual(response.status_code, 200)
        
        
        