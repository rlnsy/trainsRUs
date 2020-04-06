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

4. Tear down when done unless you want to murder your battery
```
./run.sh stack-down
```