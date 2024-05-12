Files are set based on google colab environment.

`pos_json.json` file contains labeled non-deprecated sample packages in form: [{"id": , "query": , "model_answer": , "alternative_method": "" "label": },]

`neg_json.json` file contains labeled deprecated sample packages in form: [{"id": , "query": , "model_answer": , "alternative_method": "" "label": },]

`neg_json_output.json` file contains labeled deprecated sample packages with predicted alternative methods in form: [{"id": , "query": , "model_answer": , "alternative_method": "" "label": },]

Please upload the pos_json.json and neg_json.json file to the `/content` directory in google colab.

It is recommended to forecast in batches and save the output file in time, rather than forecast all the data at once.