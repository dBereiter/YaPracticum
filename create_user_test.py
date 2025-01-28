import sender_stand_request
import data

def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body

def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1

def negative_assert_simbol(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"

def negative_assert(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

def test_1_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")
def test_2_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")
def test_3_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_simbol("А")
def test_4_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_simbol("Аааааааааааааааа")
def test_5_create_user_eng_letter_in_first_name_get_success_response():
    positive_assert("QWErty")
def test_6_create_user_rus_letter_in_first_name_get_success_response():
    positive_assert("Мария")
def test_7_create_user_has_space_in_first_name_get_error_response():  #Failed is Good, in Pytest Query
    negative_assert_simbol("Человек и Ко")
def test_8_create_user_special_simbols_in_first_name_get_error_response():
    negative_assert_simbol("№%@")
def test_9_create_user_digits_in_first_name_get_error_response():
    negative_assert_simbol("123")
def test_10_create_user_no_first_name_get_error_response():
    user_body = get_user_body("firstName")
    user_body.pop("firstName")
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

def test_11_create_user_empty_first_name_get_error_response():
    negative_assert("")
def test_12_create_user_wrong_datatype_in_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400