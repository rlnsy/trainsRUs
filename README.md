
## Trains 'R' Us 🚂
#### Live demo available [here](http://trainsrus.xyz)
Trains 'R' Us is a web application built to demonstrate the Vue-Flask-PSQL-Docker stack's capacity for quick and agile yet sophisticated development. The application models a sample railway corporation's databases and shows the possibility for a custom built app to deliver that information directly to employees of all types.

For example, employee management overviews:
![Overview Screenshot](https://github.com/rlnsy/trainsRUs/blob/master/doc%20images/Workers.png) 

And responsive, easy to understand forms:
![Worker Form Screenshot](https://github.com/rlnsy/trainsRUs/blob/master/doc%20images/AddWorker.png)
 Provide a clear method of interaction for a database with the following ER schema:
![ER Diagram](https://github.com/rlnsy/trainsRUs/blob/master/New_Milestone3ER.png)
### Deploying
1. Make sure docker commands are available

2. Create runner 
```
chmod +x run.sh
```

3. Run the app
```
./run.sh stack-up
```
  this will set up the postgres+python+flask+frontend stack, and load in initial tables and entries.

Note: occasionally the Database will fail to start properly in which case there will be some
error messages in the docker logs and things won't work properly. If this occurs, simply
tear down the stack, put 'er up again, and hope for the best.

4. Tear down when done unless you want to murder your battery
```
./run.sh stack-down
```
