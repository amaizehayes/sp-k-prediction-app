#!/bin/bash
python sp-k-prediction-app/scripts/spk_probables.py #run multiples times
python sp-k-prediction-app/scripts/team_k_splits.py #run once
python sp-k-prediction-app/scripts/spk_logs_scrape.py #run once
python sp-k-prediction-app/scripts/spk_odds_api.py #run multiple times, historic element to figure out
python sp-k-prediction-app/scripts/spk_output.py #run multiple times
python sp-k-prediction-app/scripts/spk_sim.py #run multiple times
python sp-k-prediction-app/scripts/spk_actuals.py #run once
python sp-k-prediction-app/scripts/spk_push.py #run when pushing