## Live Site!
https://gooddeeds.streamlit.app/

## Inspiration
With the unfortunate recent rise of natural disasters and man-made tragedies seemingly hitting the news more often, we came to realize that there is no active platform made exclusively for volunteers and community service organizers to come together. Existing systems for **community** efforts are often scattered, lack incentives, and don’t prioritize ease of connection between organizations and individuals who want to help. We wanted to change that by building a _streamlined_ solution that not only encourages more people to volunteer but also supports local organizers in community service and **managing** disaster recovery. By providing a centralized platform, incentives for volunteers, and regular communication through automated emails, we aim to make community engagement accessible, rewarding, and impactful for everyone involved.

## What it does
GoodDeeds targets two groups: **volunteers** and **organizers**, and we aimed to simplify the process for both. At a high level:
- A user signs up, and provides their location and a distance they are willing to travel. 
- An Organization posts an event, automatically triggering an email to every volunteer that is able to come to the location.
- A weekly email is also sent to all users with upcoming events within a user's travel distance.

Users are also able to view upcoming events through the platform, connect with a chatbot for any questions, and earn xp and other incentives for participating!

## How we built it
Data is stored in a Postgres instance, which is queried by a Flask-RESTful API. Our Flask API has three main tasks: handling the necessary basic CRUD operations, location-based user/event filtering, and mailing. A Streamlit app on the frontend provides volunteer/organization sign ups/logins and event creation. 

## Challenges we ran into
One challenge was querying efficiently - since volunteers may have a wide variety of available commuting distances, finding potential participants for an event involves is potentially computation-expensive.

## Accomplishments that we're proud of
Something I'm personally (Andrew) proud of is mailing - I was able to set up an service to dynamically generate HTML for a given event(s), and automatically send it in an email to volunteers!

## What we learned
For Amruth and Andrew, this was our first ever Hackathon! Although we've both had experience in AI and software development, this was a super new and great learning experience. I've never personally deployed any project from the ground up - learning to set up and deploy Postgres, our Flask API, and Frontend was really cool. 

## What's next for GoodDeeds:
# Brand Partnerships

- Develop a points-based rewards program where volunteers earn discounts or promo codes from partner brands that align with your mission.

- Offer tiered sponsorship levels with more prominent placement for higher-level partners, highlighting them on your website and in volunteer communications.

# NGO Partnerships

- Build relationships with diverse local and international NGOs to offer a wide range of opportunities, creating a streamlined onboarding process for them to list volunteer needs.

- Provide NGOs with tools to manage volunteers through your platform and offer impact reporting to demonstrate the value of partnering with GoodDeeds.

By focusing on these core strategies, you can create a robust ecosystem that rewards volunteers, provides value to sponsors, and increases your overall impact.

![image](https://github.com/user-attachments/assets/39731886-0468-4703-8967-72eab7934166)
