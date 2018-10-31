import unittest
import requests

class UpdateBookTests(unittest.TestCase):


    def setUp(self):

        self.book_url = "http://pulse-rest-testing.herokuapp.com/books/"
        self.test_book = {"title": "Fight club", "author": "Chack Pallanik"}
        self.update_info = {"title": "Djerelo", "author": "Ann Read"}

        r = requests.post(self.book_url, data=self.test_book)

        self.book_id = r.json()['id']#id just created book for test

        self.assertEqual(r.status_code, 201)
        responce_id = requests.get(self.book_url + str(self.book_id))
        self.assertEqual(responce_id.status_code, 200) #check that book present in list


    # update book by update_info information
    def test_update_book_pos(self):

        r = requests.put(self.book_url + str(self.book_id), data=self.update_info)
        self.assertEqual(r.status_code, 200)# check that book is updated(by status code)

        body_updated = r.json()
        self.update_info['id'] = self.book_id
        self.assertEqual(self.update_info, body_updated)# check that book is updated(by equal body)


    # update book by only title
    def test_update_title_pos(self):
        update_title = {"title": "Lullaby"}
        r = requests.put(self.book_url + str(self.book_id), data=update_title)
        self.assertEqual(r.status_code, 200)

        body_updated = r.json()

        self.assertEqual(update_title['title'], body_updated['title'])# check that book is updated(by equal body)
        self.assertEqual(self.test_book['author'],body_updated['author'])# check that book is updated(by equal body)

    #update book's id
    def test_update_id_neg(self):
        update_id = {"id":1}
        r = requests.put(self.book_url + str(self.book_id), data=update_id)
        self.assertEqual(r.status_code,200)

        body = r.json()
        self.assertNotEqual(self.book_id, update_id['id'])

    #update book by empty data
    def test_update_empty_neg(self):
        update_emp  = {"title":"","author":"" }
        r = requests.put(self.book_url + str(self.book_id), data=update_emp)
        self.assertEqual(r.status_code,400)



    def tearDown(self):
        r = requests.delete(self.book_url + str(self.book_id))
