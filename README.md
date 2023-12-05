# timeline-wrapup

Quick script to generate a top 20 of places visited from your Google Timeline

1. Download your Google Timeline data here: https://takeout.google.com/ (only select _Location History_). 
   - You should receive a compressed file containing a `Semantic Location History` directory. Enclosed is a list of twelve directories split up by years, containing a JSON file for each month of that year. 
3. Set up your constants, including your `DIRECTORY` path. Make sure that it points to a single year (i.e. `/2023/` only) 
4. yYu can view your top 20 by frequency of visits (count) or total amount of time. 
5. Run `python timeline_analysis.py`. 
