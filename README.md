

## REQUIREMENTS
- User can submit and store BP values
- BP values stored in database
- Calculations performed on BP values and displayed for user
- Possible options:
    - Upload pictures of BP readings
    - Print BP values summary over selected time period 

## FRONT END

### Tech: 
- React, React-Router

### Home Page:
- App name
- Registration 
    - Need redirect to login if successful registration
- Login 

### User Home Page:
- Checks credentials, then fetches user specific data from API
- Displays BP data (median/average, time related, etc?)
- Fetch user-specific data from API
    - BP values
    - Pictures? 
- Option to enter new BP data point – new page? 
    - Needs time stamp (user can enter time or pick current time)
    - Needs check if entry is erroneous 
    - Option to add picture? 
- Option to enter/display BP meds 
- Logout option 
    - Redirects to home page


## BACK END

### Tech: 
- Django, Django REST framework, Simple-JWT auth 

### Relational Database: 
- SQLite or PostgreSQL (One-to-Many)

### Tables:
- Users
    - Extended from default Django User Group 
    - Includes default primary key
- Blood Pressures 
    - Default primary key
    - Systolic 
    - Diastolic 
    - Foreign Key linking it to user ID (primary key)

### Calculations:
- Performs calculations on user specific data upon login and returns values for display