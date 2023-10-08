# Lifelong Learning Diary

The Lifelong Learning Diary web application is a versatile and user-centric tool designed to support the continuous learning journey of both university students and lifelong learners. Instead of viewing learning as a series of projects, our application recognizes it as a lifelong endeavor, providing users with a single, personal, and private learning diary entity.

## Status 8-Oct-2023

- **Current Features:** The following key features are currently implemented and functional:
  - Privacy by Default: users can access only their own entries
  - User Account: users can create an account, log in and out ; login is mandatory to view entries
  - Course and Project Integration: users can categorize their entries to different learning journeys

- **Upcoming Features:** The following key features are in development:
  - User Account: users can delete their accounts permanently
  - Custom Tagging: a 'tags' table will be added and utilized to allow users to categorize entries on a lower level
  - Breakthrough Moments: users can add a special 'Breakthrough' tag to note extra-special, personal insight
  - User-Specific Dashboard: after logging in, the user will get an outlook of their latest activity

- **Other upcoming changes:** In additionally, the following tasks have been planned:
  - Code commenting and cleanup (including translating error messages FIN>ENG, renaming variables)
  - Major UI improvements

- **Local Testing:** You can test the application locally by following these steps:
  1. Clone the repository: `git clone https://github.com/yogajones/learning-diary.git`
  2. Navigate to the local copy with `cd learning-diary`
  3. Create a .env file that contains: DATABASE_URL for the address of your database and SECRET_KEY for your secret key. Check instructions at: `https://hy-tsoha.github.io/materiaali/osa-2/`
  4. Start the PostgreSQL server. Check instructions at: `https://hy-tsoha.github.io/materiaali/osa-2/`
  5. To create the database, run `psql < schema.sql`
  6. Create and run the virtual environment: `python3 -m venv venv` and `source venv/bin/activate`
  7. Install the required packages: `pip install -r requirements.txt`
  8. Run the application: `flask run`
  9. Access the app in your web browser by holding Ctrl and clicking the link on your terminal

  This application is still in development. To protect your privacy, please do not input any sensitive information even when testing locally.

## Key Features

- **Unified Learning Diary:** Embrace lifelong learning with a single, comprehensive learning diary for all your educational experiences, whether you're a university student or a lifelong learner exploring diverse fields.
- **Course and Project Integration:** Attach specific courses, workshops, or other learning journeys (e.g., "Web Applications 101" at university or "Cyber Security Nordic 2023" in your professional life) to your journal entries for contextual reference.
- **Custom Tagging:** Personalize your entries with custom tags to categorize and organize your learning journey effectively.
- **Privacy by Default:** Your journal entries are automatically set to private, ensuring the utmost confidentiality of your personal and learning-related reflections.
- **User Accounts:** Access to the learning diary requires user registration, guaranteeing a secure and personalized experience.
- **User-Specific Dashboard:** Get a quick overview of your latest entries and insights with a user-specific dashboard that keeps you up-to-date.
- **Breakthrough Moments:** Mark significant insights with the "Breakthrough" tag, signifying pivotal moments in your learning journey.

## Future Enhancements

- **Automatic Hashtags:** Coming soon, automatic hashtag generation will help you easily categorize and explore your journal entries by topics and themes.
- **Learning Groups:** Form learning groups and share entries exclusively within your group members, fostering collaborative learning experiences while maintaining privacy.
- **Public Entries:** Choose to make select journal entries public, allowing you to share your insights with a broader community of learners and experts.

## License

This project is licensed under the GNU General Public License v3.0.

## Contact Information

For any questions, comments, ideas or feedback, feel free to contact the original author on Github at https://github.com/yogajones

