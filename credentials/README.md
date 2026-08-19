\# credentials/



Gitignored on purpose. Put your local `service-account.json` here — never commit it.



Get the key from the project owner, or generate one:

gcloud iam service-accounts keys create credentials/service-account.json \\

&#x20; --iam-account=olist-pipeline-sa@<PROJECT\_ID>.iam.gserviceaccount.com



Then: export GOOGLE\_APPLICATION\_CREDENTIALS="$(pwd)/credentials/service-account.json"

