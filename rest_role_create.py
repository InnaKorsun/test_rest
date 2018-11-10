import unittest
import requests


class CreateRolesTests(unittest.TestCase):

    #list with book id which should be deleted in tearDown
    roles_ids = []

    @classmethod
    def setUp(self):

        response = requests.post("http://pulse-rest-testing.herokuapp.com/books", data={"title": "Fight club", "author": "Chack Pallanik"})
        assert (response.status_code==201)
        body = response.json()
        id_book = body["id"]
        self.role_url = "http://pulse-rest-testing.herokuapp.com/roles/"
        self.new_role = {"name": "Volan de Mort", "type": "Lord", "level":1, "book":id_book}
        self.list_role = [{"name": "Albus Dambldor", "type": "Wizzard", "level":1, "book":id_book},
                          {"name": "Gandalf", "type": "Maya", "level":1, "book":id_book}]

    #add one role
    def test_create_role_pos(self):
        response = requests.post(self.role_url, data=self.new_role)

        self.assertEqual(response.status_code, 201) # check status code
        body = response.json()

        self.new_role["id"] = body["id"] # add to json id role
        self.assertEqual(self.new_role, body)

        res = requests.get(self.role_url + str(body["id"]))#check that item present in role's list
        self.assertEqual(res.status_code, 200)
        self.roles_ids.append(body["id"])

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


    def test_create_roles_without_name_neg(self):

        role = {"type": "Lord", "level":1, "book":1} #try create role without name should create 400 status code
        response = requests.post(self.role_url, data=role)
        self.assertEqual(response.status_code, 400)


    def test_create_book_without_type_neg(self):

        role = {"name": "Volan de Mort", "level":1, "book":1} #try create role without typr should create 400 status code
        response = requests.post(self.role_url, data=role)
        self.assertEqual(response.status_code, 400)

    def test_create_role_with_id(self):#try create role with id should create 200 status code and create book with default id

        role = {"id":300,"name": "Gandalf", "type": "Maya", "level":1, "book":2}
        response = requests.post(self.role_url, data=role)
        self.assertEqual(response.status_code, 201)

        body = response.json()

        role["id"] = body["id"] # add to json id role
        self.assertEqual(role, body)

        res = requests.get(self.role_url + str(body["id"]))#check that item present in role's list
        self.assertEqual(res.status_code, 200)
        self.roles_ids.append(body["id"])#add id role to list which should be deleted in tearDown


    def test_create_empty_role_neg(self):#try create book with only title should create 400 status code

        role = {"name": "", "type": "", "level":None, "book":None}
        response = requests.post(self.role_url, data=role)
        self.assertEqual(response.status_code, 400)

        # create book with title with more than max length (max is 50)
        #each elements statrs with number og symbol in title

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


    def test_max_len_name(self):

        titles = []
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
    @classmethod
    def tearDown(self):
        for role_id in self.roles_ids:
            r = requests.delete(self.role_url + str(role_id))

if __name__ == "__main__":
    unittest.main(verbosity=2)
