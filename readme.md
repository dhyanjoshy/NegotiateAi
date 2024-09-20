# Negotiation System API

This API facilitates negotiation conversations between users and the system using AI technology. It leverages LLaMA 3.1 for generating dynamic responses and uses sentiment analysis to evaluate user input and adjust offers accordingly.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [Negotiation Endpoint](#1-negotiation-endpoint)
- [How It Works](#how-it-works)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

The Negotiation System API allows users to interact with an AI agent to negotiate the purchase of an item. The API is built with Flask and integrates LLaMA 3.1 for generating responses based on the context of the conversation. Sentiment analysis is used to understand the user's emotional state and adjust the offer accordingly.

## Features

- **Dynamic Negotiation:** Responds to user messages and negotiates based on predefined rules.
- **Sentiment Analysis:** Analyzes user input to adjust offers intelligently.
- **Context Management:** Maintains conversation history for each session.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/dhyanjoshy/NegotiateAi.git
    ```

2. **Create an environment:**

    ```bash
    py -m venv env
    env\Scripts\activate
    ```

3. **Install the Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application:**

    ```bash
    python app.py
    ```

    The API will be available at `http://localhost:5000/api/v1/`.

## Usage

To interact with the API, you can use tools like `curl` or `Postman`. Make sure to send JSON data in your POST requests.

### Example Request

```bash
curl -X POST http://localhost:5000/negotiate \
    -H "Content-Type: application/json" \
    -d '{
          "user_id": "user123",
          "offer": 150.0,
          "message": "I would like to negotiate the price.",
          "maximum": 200.0,
          "minimum": 100.0
        }'
```


## API Endpoints

### 1. Negotiation Endpoint

- **URL:** `/negotiate`
- **Method:** `POST`
- **Description:** Engages in a negotiation conversation with the user.

#### Request Body

```json
{
  "user_id": "user123",
  "offer": 150.0,
  "message": "I would like to negotiate the price.",
  "maximum": 200.0,
  "minimum": 100.0
}
```

#### Response

```json
{
  "llama_response": "We can offer you a final price of $130.",
  "context": "User: I would like to negotiate the price.\nAI: We can offer you a final price of $130.\n",
  "score": 0.9,
  "offer_by_us": 130.0
}
```

## How It Works

1. **User Input:** The API receives user input through the `/negotiate` endpoint.
2. **Sentiment Analysis:** The input is analyzed to determine the user's sentiment score.
3. **Offer Calculation:** Based on the sentiment score, the API calculates an appropriate counter-offer.
4. **Response Generation:** The LLaMA 3.1 model generates a response using the updated context and offer information.
5. **Context Update:** The conversation history is maintained for consistent interactions.

## Technologies Used

- **Flask:** Web framework for building the API.
- **LLaMA 3.1:** Language model for generating responses.
- **Hugging Face Transformers:** For sentiment analysis.
- **Python:** Programming language.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.


## Contact

**Author:** Dhyan Joshy  
**Email:** [dhyanjoshy007@gmail.com](mailto:dhyanjoshy007@gmail.com)
