#!/bin/bash
CLOUD_RUN_URL="https://mlops-api-385501609124.us-central1.run.app"
FUNCTION_URL="https://us-central1-mlops-milestone1-486120.cloudfunctions.net/mlops-function"
PAYLOAD='{"features": [8.3252, 41.0, 6.9841, 1.0238, 322.0, 2.5556, 37.88, -122.23]}'

# Smart Project Directory Detection
if [ -f "main.py" ]; then
    PROJECT_DIR="."
    echo "📂 Found files in current directory."
elif [ -f "milestone_1/main.py" ]; then
    PROJECT_DIR="milestone_1"
    echo "📂 Found files in milestone_1 directory."
else
    echo "❌ Could not auto-locate main.py. Make sure you are in the project folder."
    exit 1
fi

echo "========================================"
echo "🛡️  IDS 568 AUTOMATED SANITY CHECK"
echo "========================================"

echo -e "\n[1] Checking Required Files..."
test -f "$PROJECT_DIR/main.py" && echo "✅ main.py found" || echo "❌ main.py missing"
test -f "$PROJECT_DIR/requirements.txt" && echo "✅ requirements.txt found" || echo "❌ requirements.txt missing"
test -f "$PROJECT_DIR/model.pkl" && echo "✅ model.pkl found" || echo "❌ model.pkl missing"

echo -e "\n[2] Checking Dependency Pinning..."
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    UNPINNED=$(grep -E '^[a-zA-Z]' "$PROJECT_DIR/requirements.txt" | grep -v '==' | grep -v '^#')
    if [ -z "$UNPINNED" ]; then
        echo "✅ All dependencies are pinned"
    else
        echo "⚠️  Warning: Unpinned dependencies found:"
        echo "$UNPINNED"
    fi
else
    echo "❌ requirements.txt not found"
fi

echo -e "\n[3] Checking Pydantic Schemas..."
grep -E "class.*BaseModel" "$PROJECT_DIR/main.py" > /dev/null && echo "✅ Pydantic models found" || echo "❌ No Pydantic models found"

echo -e "\n[4] Testing Cloud Run Endpoint..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$CLOUD_RUN_URL/predict" \
    -X POST -H "Content-Type: application/json" -d "$PAYLOAD")
if [ "$HTTP_CODE" -eq 200 ]; then echo "✅ Cloud Run success (200 OK)"; else echo "❌ Cloud Run failed ($HTTP_CODE)"; fi

echo -e "\n[5] Testing Cloud Function Endpoint..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FUNCTION_URL" \
    -X POST -H "Content-Type: application/json" -d "$PAYLOAD")
if [ "$HTTP_CODE" -eq 200 ]; then echo "✅ Cloud Function success (200 OK)"; else echo "❌ Cloud Function failed ($HTTP_CODE)"; fi

echo -e "\n========================================"
echo "🎉 Sanity Check Complete!"
echo "========================================"
