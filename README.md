# Survey Similarity Ranking

## Author
Jaideep Shekhar

DUCS (2022-2024)

## How to Use?

1. Clone the repo with `git clone https://github.com/WitherVexStorm/SurveySimilarityRanking.git`
2. OR fork the repo.
3. OR download the zip.
4. Run the server with `python manage.py runserver`.
5. Open up  `http://127.0.0.1:8000/` in browser of choice.

## Functionality

1. Add users from `/register/` route.
2. Login from `/login/` route.
3. Logout from `/logout/` route.
4. View list of surveys at `/survey/` route. Can create or attempt survey from here. Also use all functionalities.
5. Create a new survey at `/survey/create` route (only allowed by `superuser`).
6. Attempt a survey (Please login properly first!) at `/survey/fill/?survey-id=<id>` route.
7. Find similarity measures at `/survey/find-similarity/?survey-id=<id>` route.
8. Find similarity against particular user by filtering at `/survey/find-similarity-to/?survey-id=<id>&user-id=<uid>` route.
9. Pagination functionality at `/survey/find-similarity-paged/?survey-id=<id>&entries-per-page=<entries>&page-no=<page>` route.
10. Search for similarities between all users matching pattern at `/survey/find-similarity-between/?survey-id=<id>&username-pattern=<pattern>` route.

## Current Users:

1. **adminUser** (`superuser`)
    - username: `adminUser`
    - email: `adminUser@gmail.com`
    - password: `adminUser`
2. **user123**
    - username: `user123`
    - email: `user123@gmail.com`
    - password: `userpassword123`
2. **user456**
    - username: `user456`
    - email: `user456@gmail.com`
    - password: `userpassword456`

## Notes

1. All candidates need to sign up first. Sign up at `/register/`
2. Assuming a canadidate can only attempt survey once.
3. To remove the responses of candidate, run `Answer.objects.filter(user=User.objects.get(id= <id> )).delete()`
4. Also run `Similarity.objects.filter(Q(user_1=User.objects.get(id= <id>) | Q(user_2=User.objects.get(id= <id>) )).delete()`