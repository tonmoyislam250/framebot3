#!/bin/bash
pwd && ls -a
cd /usr/src/app
mkdir RAW
gdown $LINK
unzip -q -d RAW/ "$VIDEO_NAME.zip"

# Initialize progress tracking
PROGRESS_FILE="posting_progress.txt"
TOTAL_COUNT=$(ls RAW/ | wc -l)
POSTED_COUNT=0

# Function to get current progress
get_posted_count() {
    if [ -f "$PROGRESS_FILE" ]; then
        POSTED_COUNT=$(cat "$PROGRESS_FILE" 2>/dev/null || echo 0)
    else
        POSTED_COUNT=0
    fi
}

# Function to run python script with retry mechanism
run_with_retry() {
    while true; do
        get_posted_count
        REMAINING_COUNT=$((TOTAL_COUNT - POSTED_COUNT))
        
        if [ $REMAINING_COUNT -le 0 ]; then
            echo "All frames have been posted successfully!"
            break
        fi
        
        echo "Starting/Resuming posting from frame $((POSTED_COUNT + 1)). Remaining: $REMAINING_COUNT frames"
        
        # Run the python script
        python3 post.py --page-id $PAGE_ID --pdir "RAW/" --token $ACCESS_TOKEN --start $((START + POSTED_COUNT)) --count $REMAINING_COUNT --delay 60
        
        EXIT_CODE=$?
        
        if [ $EXIT_CODE -eq 0 ]; then
            echo "Python script completed successfully!"
            break
        else
            echo "Python script exited with code $EXIT_CODE. Checking progress and retrying..."
            sleep 5
        fi
    done
}

# Run the script with retry mechanism
run_with_retry
