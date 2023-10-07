# BMR Calculator - By Rushil Shah from Fremont,CA (USA). Age: 16 Date: 12/31/21
#### Video Demo:  https://www.youtube.com/watch?v=Oo4D8tzKAoE
#### Description:

    I decided to make a BMR calculator for my final project. BMR stands for Basal Metabolic Rate and it essentially
tells the user based on their sex, age, height, and weight, what their caloric intake should be for a given day. I decided
to make this calculator based off bad eating habits I have myself. Oftentimes, I don't eat as much and am underweight. I created this
calculator in hopes that it would tell me what my caloric intake should be in order to achieve my goal for gaining weight.

    First off, before I dive into the specifics I would like to cite sources of several bits of code I used. I used apology.html
and helpers.py files from the week 9 problem set. I did not know how to replicate the files on my own so I understand them and then incorporated them
into my own project. I also the basic foundation of application.py and layout.html from my week 9 problem set when making this project. Lastly,
I would like to credit the youtube video https://www.youtube.com/watch?v=E2hytuQvLlE for giving me a basic tutorial and the javascript code
(see users.html) on how to display charts with flask.

    When making this project, I wanted to incorporate a login/log out system. I wanted to do this since the calculator should be personalized and store data
for each user. This meant that I had to use Flask in order to do so. First I created a database called project.db which would store all the information regarding each user.
In the database, there were three fields - one with a unique id, another with the username, and the last with a hashed password for security. Then
I created my register and log in pages. The pages were simple with text fields in the register.html page to enter a username, enter a password, and confirm the password.
In login.html I did the same thing but there was only two fields which was to enter the username and password. Then in my application.py I used two routes when the submit button was clicked.
The first route was /register. This route would essentially add the users' information to the database. The route /login was coded by the CS50 staff as in the week 9 problem set
but I altered the destination routes. So after a succesful login the user would be greeted with homepage.html.

    Initially, I thought that a simple login page and register page would suffice for the first user interaction. However, I soon realized that I wanted to add an additional page that the user
would first land on to give them more background information about the BMR calculator and what exactly it is and its functions. This is when I created homepage.html. When making homepage.html, I wanted it to be
organized in a clean manner that is much more presentable than the code I had turned in during problem set 8. To fix the layout of the website, I heavily incorporated bootstrap into the html page. Bootstrap was essential
for homepage.html since it made the HTML page look neat and organized. I used different size rows and columns to organize my information. Using bootstrap was great too, since it allowed my website to dynamically adjust to the size
of the browser on the window. This meant that look of the website would not be affected by the size of the browser. Finally, I ran into the issue of possibly requiring to duplicate homepage.html.
During the design process, I wanted to use homepage.html to both greet the users when they initally open the site and even after they log in. The problem with re-using homepage.html was that I had decided to include a nav-bar
at the bottom of it. The contents of the nav-bar depended on whether the user was logged in or not. If the user was logged in, then the nav-bar would display buttons to sign out, check history, or calculate. Otherwise it would display buttons
to sign in or register. To get around this issue of copy pasting an entire file and changing several lines, I decided to use Jinja and check if the user was logged in or not and then display the appropriate nav-bar. This fixed the issue quite well.

    Next, I had to create a webpage to calculate the BMR. This webpage was calculate.html. The formula for calculating Basal Metabolic Rate differs for men and women. So when making the form, I first created a drop down menu that asked what the
person's gender was. Then I added three text fields (age, height, weight) to calculate the BMR. The BMR would be calculated in the /calculate route. I assigned the genders different values then checked with an if statement which formula to use. Based on the formula I would calculate the person's BMR.
Once I had the calculated BMR, I needed to store it into a database. Hence, in project.db I created a new table that had the BMR, the user_id, and the date the BMR was calculated. After calculating the BMR, I would store the data and then display the users.html page. I did this by redirecting the route
to /user. In this route I accesed the database and returned to users.html the most recently calculated BMR. However, I also form a list of values that contain the date and value of each calculated BMR. Theses lists gets passed to users.html to display in a graph like format.
In users.html, I display the most recently calculated BMR of a user while also showcasing their history in the form of a line graph. I utilized the chart.js library to make this possible. In order to draw the chart, I used the BMR values and dates passed from application.py. I then utilized the javascript code from the
youtube tutorial to display the values. An object of the class chart was created with many arguements passed in that dictated how the chart should be drawn. Finally, I used health.html as a dummy html page to check if certain routes would work from the controller - application.py



