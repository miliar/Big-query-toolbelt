# Big query toolbelt

Tool for copy tables, delete tables and write queries for time range


<img width="685" alt="Screenshot 2019-09-13 at 10 57 00" src="https://user-images.githubusercontent.com/35922697/64850497-cb00df00-d615-11e9-953b-924a31df87b7.png">


Setup:
- Create a folder ```bq_service_account```, place your service account file inside and name it ```bq_service_account.json```
- ```docker build -t bq_toolbelt .```     (<-- Don't miss the point)

Run the app:
- ```docker run -p 4000:4000 bq_toolbelt```
- In your browser, visit http://localhost:4000/
