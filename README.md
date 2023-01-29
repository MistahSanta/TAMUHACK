## Inspiration
- We wanted to create a straightforward approach to the CBRE challenge with a beautiful UI that keeps in scalability in mind. 

## What it does
- Our project is a web application which helps companies optimize the use of their office space, by distributing teams into different floors in an office space based on floor capacity, team size, and team preference. The web app is scalable, more team or floor can be added.

## How we built it
- We used Python, Flask, Numpy and Pandas to design the backend. For the frontend, we used Jinja for client side code, HTML, CSS, and Bootstrap for styling. For deployment, we used Microsoft Azure App Service.

## Challenges we ran into
- We originally used React.js for the frontend, but since most of our program was in Python, we used Flask templates to consolidate the frontend and backend. This was better in the long run, but required some extra dev time that wouldn't have been necessary had we utilized Flask templates from the start. 
- Initially, we considered using a decision tree before settling on our current implementation, which attempts to greedily fill each floor with teams, keeping in mind that some teams should not be placed on the same floor by any means necessary. 
- We didn't catch a bug in time in which it only compare the first list instead of the current team, yielding an invalid Floor 5 in which team 2, 5, 6 are all on the no way list and the algorithm still places these teams on the same floors.
- Flask templates is not designed to make reactive components unlike React, so we were unable to complete the save table component.

## Accomplishments that we're proud of
- We are proud of the algorithm and backend structure, because it works consistently and we were to integrate the data into the web page easily. 
- We also pivoted from a React app to serving static HTML templates from Flask which was challenging. - - This was our first time using Azure for deployment in a tech domain.  

## What we learned
- We learned how to apply data structures and algorithms to complex real-world problems.
- We learned how to make an API with Flask, parse and process data of CSV with Numpy and Pandas, and, finally, style our frontend with Bootstrap.
- We also learned a bit of Machine Learning decision tree, before we scraped the plan for our current algorithms.

## What's next
- In the future, we want to implement machine learning to sort the teams based on other attributes, such as a need for cross team collaboration. 
- We would also like to improve the user experience by adding collapse menu, allowing users to upload data, and white-labeling the application for companies to use with their clients in a business-to-business environment.
