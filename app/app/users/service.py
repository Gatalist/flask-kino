from app import db
from .models import User
# from .validation import CreateUserSchema, LoginUserSchema
from .auth import generate_jwt_token, token_required, error_response



def create_user(input_data):
    # create_validation_schema = CreateUserSchema()
    
    # errors = create_validation_schema.validate(input_data)
    # if errors:
    #     return {'username': 'len be 4', 'pass': 'len be 6'}
    
    check_username_exist = User.query.filter_by(username=input_data.get("username")).first()
    if check_username_exist:
        return {'error':'Username already exist'}
    
    check_email_exist = User.query.filter_by(email=input_data.get("email")).first()
    if check_email_exist:
        return {'error':'Email already taken'}

    new_user = User(
        username = input_data['username'],
        email = input_data['email'])
    new_user.set_password(input_data['password'])
    db.session.add(new_user)  # Adds new User record to database
    db.session.commit()  # Comment
   
    # return {"ok":"User Created"}
    return new_user


def login_user(input_data):
    get_user = User.query.filter_by(email=input_data.get("email")).first()
    if get_user is None:
        return {"error":"User not found"}
    print('user', get_user.username)
    if get_user.check_password(input_data.get("password")):
        token = generate_jwt_token(get_user)
        return {'x-access-tokens': token}
    
    else:
        return {"error":"Password is wrong"}



class ApiDocumentation:
    def documentation(self, method, url, desc, url_full, data=''):
        sample = """
            Пример использования:
            {} - {}


            fetch('{}', {{
                method: '{}',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                {}
            }})
        """.format(url, desc, url_full, method, data)
        return sample