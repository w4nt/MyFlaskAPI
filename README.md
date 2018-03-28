# MyFlaskAPI
API meant to handle creating and logging in of users, and users being able to perform CRUD operations on businesses.

## API will have the following endpoints
Endpoint | Functionality
-------- | -------------
POST /api/v1/auth/register | Creates a user account
POST /api/v1/auth/login | Logs in a user
POST /api/v1/auth/logout | Logs out a user
POST /api/v1/auth/reset-password | Resets a user password
POST /api/v1/businesses/ | Register a business
PUT /api/v1/businesses/`<businessId>` | Update a business profile
DELETE /api/v1/businesses/`<businessId>` | Delete a business
GET /api/v1/businesses | Retrieves all businesses
GET /api/v1/businesses/`<businessId>` | Retrieves a business matching the specified business ID.
POST /api/v1/businesses/`<businessId>`/reviews | Add a review
GET /api/v1/businesses/`<businessId>`/reviews | Get all reviews for a business
