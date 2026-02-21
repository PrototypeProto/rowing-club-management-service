# Rowing Club Management Service

### This is a personal project where the primary goal is to learn a new set of technologies and improve my working knowledge of what I know, that being:

<ul>
    <li><b>Python</b> (3.14.2)</li>
    <li><b>SQLAlchemy</b> (Python SQL toolkit and Object Relational Mapper)</li>
    <li><b>Alembic</b> (Database migration tool)</li>
    <li><b>PostgreSQL</b> (SQL database)</li>
    <li><b>Redis</b> (In-memory database)</li>
    <li><b>Docker</b> Containerized applications</li>
    <li>... and many more libraries to provide greater functionality and security</li>
</ul>

<br>
This project is inspired by my experience at my University's rowing club (Hence a service dedicated to rowing) and my observation of their needs.
</br>
<br>
As it stands, it is a standalone service, lacking a front end wrapper to use this. I will most likely work on one once this is completed using React. 
</br>

## TODO

### Planning

<ol>
    <li>Calendar</li>
        <ul>
            <li>Attendance</li>
                <ul>
                    <li>tracking absences only</li>
                    <li>assumed present if not absent</li>
                </ul>
            <li>Availability</li>
                <ul>
                    <li>Monitors anticipated availability of all members (for the week)</li>
                    <li>unsure how to go about storing this one</li>
                </ul>
            <li>Practice schedules</li>
                <ul>
                    <li>Dates</li>
                        <ul>
                            <li>contains info on what will be done on practice (Land vs Water and Intensity)</li>
                            <li>Varies on day-by-day basis</li>
                        </ul>
                </ul>
        </ul>
    <li>Volunteering (Maybe merge with calendar or keep standalone)</li>
        <ul>
            <li>Headcount for anticipated members</li>
            <li>Track who has/n't volunteered</li>
        </ul>
    <li>Feedback</li>
        <ul>
            <li>Session (Create a feedback opportunity each session)</li>
                <ul>
                    <li>Coxwains</li>
                        <ul>
                            <li>general thoughts on overall performance up to this point in the semester</li>
                        </ul>
                    <li>Boats</li>
                        <ul>
                            <li>Opinions of the coxwain and rowers on a specific boat in relations to performance and constructive criticism</li>
                        </ul>
                </ul>
            <li>General (random feedback, undated and not required)</li>
                <ul>
                    <li>Rowers</li>
                </ul>
        </ul>
</ol>

### Data

<ul>
    <li>Membership</li>
        <ul>
            <li>**Possibly in the distant future** Implement stripe payment for dues payment</li>
        </ul>
</ul>

### Data Processing

<ol>
    <li>Boats</li>
        <ul>
            <li>min, max, avg pace</li>
            <li>distance travelled</li>
            <li>rowers & coxwains on boat</li>
                <ul>
                    <li>Rower contribution score (RCS)</li>
                    <ul>
                        <li>FURTHER RESEARCH REQUIRED. find mathematical representation to estimate combined effort to speed</li>
                        <li>Avg out performance of boats rower was in</li>
                    </ul>
                    <li>Boat power & expected boat power based off RCS</li>
                </ul>
        </ul>
    <li>Workouts</li>
        <ul>
            <li>Ergs</li>
                <ul>
                    <li>Varies as not everyone does the same workouts</li>
                </ul>
            <li>Water</li>
                <ul>
                    <li>Varies as not everyone does the same workouts</li>
                </ul>
            <li>Mile Runs</li>
            <li>Black & Gold</li>
                <ul>
                    <li>Submissions for different teams</li>
                        <ul>
                            <li>Teams are Gold & Black, teams are same for the school year (fall-spr)</li>
                        </ul>
                </ul>
            <li>Notes:</li>
                <ul>
                    <li>Allow partial submissions (Sometimes members can't finish for some reason)</li>
                    <li>Will have users manually inputting their performance</li>
                    <li>Some are repeated, making it easy to track performance over time</li>
                    <li>Are done in sequential order</li>
                    <li>may track wattage, pace and/or distance of member</li>
                </ul>
        </ul>
</ol>

## GOALS

### Completed

<ul>
    <del>
        <li>Build a simple web server</li>
    </del>
    <del>
        <li>API paths</li>
    </del>
    <del>
        <li>Request Bodies</li>
    </del>
    <del>
        <li>Organize API Paths with Routers</li>
    </del>
    <del>
        <li>Databases With SQLModel</li>
    </del>
    <del>
        <li>Creating a database model with SQLModel</li>
    </del>
    <del>
        <li>Creating database tables</li>
    </del>
    <del>
        <li>CRUD With SQLModel</li>
    </del>
    <del>
        <li>Separate CRUD logic using service classes</li>
    </del>
    <del>
        <li>Use service methods in API path handlers</li>
    </del>
    <del>
        <li>Create the user auth model</li>
    </del>
    <del>
        <li>Database Migrations With Alembic</li>
    </del>
    <del>
        <li>User Account Creation</li>
    </del>
    <del>
        <li>Password hashing with bcrypt</li>
    </del>
    <del>
        <li>JWT Authentication</li>
    </del>
    <del>
        <li>PyJWT Setup</li>
    </del>
    <del>
        <li>User Login Endpoint</li>
    </del>
    <del>
        <li>Add roles to the user model</li>
    </del>
    <del>
        <li>HTTP Bearer Authentication</li>
    </del>
    <del>
        <li>Regaining Access with refresh tokens</li>
    </del>
    <del>
        <li>Revoking Tokens using Redis</li>
    </del>
</ul>

### WIP

<ul>
    <li>Read and set headers</li>
    <li>Role-Based Access Control</li>
    <li>Get the currently authenticated user</li>
    <li>Error Handling</li>
    <li>Create custom API Exceptions and exception handlers</li>
    <li>Register Error handlers on the app</li>
    <li>Create a custom logging middleware</li>
    <li>Use Custom ASGI middleware with FastAPI</li>
    <li>Adding CORS Middleware</li>
    <li>Adding Trusted Hosts</li>
    <li>Setting Up FastAPI-Mail</li>
    <li>User account verification</li>
    <li>Password Reset</li>
    <li>Background Tasks</li>
    <li>FastAPI Background Tasks</li>
    <li>Background Tasks with Celery and Redis</li>
    <li>Celery Monitoring With Flower</li>
    <li>API Testing</li>
    <li>Unit-tests with Unittest Mock and Pytest</li>
    <li>Document-driven Testing with Schemathesis</li>

</ul>

### A big thanks to Mr. Ssali Jonathan's guidance, providing great inspiration, and making this possible in the first place.
