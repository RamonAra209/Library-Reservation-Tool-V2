# Library-Reservation-Tool-V2
This is the successor to my first [Library Reservation Tool](https://github.com/RamonAra209/Library-Reservation-Tool)!

But why successor? Because my school decided to update their website and it broke the old one
After a semester of putting it off, I finally got around to fixing it. 
Proud to say that V2 averages ~5sec, as opposed to V1's ~45sec
## The problem

Imagine, you're a computer science student. You and your friends hold study sessions in your
universities library every other day at specific times. 

Your university has a website to reserve a study room, all you have to do is find which room
and times you want, enter relevant information such as your name and email, and click reserve.

## My solution
I quickly realized that reserving study rooms on a reoccuring basis was tedious. Every other day
I would havve to go into the library's room reservation website, and reserve it manually. 

To avoid such a tedious task, I created this program to scrape room data (i.e. which rooms were 
available at specified times), and to reserve any rooms that fit critera defined by me (i.e. reoccurring
days and reoccuring times).

## Outcome
Our university website refreshes the available rooms everyday, for two days in advance.
For example, if you want to reserve a room on wednesday, those rooms/times will become available monday.

Now, I never have to reserve a room manually again. I host the automation script on my raspberry pi, and it 
reserves me a room 2 days before I need it. 
