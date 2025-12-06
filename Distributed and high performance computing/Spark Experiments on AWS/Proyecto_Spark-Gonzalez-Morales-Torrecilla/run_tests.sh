#!/bin/bash

# Directory where logs will be stored
LOG_DIR="logs"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Input files to test (adjust names if needed)
INPUT_FILES=("infoActors.csv" "infoActorsX2.csv" "infoActorsX4.csv" "infoActorsX8.csv" "infoActorsX16.csv")

# Programs to test (adjust paths if needed)
PROGRAMS=(
  "python3 python_actorDirector.py"
  "$SPARK_HOME/bin/spark-submit --master=spark://ip-172-31-28-10.ec2.internal:7077 DF_actorDirector.py"
  "$SPARK_HOME/bin/spark-submit --master=spark://ip-172-31-28-10.ec2.internal:7077 RDD_actorDirector.py"
)

# Run all combinations
for file in "${INPUT_FILES[@]}"; do
  for prog in "${PROGRAMS[@]}"; do
    # Extract program name for logging (e.g., "DF_actorDirector")
    prog_name=$(echo "$prog" | awk '{print $NF}' | sed 's/.py//')
    
    # Define log file path (e.g., logs/python_actorDirector_infoActors.csv.log)
    LOG_FILE="$LOG_DIR/${prog_name}_${file}.log"
    
    echo "Running: $prog '$file'"
    echo "Logging to: $LOG_FILE"
    
    # Run with /usr/bin/time and redirect all output to log file
    /usr/bin/time -v $prog "$file" &> "$LOG_FILE"
    
    echo "--------------------------------------"
  done
done

echo "All tests completed. Logs saved to $LOG_DIR/"