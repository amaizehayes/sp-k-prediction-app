#!/bin/bash
python sp-k-prediction-app/scripts/spk_logs_scrape.py #run once
python sp-k-prediction-app/scripts/spk_actuals.py #run once
python sp-k-prediction-app/scripts/spk_push.py #run when pushing