Stop the autonomous trading cron job.

1. List active cron jobs to find the ID:
```
claude cron list
```

2. Delete the job using CronDelete with the job ID.

Current known job ID: f98fa368

If that doesn't work, list all jobs and cancel any active ones.

3. Confirm it's stopped and show final portfolio status:
```
cd /Users/corri/polymarket-agent && python3 -c "
from agents.trader import get_portfolio
import json
print(json.dumps(get_portfolio(), indent=2))
"
```
