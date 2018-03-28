import bcrypt
"""This contains the WeConnect, User, and Business classes.
The WeConnect class acts as the main class, handling
the interactions of the user with the application by
utilizing the other classes defined here."""


class WeConnect():
    """Overall application class.
    Manages the other classes"""

    def __init__(self):
        """
        - userdb: User database.
        - business: Businesses' database"""

        self.userdb = []

        self.business = []

    def register_user(self, user_id, first_name, last_name, email, password):
        """Adds a user to the application
        - user_id: uniquely identifies the user record
        - first_name: Holds the user's first name
        - last_name: Holds the user's last name
        - password: Holds the user's password
        - user_record: a dictionary storing the user details
        in the following format:
        {
            'id': randint,
            'first_name': 'string',
            'last_name': 'string',
            'email': 'string',
            'password': 'hashed password converted to string format'
        }
        Is stored in the self.userdb list
        - self.userdb: a list of dictionaries, each symbolized by user_record"""
        for user_record in self.userdb:
            # check if the email submitted is already in the dictionary
            # and there is an id in the dictionary. If so do not proceed
            if user_record['email'] == email and user_record['id'] is not None:
                return "You're already registered. Try signing in."

        if email is not None and password is not None:
            # make instance of User class with required parameters
            user = User(user_id, first_name, last_name, email, password)
            # Hash the user password
            user_password = user.set_password(password)
            # create dictionary record of user details
            new_user = {
                'id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'password': user_password
            }
            # add dictionary to self.userdb list
            self.userdb.append(new_user)
            return True

    def login_user(self, email, password):
        """Logs in users to the application.
        - email: Holds the user's entered e-mail address.
        - password: Holds the user's entered password
        - user_record: a dictionary storing the user details
        in the following format:
        {
            'id': randint,
            'first_name': 'string',
            'last_name': 'string',
            'email': 'string',
            'password': 'hashed password converted to string format'
        }
        Is stored in the self.userdb list
        - self.userdb: a list of dictionaries, each symbolized by user_record"""
        for user_record in self.userdb:
            # assign dictionary values for ease of reference
            user_id = user_record['id']
            user_password = user_record['password']
            user_email = user_record['email']
            first_name = user_record['first_name']
            last_name = user_record['last_name']
            # make instance of User class with required parameters
            user = User(user_id, first_name, last_name, user_email, user_password)
            # check that there is an id value in the dictionary
            if user.user_id:
                # check that the email in the dictionary is the same as that entered
                # by the user
                if user.check_email(email):
                    # check that the password in the dictionary is the same as that entered
                    # by the user
                    if user.check_password(password, user_password):
                        return user_id

    def reset_password(self, email, password, new_password):
        """Changes the user's password
        - email: Holds the user's entered e-mail address.
        - password: Holds the user's entered password.
        - user_record: a dictionary storing the user details
        in the following format:
        {
            'id': randint,
            'first_name': 'string',
            'last_name': 'string',
            'email': 'string',
            'password': 'hashed password converted to string format'
        }
        Is stored in the self.userdb list
        - self.userdb: a list of dictionaries, each symbolized by user_record"""
        for user_record in self.userdb:
            # assign dictionary values for ease of reference
            user_password = user_record['password']
            user_email = user_record['email']
            user_id = user_record['id']
            first_name = user_record['first_name']
            last_name = user_record['last_name']
            # make instance of User class with required parameters
            user = User(user_id, first_name, last_name, user_email, user_password)
            # check that there is an id for the user
            if user_id:
                # check that the email passed to reset_password is the same as that
                # in the dictionary
                if user.check_email(email):
                    # check that the password passed to reset_password
                    # is the same as that in the dictionary
                    if user.check_password(password, user_password):
                        # call the change_password method from the User class to switch the the string password
                        # passed to reset_password with that stored in new_password
                        password = user.change_password(new_password)
                        # update the value of the password in the dictionary
                        user_password = user.set_password(password)
                        user_record['password'] = user_password
                        # check if the password matches the hashed password
                        # in the dictionary
                        if user.check_password(password, user_record['password']):
                            return True
                        return False

    def create_business(self, user_id, business_id, name, location, category, description):
        """Creates a business for the user
        - user_id: ID of the user creating the business.
        - business_id: ID of the created business.
        - name: Name of the business.
        - location: Holds where the business is located.
        - category: Holds the category which the business falls under.
        - description: Holds the description of the business.
        - reviews: Holds reviews associated with the business.
        - user_business: Dictionary holding details of a given business as follows:
        {
            'user_id': integer,
            'business_id': integer,
            'name': 'string',
            'location': 'string',
            'description': 'string',
            'category': 'string'
        }
        Is stored in the self.business list
        - self.business: Holds a list of businesses, each in dictionary format."""
        # make sure that no empty fields are entered as part of the business details
        if name is None or location is None or category is None or description is None:
            return "Missing Field: Please provide Name & Description."

        # make an instance of the business class
        business = Business(business_id, name, location, description, category)
        # create the user's business
        user_business = {
            'user_id': user_id,
            'business_id': business.business_id,
            'name': business.name,
            'location': business.location,
            'description': business.description,
            'category': business.category,
            'reviews': []
        }
        #add the created business as a list entry in self.business
        self.business.append(user_business)
        return user_business

    def get_businesses(self):
        """Gets all businesses on the application
        for a logged-in user"""
        all_businesses = []
        for item in self.business:
            item1 = item.copy()
            item1.pop('reviews', None)
            all_businesses.append(item1)
        return all_businesses

    def update_business(self, user_id, business_id, name=None, location=None, description=None, category=None):
        """Updates an existing business with details provided by the user.
        - user_id: ID of the user creating the business.
        - business_id: ID of the created business.
        - name: Name of the business.
        - location: Holds where the business is located.
        - category: Holds the category which the business falls under.
        - description: Holds the description of the business.
        - reviews: Holds reviews associated with the business.
        - user_business: Dictionary holding details of a given business as follows:
        {
            'user_id': integer,
            'business_id': integer,
            'name': 'string',
            'location': 'string',
            'description': 'string',
            'category': 'string'
        }
        Is stored in the self.business list
        - self.business: Holds a list of businesses, each in dictionary format."""
        # iterate through list of businesses
        for my_business in self.business:
            # check that the user ID given is associated with the business
            if user_id == my_business['user_id']:
                # check that the business ID given is associated with the business
                if business_id == my_business['business_id']:
                    # make instance of the Business class with the parameters passed
                    business = Business(business_id, name, location, description, category)
                    # if we have a value for 'name', change the business name
                    if name is not None:
                        new_name = business.change_name(name)
                        my_business['name'] = new_name
                    # if we have a value for 'location', change the business location
                    if location is not None:
                        new_location = business.change_location(location)
                        my_business['location'] = new_location
                    # if we have a value for 'description', change the business description
                    if description is not None:
                        new_description = business.change_description(description)
                        my_business['description'] = new_description
                    # if we have a value for 'category', change the business category
                    if category is not None:
                        new_category = business.change_category(category)
                        my_business['category'] = new_category
                    # return the updated business
                    return my_business
        return False

    def get_business(self, business_id):
        all_businesses = []
        for item in self.business:
            item1 = item.copy()
            item1.pop('reviews', None)
            all_businesses.append(item1)

            for business in all_businesses:
                for key in business.keys():
                    if key == 'id' and business[key] == business_id:
                        return business

    def delete_business(self, business_id):
        """Deletes a business created by the user."""
        if business_id is not None:
            for my_business in self.business:
                if my_business['id'] == business_id:
                    self.business.remove(my_business)
                    return True

    def add_review(self, business_id, review_id, user_review):
        """Adds a review by a user"""
        if business_id is not None:
            for business in self.business:
                for key, value in business.items():
                    if key == 'id' and value == business_id:
                        review = Review(review_id, user_review)
                        new_review = {
                            'id': review.review_id,
                            'review': review.review
                        }
                        business['reviews'].append(new_review)
                        return business

    def get_reviews(self, business_id):
        """Gets all reviews for a single business and
        shows them to a logged-in user."""
        if business_id is not None:
            for business in self.business:
                for business_id in business:
                    return business['reviews']


class User():
    """Basic blueprint of the User class.
    Provides the foundation for how the user interacts
    with the application."""

    def __init__(self, user_id, first_name, last_name, email, password):
        """Required parameters for the User class
        - user_id: Holds the user id
        - first_name: Holds the user's first name
        - last_name: Holds the user's last name
        - password: Holds the user's password"""
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def set_password(self, password):
        """Sets the user's password. Handles password hashing
        as well.
        - password: Holds the user's password"""
        salt = bcrypt.gensalt(16)
        password = self.password
        hashed_password = bcrypt.hashpw(password.encode('utf8'), salt)
        return hashed_password.decode('utf8')

    def check_password(self, password, hashed_password):
        """Checks that the password entered is the same
        as the hashed password we have
        - password: Holds the entered password
        - hashed_password: Holds the (stored) hashed password."""
        return bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8'))

    def check_email(self, email):
        """Checks that the email entered is the same
        as the email we have
        - email: Holds the entered password
        - user_email: Holds the (stored) email."""
        if email == self.email:
            return True
        return False

    def change_password(self, fresh_password):
        """Changes the password of the user.
        - password: Holds the (old entered) password
        of the user
        - fresh_password: Holds the (new entered) password
        of the user"""
        if self.password != fresh_password:
            self.password = fresh_password
            return self.password
        return False

class Business():
    """Basic blueprint of the Business class.
    Provides the foundation for how the businesses will
    be modeled in with the application."""

    def __init__(self, business_id, name, location, description, category):
        self.business_id = business_id
        self.name = name
        self.location = location
        self.description = description
        self.category = category

    def change_name(self, new_name):
        """Changes business name."""
        self.name = new_name
        return new_name

    def change_description(self, new_description):
        """Changes business description"""
        self.description = new_description
        return new_description

    def change_location(self, new_location):
        """Changes business name."""
        self.name = new_location
        return new_location

    def change_category(self, new_category):
        """Changes business description"""
        self.category = new_category
        return new_category


class Review():
    def __init__(self, review_id, review):
        self.review = review
        self.review_id = review_id


