# Installation:

This has been tested with python 3.12.7.


1. Create venv
```
virtualenv venv
```
2. Activate venv & install requirements
```
. ./venv/bin/activate
pip install -r requirements.txt
```
3. Get a service account file, it does not need to be on a real gcloud project.

4. Setup env variables:
```
export DATASTORE_EMULATOR_HOST=0.0.0.0:8081
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service/account
```

5. start the sample app (at this point, it wont work, we need to start the emulator) :
```
python main.py
```

6. On a separate terminal, install and start emulator:
[Installation](https://cloud.google.com/firestore/docs/emulator#install)

```
gcloud emulators firestore start --database-mode datastore-mode   --export-on-exit ./saved_data  --host-port 0.0.0.0:8081 --project  [PROJECT-ID]
```

Where [PROJECT-ID] matches service account's "project_id" key


# Reproducing issue
1. reload the app page a few time. The number of rows display increases, which attest that the data is stored on the emulator. The datastore emulator will also display `AM io.gapi.emulators.netty.HttpVersionRoutingHandler channelRead`
2. Stop the emulator using `Ctrl + C`. I expect this to write a file in my specified directory, it does not.



# Note: 

This repro is an adaptation of [GCP python docs samples](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/appengine/standard_python3/building-an-app/building-an-app-3) adapted to use ndb.
