# CS4501-EMS
4501 ISA Project
* Elliott Kim (ek4tx) - etkim97
* Marissa Lee (myl2vu) - Shardi3
* Sherry Li (xl2gs) - LiXiaoying

# Project 2

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


## Services
All fields need to be entered for CREATE, but not UPDATE

### Consumer
* /api/v1/consumers/1
* /api/v1/consumers/create
* /api/v1/consumers/1/update
* /api/v1/consumers/1/delete

### Producer
* /api/v1/producers/1
* /api/v1/producers/create
* /api/v1/producers/1/update
* /api/v1/producers/1/delete

### Review
* /api/v1/reviews/1
* /api/v1/reviews/create
* /api/v1/reviews/1/update
* /api/v1/reviews/1/delete

### ConsumerRequest
* /api/v1/consumerRequests/1
* /api/v1/consumerRequests/create
* /api/v1/consumerRequests/1/update
* /api/v1/consumerRequests/1/delete