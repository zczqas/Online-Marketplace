# Online Marketplace - Readme

## Overview

Welcome to Online Marketplace! This project is a simple and user-friendly platform where customers can sell their products and easily connect with each other. 
It's built using the Django framework, utilizes an SQLite database for data storage, and is styled with Tailwind CSS using a CDN.

## Features

- **Product Listing**: Users can easily create listings for their products, providing details such as product name, description, and price.
  
- **User Authentication**: Secure user authentication is implemented to ensure that only registered users can create listings and interact with others.

- **Messaging System**: Customers can contact each other through an integrated messaging system, fostering communication between buyers and sellers.

- **Responsive Design**: The user interface is designed to be responsive and accessible on various devices, offering a seamless experience.

- **SQLite Database**: The project uses SQLite as the database to store user information, product listings, and messaging data.

- **Tailwind CSS Styling**: The UI is styled using Tailwind CSS via CDN, providing a clean and modern look to enhance user experience.

## Setup Instructions

### Prerequisites

Make sure you have the following installed on your machine:

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [SQLite](https://www.sqlite.org/)

### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Infamous-Ironman/Projekt

2. **Navigate to the project directory:**

   ```bash
   cd myprojekt

3. **Apply database migrations:**

   ```bash
   python manage.py migrate

4. **Run the development server:**

   ```bash
   python manage.py runserver

Visit http://127.0.0.1:8000/ in your web browser to access the Online Marketplace.


