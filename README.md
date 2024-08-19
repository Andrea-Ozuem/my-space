# My Space - A Productivity & Music Recommendation App

A customized productivity app designed to help users manage their tasks efficiently while enjoying personalized music recommendations. The app features a user-friendly interface built with HTML, CSS, and JavaScript, interacting with a backend via APIs.

## Features

- **Simple User Authentication**: Using JWT tokens.
- **Task Management**: Add, edit, and delete tasks to stay organized.
- **Music Recommendations**: Receive personalized music suggestions based on your preferences via Spotify API.
- **Real-Time Updates**: The app interacts with the backend to fetch and display real-time data.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend Interaction**: RESTful APIs

## Getting Started

To get started with the app, simply clone the repository and open the `index.html` file in your browser.

```bash
git clone https://github.com/yourusername/productivity-music-app.git
cd productivity-music-app
```

### Running the App

1. **Open the App**: Locate the `index.html` file in the project directory and open it in your preferred web browser. No additional setup is required.
2. **Interact with Features**: 
   - **Add Tasks**: Use the task input field to create new tasks and manage them.
   - **Get Music Recommendations**: click `Get Flow` to get top tracks via Spotify client.

### API Integration

The frontend communicates with a backend server via RESTful APIs to handle task management and provide music recommendations.

#### Example API Endpoints

- **Task Management**:
  - `GET /api/v1/tasks`: Retrieve a list of all tasks.
  - `POST /api/v1/tasks`: Add a new task by sending a JSON payload.
  - `PUT /api/v1/tasks/:id`: Update an existing task by sending a JSON payload with the task ID.
  - `DELETE /api/v1/tasks/:id`: Remove a task using its ID.

- **Music Recommendations**:
  - `GET /v1/me/top/tracks`: Fetch a recommended track based on user preferences.

#### API Response Example

**Fetching Tasks:**

```json
[
  {
    "id": "001-234",
    "description": "Finish the project",
    "completed": false
  },
  {
    "id": "002-234",
    "title": "Go for a walk",
    "completed": true
  }
]
```

## Screenshots

<img width="1440" alt="Screenshot 2024-08-19 at 13 22 11" src="https://github.com/user-attachments/assets/ae9a4516-f276-442e-8841-119220e5a69b">


## Roadmap

The following features and enhancements are planned for future releases:

- **Get Recommendation for Deadlines**
  - Using Spotify API get recommended tasks based on user inputed seed values

- **Implement Delete & Edit task**
    - Implement delete & edit task button and functionality on the frontend.
 
- **Light Mode**
  - Add a light mode option to improve usability in low-light environments and provide a better user experience.

- **Notifications**
  - Implement push notifications and alerts to remind users of upcoming tasks and deadlines.

## Authors

- **Andrea Ozuem** - *Initial work and ongoing development*  
  - [LinkedIn]((https://www.linkedin.com/in/andrea-ozuem/))
  - [Email](mailto:andreaozuem2021@gmail.com)
