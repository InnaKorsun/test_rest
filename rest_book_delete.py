import unittest
import requests

class DeleteBookTests(unittest.TestCase):


    def setUp(self):

        self.book_url = "http://pulse-rest-testing.herokuapp.com/books/"
        self.test_book = {"title": "Fight club", "author": "Chack Pallanik"}
        self.update_info = {"title": "Djerelo", "author": "Ann Read"}

        r = requests.post(self.book_url, data=self.test_book)

        self.book_id = r.json()['id']#id just created book for test

        self.assertEqual(r.status_code, 201)
        responce_id = requests.get(self.book_url + str(self.book_id))
        self.assertEqual(responce_id.status_code, 200) #check that book present in list

    def test_delete_book_pos(self):

        r = requests.delete(self.book_url + str(self.book_id))
        self.assertEqual(r.status_code,204)#check that book deleted(by status code)

        responce_get = requests.get(self.book_url + str(self.book_id))
        self.assertEqual(responce_get.status_code, 404) #check that book doen't present in list

    def test_delete_book_notExistId_neg(self):

        r = requests.delete(self.book_url + str(self.book_id+10000))# try delete book with d which doesn;t exist
        self.assertEqual(r.status_code,404)#check that book deleted(by status code)




