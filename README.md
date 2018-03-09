# CS4501-EMS
4501 ISA Project
* Elliott Kim (ek4tx) - etkim97
* Marissa Lee (myl2vu) - Shardi3
* Sherry Li (xl2gs) - LiXiaoying

# Project 3

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


## Microservices

All fields need to be entered for CREATE, but not UPDATE

### Consumer
* 8001/api/v1/consumers/1
* 8001/api/v1/consumers/create
* 8001/api/v1/consumers/1/update
* 8001/api/v1/consumers/1/delete

### Producer
* 8001/api/v1/producers/1
* 8001/api/v1/producers/create
* 8001/api/v1/producers/1/update
* 8001/api/v1/producers/1/delete

### Review
* 8001/api/v1/reviews/1
* 8001/api/v1/reviews/create
* 8001/api/v1/reviews/1/update
* 8001/api/v1/reviews/1/delete

### ConsumerRequest
* 8001/api/v1/consumerRequests/1
* 8001/api/v1/consumerRequests/create
* 8001/api/v1/consumerRequests/1/update
* 8001/api/v1/consumerRequests/1/delete
* 8001/api/v1/consumerRequests/getNewest
* 8001/api/v1/consumerRequests/getHighestPrice


## Services

* 8002/api/v1/getNewestRequestPk
* 8002/api/v1/getHighestRequestPk
* 8002/api/v1/requestDetail/1


## Web

* 8000/
* 8000/request_detail/1