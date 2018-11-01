import unittest
import requests

class CreateRolesTestsPositive(unittest.TestCase):

    #list with book id which should be deleted in tearDown
    roles_ids = []

    @classmethod
    def setUp(self):

        response = requests.post("http://pulse-rest-testing.herokuapp.com/books",
                                 data={"title": "Fight club", "author": "Chack Pallanik"})
        assert(response.status_code==201)
        body = response.json()
        self.id_book = body["id"]

        self.role_url = "http://pulse-rest-testing.herokuapp.com/roles/"
        self.new_role = {"name": "Volan de Mort", "type": "Lord", "level":1, "book":self.id_book}
        self.list_role = [{"name": "Albus Dambldor", "type": "Wizzard", "level":1, "book":self.id_book},
                          {"name": "Gandalf", "type": "Maya", "level":1, "book":self.id_book},
                          {"id":300,"name": "Gandalf", "type": "Maya", "level":1, "book":self.id_book}]


    # add list roles
    def test_create_list_roles_pos(self):
        for item in self.list_role:
            with self.subTest(item=item): #test with parameters (add one by one by from list_roles)

                responce = requests.post(self.role_url, data=item)
                self.assertEqual(responce.status_code, 201) #check status code
                body = responce.json()

                self.roles_ids.append(body["id"]) # add id role to list roles which should be deleted
                item['id'] = body['id']# add id to just created role
                self.assertEqual(item, body)

                res = requests.get(self.role_url + str(body["id"]))#check that item present in roles's list
                self.assertEqual(res.status_code, 200)

    def test_create_role_with_only_req_field(self):
        #try create role with only required field(name and type)

        role = {"name": "Gandalf", "type": "Maya"}
        response = requests.post(self.role_url, data=role)
        self.assertEqual(response.status_code, 201)

        body = response.json()

        self.assertEqual(role["name"], body["name"])
        self.assertEqual(role["type"], body["type"])

        res = requests.get(self.role_url + str(body["id"]))#check that item present in role's list
        self.assertEqual(res.status_code, 200)
        self.roles_ids.append(body["id"])#add id role to list which should be deleted in tearDown

    @classmethod
    def tearDown(self):
        for role_id in self.roles_ids:
            r = requests.delete(self.role_url + str(role_id))
        r = requests.delete("http://pulse-rest-testing.herokuapp.com/books/"+ str(self.id_book))


class CreateRolesTestsNegative(unittest.TestCase):

    roles_ids = []
    @classmethod
    def setUp(self):

        response = requests.post("http://pulse-rest-testing.herokuapp.com/books",
                                 data={"title": "Fight club", "author": "Chack Pallanik"})
        assert(response.status_code==201)
        body = response.json()
        self.id_book = body["id"]
        self.role_url = "http://pulse-rest-testing.herokuapp.com/roles/"
        self.list_role = [{"type": "Lord", "level":1, "book":self.id_book},
                          {"name": "Volan de Mort", "level":1, "book":self.id_book},
                          {"name": "", "type": "", "level":None, "book":None},
                          {"name": "Volan de Mort", "type":"Lord","level":1, "book":self.id_book-1000000},
                          {"name": "Volan de Mort", "type":"Lord","level":1, "book":"l"}]

    def test_create_list_roles_neg(self):
        for item in self.list_role:
            with self.subTest(item=item): #test with parameters (add one by one by from list_role)

                responce = requests.post(self.role_url, data=item)
                self.assertEqual(responce.status_code, 400) #check status code


    def test_max_len_name(self):
    #max len of name field is 200

        titles=[] # create name string with len 199 200 and 201 symbols
        #the first is i = "199sssss...." (len is 199)

        for i in range(199,202,1):
            s=str(i) + "s"*(i-3)
            titles.append(s)

        for title in titles:
            with self.subTest(item=title):
                role = {"name": title, "type": "InnaK"}
                if title.startswith("199") or title.startswith("200"):# check if title contain 49 or 50 symbol  - book should created
                    response = requests.post(self.role_url, data=role)
                    self.assertEqual(response.status_code, 201)
                    body = response.json()
                    res = requests.get(self.role_url + str(body["id"]))#check that item present in book's list
                    self.assertEqual(res.status_code, 200)
                    self.roles_ids.append(body["id"])
                else:
                    response = requests.post(self.role_url, data=role)# check if title contain 51 symbol s - book shouldn't created
                    self.assertEqual(response.status_code,400)

    def test_max_level_value(self):
    #max len of name field is 200

        level=[] # create test data with value low and high boundary

        for i in range(-2147483647,-2147483650,-1): #нижняя граница
            level.append(i)
        for i in range(2147483646,2147483649):#верхняя граница
            level.append(i)

        for title in level:
            with self.subTest(item=title):
                role = {"name": "test_level", "type": "InnaK", "level":title}
                if (str(title).startswith("-") and str(title).endswith("49")) or \
                        (str(title).startswith("2") and str(title).endswith("48")):
                    response = requests.post(self.role_url, data=role)
                    self.assertEqual(response.status_code,400)

                else:
                    response = requests.post(self.role_url, data=role)
                    self.assertEqual(response.status_code, 201)
                    body = response.json()
                    res = requests.get(self.role_url + str(body["id"]))#check that item present in roles's list
                    self.assertEqual(res.status_code, 200)
                    self.roles_ids.append(body["id"])


    @classmethod
    def tearDown(self):
        for role_id in self.roles_ids:
            r = requests.delete(self.role_url + str(role_id))
        r = requests.delete("http://pulse-rest-testing.herokuapp.com/books/"+ str(self.id_book))

if __name__ == "__main__":
    unittest.main(verbosity=2)
