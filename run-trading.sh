#!/bin/bash
cd /home/azureuser/ai-Trader
source venv/bin/activate
python main.py >> trading.log 2>&1