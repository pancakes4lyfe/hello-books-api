def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

#I client refers to the function on conftest.py, which refers to app, but what does app refer to?
def test_get_one_book(client, two_saved_books):
    #Act
    response = client.get("/books/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

def test_get_one_non_existing_book(client):
    #Act
    response = client.get("/books/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 404

def test_get_all_books_with_existing_data(client, two_saved_books):
    #Act
    response = client.get("/books")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == [{
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
        }, 
        {
        "id": 2,
        "title": "Mountain Book",
        "description": "i luv rocks"
        }]
# def test_create_new_book(client):
#     #Act
#     response = client.post("/books", json=)
#     response_body = response.get_json()
    
#     #Assert
#     assert response.status_code == 201
#     assert response_body == {
#         "success": True,
#         "message": f"Book {new_book.title} has been created"
#         }