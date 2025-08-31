#!/bin/bash

# Test script for Weather API
echo "🧪 Testing Weather API..."

# Start the server in background
echo "🚀 Starting Weather API server..."
cd go-projects/weather-api
go run main.go &
SERVER_PID=$!

# Wait for server to start
sleep 3

echo ""
echo "📊 Testing endpoints..."

# Test health endpoint
echo "🔍 Testing health endpoint..."
curl -s http://localhost:8080/health | python -m json.tool

# Test single city weather
echo ""
echo "🔍 Testing single city weather..."
curl -s http://localhost:8080/api/weather/london | python -m json.tool

# Test multiple cities weather
echo ""
echo "🔍 Testing multiple cities weather..."
curl -s "http://localhost:8080/api/weather?cities=london,newyork,tokyo" | python -m json.tool

# Test cached cities
echo ""
echo "🔍 Testing cached cities..."
curl -s http://localhost:8080/api/cities | python -m json.tool

# Stop the server
echo ""
echo "⏹️ Stopping server..."
kill $SERVER_PID 2>/dev/null || true

echo ""
echo "✅ Weather API testing completed!"
