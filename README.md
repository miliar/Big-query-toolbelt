# Big query toolbelt

Tool for copy tables, delete tables and write queries for time range


<img width="831" alt="Screenshot 2019-07-31 at 16 17 29" src="https://user-images.githubusercontent.com/35922697/62219741-2604ac80-b3af-11e9-89a8-bca20eb37d40.png">

Setup:
- Create a folder ```bq_service_account```, place your service account file inside and name it ```bq_service_account.json```
- ```docker build -t bq_toolbelt .```     (<-- Don't miss the point)

Run the app:
- ```docker run -p 4000:4000 bq_toolbelt```
- In your browser, visit http://localhost:4000/
