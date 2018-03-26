# CS4501-EMS
4501 ISA Project
* Elliott Kim (ek4tx) - etkim97
* Marissa Lee (myl2vu) - Shardi3
* Sherry Li (xl2gs) - LiXiaoying

# Project 4

## Models

### Consumer
* username
* password
* first_name
* last_name
* phone
* email

### Producer
* username
* password
* first_name
* last_name
* phone
* email
* bio
* skills

### Review
* rating (int)
* comment
* author (foreign key of Consumer)
* producer (foreign key)

### Consumer Request
* title
* offered_price (float)
* description
* timestamp
* availability
* consumer (foreign key)
* accepted_producer (foreign key)

### Authenticator
* user_id (int)
* is_consumer (boolean)
* authenticator (primary key)
* date_created


## Microservices

All fields need to be entered for CREATE, but not UPDATE

### Consumer
* 8001/api/v1/consumers/1
* 8001/api/v1/consumers/create, post_data={username, password, first_name, last_name, email, phone}
* 8001/api/v1/consumers/1/update, post_data={username, password, first_name, last_name, email, phone}
* 8001/api/v1/consumers/1/delete

### Producer
* 8001/api/v1/producers/1
* 8001/api/v1/producers/create, post_data={username, password, first_name, last_name, email, phone, bio, skills}
* 8001/api/v1/producers/1/update, post_data={username, password, first_name, last_name, email, phone, bio, skills}
* 8001/api/v1/producers/1/delete

### Review
* 8001/api/v1/reviews/1
* 8001/api/v1/reviews/create, post_data={rating, comment, author, producer}
* 8001/api/v1/reviews/1/update, post_data={rating, comment, author, producer}
* 8001/api/v1/reviews/1/delete

### ConsumerRequest
* 8001/api/v1/consumerRequests/1
* 8001/api/v1/consumerRequests/create, post_data={title, description, offered_price, availability, consumer, accepted_producer (null)}
* 8001/api/v1/consumerRequests/1/update, post_data={title, description, offered_price, availability, consumer, accepted_producer (null)}
* 8001/api/v1/consumerRequests/1/delete
* 8001/api/v1/consumerRequests/getNewest
* 8001/api/v1/consumerRequests/getHighestPrice

### Authenticator
* 8001/api/v1/authenticators/create, post_data={user_id, is_consumer}
* 8001/api/v1/authenticators/delete, post_data={authenticator}
* 8001/api/v1/authenticators/validate, post_data={authenticator}

### Login
* 8001/api/v1/login, post_data={username, password, user_id}

## Services

* 8002/api/v1/login
* 8002/api/v1/logout
* 8002/api/v1/getNewestRequestPk
* 8002/api/v1/getHighestRequestPk
* 8002/api/v1/requestDetail/1
* 8002/api/v1/consumerDetail/1
* 8002/api/v1/producerDetail/1
* 8002/api/v1/createListing, post_data={consumer, authenticator, title, description, offered_price, availability}
* 8002/api/v1/createConsumer, post_data={username, password, first_name, last_name, email, phone}
* 8002/api/v1/createProducer, post_data={username, password, first_name, last_name, email, phone, bio, skills}

## Web

* 8000/
* 8000/login
* 8000/logout
* 8000/request_detail/1
* 8000/consumer_detail/1
* 8000/producer_detail/1
* 8000/create_listing
* 8000/create_consumer
* 8000/create_producer