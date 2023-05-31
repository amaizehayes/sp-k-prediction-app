#!/bin/bash
python scripts/spk_probables.py
python scripts/team_k_splits.py
python scripts/spk_logs_scrape.py
python scripts/spk_odds_api.py
python scripts/spk_output.py
python scripts/spk_sim.py
python scripts/spk_actuals.py
python spk_push.py