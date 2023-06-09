# Network
## Description
This project successfully implemented the specified functionality of a social network web application using Python, Django, JavaScript, HTML, and CSS. While the primary focus was on functionality, some design elements were incorporated using Bootstrap and custom CSS styles. The application allows users to create posts, follow other users, and like posts, providing a comprehensive social networking experience. Future improvements could include further enhancing the frontend design to enhance user experience and visual appeal

## How To Use App

To use this code, you also need to have the following installed on your machine:

1. Python
2. Django

## Technical Specifications

### Backend Development:

The backend development was done using Python 3 and the Django web framework.
Django's powerful features were leveraged to implement user authentication, post creation, following functionality, and handling likes.
The Django models were utilized to define the database structure and interact with the database, ensuring efficient storage and retrieval of user data, posts, likes, and followers.

### Frontend Development:

HTML and Jinja templating engine were used to structure the web pages and dynamically display data from the backend.
CSS styles were applied to enhance the visual presentation of the application.
Bootstrap 5 framework was used to provide responsive and mobile-friendly design elements.

## Functionality Implemented:

1. New Post:
Users can create new text-based posts by entering content in a text area and submitting the post.
2. All Posts:
The "All Posts" page displays all posts from all users, with the most recent posts shown first.
Each post includes the username of the poster, the post content, the date and time of the post, and the number of likes.
3. Profile Page:
Clicking on a username loads that user's profile page.
The profile page shows the number of followers and the number of people the user follows.
All posts made by the user are displayed in reverse chronological order.
For other signed-in users, a "Follow" or "Unfollow" button is provided to toggle following status.
4. Following:
The "Following" page displays posts from users that the current user follows.
Similar to the "All Posts" page, posts are shown with the most recent posts first.
5. Pagination:
Posts are displayed in sets of 10 per page.
Navigation buttons ("Next" and "Previous") enable users to navigate between pages of posts.
6. Edit Post:
Users can edit their own posts by clicking an "Edit" button or link.
The post's content is replaced with a textarea for editing.
Users can save the edited post without needing to reload the entire page.
Appropriate security measures are in place to prevent unauthorized editing of other users' posts.
7. Like and Unlike:
Users can like or unlike a post by clicking a button or link.
The like count is asynchronously updated on the server using JavaScript and Fetch API, without requiring a full page reload.

## Contact

Any information, bugs or questions can be sent on the e-mail adress: adzamija@icloud.com
