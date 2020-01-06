gcloud functions deploy leads --runtime python37 --trigger-event providers/cloud.firestore/eventTypes/document.write --trigger-resource projects/ml-saas/databases/leads/documents/messages/{pushId}
