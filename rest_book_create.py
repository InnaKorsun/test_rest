import unittest
import requests
import requests


class CreateBookTests(unittest.TestCase):

    #list with book id which should be deleted in tearDown
    book_ids = []

    @classmethod
    def setUp(self):

        self.book_url = "http://pulse-rest-testing.herokuapp.com/books/"
        self.new_book = {"title": "Fight club", "author": "Chack Pallanik"}
        self.list_book = [{"title": "Djerelo", "author": "Ann Read"},
                          {"title": "Unittest tutorial", "author": "InnaK"}]
    #add one book
    def test_create_book_positive(self):
        response = requests.post(self.book_url, data=self.new_book)

        self.assertEqual(response.status_code, 201) # check status code
        body = response.json()

        self.new_book["id"] = body["id"] # add to json id book
        self.assertEqual(self.new_book, body)

        res = requests.get(self.book_url + str(body["id"]))#check that item present in book's list
        self.assertEqual(res.status_code, 200)
        self.book_ids.append(body["id"])

    # add list book
    def test_create_list_books_pos(self):
        for item in self.list_book:
            with self.subTest(item=item): #test with parameters (add one by one by from list_book)

                responce = requests.post(self.book_url, data=item)
                self.assertEqual(responce.status_code, 201) #check status code
                body = responce.json()

                self.book_ids.append(body["id"]) # add id book to list book which should be deleted
                item['id'] = body['id']# add id to just created book
                self.assertEqual(item, body)

                res = requests.get(self.book_url + str(body["id"]))#check that item present in book's list
                self.assertEqual(res.status_code, 200)

    def test_create_book_withou_author_neg(self):

        book = {"title": "Eat,pray,love"} #try create book with only title should create 400 status code
        response = requests.post(self.book_url, data=book)
        self.assertEqual(response.status_code, 400)

    def test_create_book_withou_title_neg(self):

        book = {"author": "InnaK"}#try create book with only author should create 400 status code
        response = requests.post(self.book_url, data=book)
        self.assertEqual(response.status_code, 400)

    def test_create_book_with_id(self):#try create book with id should create 200 status code and create book with default id

        book = {"id": 1,"title":"Lulluby","author":"Chak Pallanik" }
        response = requests.post(self.book_url, data=book)
        self.assertEqual(response.status_code, 201)

        body = response.json()

        book["id"] = body["id"] # add to json id book
        self.assertEqual(book, body)

        res = requests.get(self.book_url + str(body["id"]))#check that item present in book's list
        self.assertEqual(res.status_code, 200)
        self.book_ids.append(body["id"])#add id book to list which should be deleted in tearDown


    def test_create_empty_book_neg(self):#try create book with only title should create 400 status code

        book = {"title":"","author":"" }
        response = requests.post(self.book_url, data=book)
        self.assertEqual(response.status_code, 400)

    def test_create_title_max_len(self):
        # create book with title with more than max length (max is 50)
        #each elements statrs with number og symbol in title
        titles = ["51Maxlengthisfiftypointmxmxmxmxmxmxmxmxmxmxmxmxmxmmxm","50Maxlengthisfiftypointmxmxmxmxmxmxmxmxmxmxmxmxmxm",
                  "49Maxlengthisfiftypointmxmxmxmxmxmxmxmxmxmxmxmxmx"]

        for title in titles:
            with self.subTest(item=title):
                book = {"title": title, "author": "InnaK"}
                if title.startswith("49") or title.startswith("50"):# check if title contain 49 or 50 symbol  - book should created
                    response = requests.post(self.book_url, data=book)
                    self.assertEqual(response.status_code, 201)
                    body = response.json()
                    res = requests.get(self.book_url + str(body["id"]))#check that item present in book's list
                    self.assertEqual(res.status_code, 200)
                    self.book_ids.append(body["id"])
                else:
                    response = requests.post(self.book_url, data=book)# check if title contain 51 symbol s - book shouldn't created
                    self.assertEqual(response.status_code,400)

    @classmethod
    def tearDown(self):
        for book_id in self.book_ids:
            r = requests.delete(self.book_url + str(book_id))

if __name__ == "__main__":
    unittest.main(verbosity=2)
