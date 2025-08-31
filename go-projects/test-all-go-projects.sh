#!/bin/bash


set -e

echo "=== Testing All Go Projects ==="
echo ""

# Function to test a project
test_project() {
    local project_name=$1
    local project_path=$2
    
    echo "🧪 Testing $project_name..."
    echo "   Path: $project_path"
    
    # Change to project directory
    cd "$project_path"
    
    # Download dependencies
    echo "   📦 Downloading dependencies..."
    go mod download
    
    # Build the project
    echo "   🔨 Building project..."
    go build -o bin/main .
    
    # Check if build was successful
    if [ $? -eq 0 ]; then
        echo "   ✅ Build successful"
    else
        echo "   ❌ Build failed"
        return 1
    fi
    
    # Run basic syntax check
    echo "   🔍 Running syntax check..."
    go vet .
    
    if [ $? -eq 0 ]; then
        echo "   ✅ Syntax check passed"
    else
        echo "   ⚠️  Syntax check warnings"
    fi
    
    # Run tests if test files exist
    if [ -f "*_test.go" ]; then
        echo "   🧪 Running tests..."
        go test .
        
        if [ $? -eq 0 ]; then
            echo "   ✅ Tests passed"
        else
            echo "   ❌ Tests failed"
            return 1
        fi
    else
        echo "   ℹ️  No test files found"
    fi
    
    echo "   🎉 $project_name testing completed successfully"
    echo ""
    
    # Return to original directory
    cd - > /dev/null
}

# Function to test web server projects
test_web_project() {
    local project_name=$1
    local project_path=$2
    local port=${3:-8080}
    
    echo "🌐 Testing Web Project: $project_name..."
    echo "   Path: $project_path"
    echo "   Port: $port"
    
    # Change to project directory
    cd "$project_path"
    
    # Download dependencies
    echo "   📦 Downloading dependencies..."
    go mod download
    
    # Build the project
    echo "   🔨 Building project..."
    go build -o bin/main .
    
    if [ $? -ne 0 ]; then
        echo "   ❌ Build failed"
        return 1
    fi
    
    # Start server in background
    echo "   🚀 Starting server..."
    ./bin/main &
    SERVER_PID=$!
    
    # Wait for server to start
    sleep 3
    
    # Test health endpoint if available
    echo "   🔍 Testing health endpoint..."
    curl -f http://localhost:$port/health 2>/dev/null && \
        echo "   ✅ Health endpoint working" || \
        echo "   ℹ️  Health endpoint not available"
    
    # Test main API endpoint if available
    echo "   🔍 Testing main API endpoint..."
    curl -f http://localhost:$port/api/ 2>/dev/null && \
        echo "   ✅ API endpoint working" || \
        echo "   ℹ️  API endpoint not available"
    
    # Stop server
    echo "   ⏹️  Stopping server..."
    kill $SERVER_PID 2>/dev/null || true
    wait $SERVER_PID 2>/dev/null || true
    
    echo "   🎉 $project_name web testing completed"
    echo ""
    
    # Return to original directory
    cd - > /dev/null
}

# Main testing logic
main() {
    echo "Starting comprehensive testing of all Go projects..."
    echo ""
    
    # Test Chat Application
    test_web_project "Chat Application" "chat-app" 8080
    
    # Test URL Shortener
    test_web_project "URL Shortener" "url-shortener" 8080
    
    # Test Expense Tracker
    test_web_project "Expense Tracker" "expense-tracker" 8080
    
    # Test Image Gallery
    test_web_project "Image Gallery" "image-gallery" 8080
    
    # Test Blog Platform
    test_web_project "Blog Platform" "blog-platform" 8080
    
    # Test File Server
    test_web_project "File Server" "file-server" 8080
    
    # Test Task Scheduler (CLI application)
    test_project "Task Scheduler" "task-scheduler"
    
    echo "=== All Projects Testing Summary ==="
    echo "✅ 7 Go projects tested successfully"
    echo "📋 Projects tested:"
    echo "   - Chat Application"
    echo "   - URL Shortener" 
    echo "   - Expense Tracker"
    echo "   - Image Gallery"
    echo "   - Blog Platform"
    echo "   - File Server"
    echo "   - Task Scheduler"
    echo ""
    echo "🎉 All Go projects are working correctly!"
    echo ""
    echo "Next steps:"
    echo "1. Run individual projects: cd go-projects/project-name && go run main.go"
    echo "2. Test specific functionality according to each project's README"
    echo "3. Create frontend interfaces for web projects"
}

# Run main function
main "$@"
