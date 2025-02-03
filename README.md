# Receipt Processor

Build a webservice that fulfils the documented API. The API is described below. A formal definition is provided 
in the [api.yml](./api.yml) file. We will use the described API to test your solution.

Provide any instructions required to run your application.

Data does not need to persist when your application stops. It is sufficient to store information in memory. There are too many different database solutions, we will not be installing a database on our system when testing your application.

This is a FastAPI web service for processing receipts and awarding points according to a defined set of rules.

## API Endpoints

### Process Receipts

- **Endpoint:** `POST /receipts/process`
- **Description:** Accepts a JSON receipt, processes it, and returns a unique receipt ID.
- **Example Request Body:**
  ```json
  {
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}
```
- **Example Response: **
```json
{ "id": "7fb1377b-b223-49d9-a31a-5a02701dd310" }
```

### Get Points
- **Endpoint:**  GET /receipts/{id}/points
- **Description:** Returns the points awarded for the receipt with the specified ID.
- **Example Response:**
```json
{ "points": 109 }
```

- **Important:** The error message for invalid receipt input includes the phrase "Please verify input." to comply with the exercise requirements.

## Running the Application using Docker
### Prerequisites

Docker must be installed on your system.
Build the Docker Image
Run the following command in the project directory (where the Dockerfile is located):

```bash
docker build -t receipt-processor .
```
### Run the Docker Container
Run the container with:

```bash
docker run -d -p 8000:8000 receipt-processor
```

The service will be available at: http://localhost:8000

## API Documentation
When the application is running, you can view the automatically generated API docs at:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
## Additional Notes
Data is stored in memory and will be lost when the application stops.
The service validates incoming receipts. If a receipt is invalid, a 400 Bad Request is returned with an error message containing "Please verify input."