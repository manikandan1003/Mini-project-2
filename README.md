# Mini-project-2
Placement Eligibility App
I created a dataset with the following columns: student_id, name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year, language, problems_solved, assessments_completed, mini_projects, certifications_earned, latest_project_score, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills, mock_interview_score, internships_completed, placement_status, company_name, placement_package, interview_rounds_cleared, and placement_date. After creating the dataset, I checked for any null values.

I cleaned the null values using df.loc and ensured that the data was clean and complete.

Next, I established a connection between Python and MySQL using XAMPP. Once the connection was successful, I imported the cleaned data into MySQL and used it to analyze answers to specific questions.

Finally, I created a Streamlit application in VS Code and connected it to MySQL using the appropriate connection code. In the Streamlit app, I included an image, a sidebar, student placement details, student information, and a section for answering various questions.
