#!/bin/bash
python scripts/spk_probables.py #run multiples times
python scripts/team_k_splits.py #run once
python scripts/spk_logs_scrape.py #run once
python scripts/spk_odds_api.py #run multiple times, historic element to figure out
python scripts/spk_output.py #run multiple times
python scripts/spk_sim.py #run multiple times
python scripts/spk_actuals.py #run once
python scripts/spk_push.py #run when pushing