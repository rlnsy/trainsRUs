## Trains 'R' Us 🚂

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
