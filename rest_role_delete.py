import unittest
import requests

class DeleteRoleTests(unittest.TestCase):

    def setUp(self):

        response = requests.post("http://pulse-rest-testing.herokuapp.com/books",
                                 data={"title": "Fight club", "author": "Chack Pallanik"})
        assert(response.status_code==201)
        body = response.json()
        self.id_book = body["id"]

        self.role_url = "http://pulse-rest-testing.herokuapp.com/roles/"

        self.new_role = {"name": "Volan de Mort", "type": "Lord", "level":1, "book":self.id_book}
        r = requests.post(self.role_url,data = self.new_role)
        assert (r.status_code,201)
        self.id_role = r.json()['id']


    def test_delete_role_pos(self):

        r = requests.delete(self.role_url + str(self.id_role))
        self.assertEqual(r.status_code,204)#check that book deleted(by status code)

        responce_get = requests.get(self.role_url + str(self.id_role))
        self.assertEqual(responce_get.status_code, 404) #check that book doen't present in list

    def test_delete_role_notExistId_neg(self):

        r = requests.delete(self.role_url + str(self.id_role-10000))# try delete book with d which doesn;t exist
        self.assertEqual(r.status_code,404)#check that book deleted(by status code)


    def tearDown(self):
        r = requests.delete("http://pulse-rest-testing.herokuapp.com/books/" + str(self.id_book))
