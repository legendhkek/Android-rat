#!/bin/bash

# APK Modifier - Advanced Build Script
# Automated build with all configurations

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   APK Modifier - Advanced Build       ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo ""

# Function to print status
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[i]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check Java
    if command -v java &> /dev/null; then
        JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2)
        print_status "Java found: $JAVA_VERSION"
    else
        print_error "Java not found. Install JDK 11+"
        exit 1
    fi
    
    # Check Android SDK
    if [ -z "$ANDROID_HOME" ]; then
        print_error "ANDROID_HOME not set"
        echo "Set it with: export ANDROID_HOME=/path/to/android-sdk"
        exit 1
    else
        print_status "ANDROID_HOME: $ANDROID_HOME"
    fi
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_status "Python found: $PYTHON_VERSION"
    else
        print_error "Python3 not found"
        exit 1
    fi
    
    echo ""
}

# Install Python dependencies
install_python_deps() {
    print_info "Installing Python dependencies..."
    pip install -q -r requirements.txt
    print_status "Python dependencies installed"
    echo ""
}

# Build configuration
select_build_type() {
    echo -e "${YELLOW}Select build type:${NC}"
    echo "1) Debug   - Fast build, with debugging"
    echo "2) Release - Production, FUD enabled (recommended)"
    echo ""
    read -p "Choice [1-2]: " choice
    
    case $choice in
        1)
            BUILD_TYPE="Debug"
            GRADLE_TASK="assembleDebug"
            ;;
        2)
            BUILD_TYPE="Release"
            GRADLE_TASK="assembleRelease"
            ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac
    
    print_status "Selected: $BUILD_TYPE build"
    echo ""
}

# Clean previous builds
clean_build() {
    print_info "Cleaning previous builds..."
    cd android-app
    ./gradlew clean > /dev/null 2>&1
    cd ..
    print_status "Build directory cleaned"
    echo ""
}

# Build APK
build_apk() {
    print_info "Building APK ($BUILD_TYPE)..."
    print_info "This may take 5-10 minutes..."
    echo ""
    
    cd android-app
    ./gradlew $GRADLE_TASK
    
    if [ $? -eq 0 ]; then
        print_status "APK built successfully!"
        echo ""
        
        # Find APK
        if [ "$BUILD_TYPE" == "Debug" ]; then
            APK_PATH="app/build/outputs/apk/debug/app-debug.apk"
        else
            APK_PATH="app/build/outputs/apk/release/app-release.apk"
        fi
        
        if [ -f "$APK_PATH" ]; then
            APK_SIZE=$(du -h "$APK_PATH" | cut -f1)
            print_info "APK Location: android-app/$APK_PATH"
            print_info "APK Size: $APK_SIZE"
            echo ""
            
            # Copy to root for easy access
            cp "$APK_PATH" "../APK_Modifier_${BUILD_TYPE}.apk"
            print_status "Copied to: APK_Modifier_${BUILD_TYPE}.apk"
        fi
    else
        print_error "Build failed!"
        exit 1
    fi
    
    cd ..
    echo ""
}

# Sign APK (for release)
sign_apk() {
    if [ "$BUILD_TYPE" == "Release" ]; then
        echo -e "${YELLOW}Sign APK?${NC} [y/N]: "
        read -p "" sign_choice
        
        if [ "$sign_choice" == "y" ] || [ "$sign_choice" == "Y" ]; then
            print_info "Signing APK..."
            
            # Check for keystore
            if [ ! -f "apk-modifier.keystore" ]; then
                print_info "Creating keystore..."
                keytool -genkey -v \
                    -keystore apk-modifier.keystore \
                    -alias apk-modifier \
                    -keyalg RSA \
                    -keysize 2048 \
                    -validity 10000
            fi
            
            # Sign
            if command -v apksigner &> /dev/null; then
                apksigner sign \
                    --ks apk-modifier.keystore \
                    --out APK_Modifier_Signed.apk \
                    APK_Modifier_Release.apk
                print_status "APK signed: APK_Modifier_Signed.apk"
            else
                print_error "apksigner not found. Install Android SDK Platform-Tools."
            fi
        fi
    fi
    echo ""
}

# Generate summary
generate_summary() {
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║         Build Complete!                ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
    echo ""
    
    print_info "Build Summary:"
    echo "  • Build Type: $BUILD_TYPE"
    echo "  • APK File: APK_Modifier_${BUILD_TYPE}.apk"
    
    if [ -f "APK_Modifier_Signed.apk" ]; then
        echo "  • Signed APK: APK_Modifier_Signed.apk"
    fi
    
    echo ""
    print_info "Next Steps:"
    echo "  1. Install APK:"
    echo "     adb install APK_Modifier_${BUILD_TYPE}.apk"
    echo ""
    echo "  2. Or run Python server:"
    echo "     python app.py"
    echo ""
    print_info "Documentation:"
    echo "  • README_SOURCE.md - Complete source guide"
    echo "  • ../BUILD_INSTRUCTIONS.md - Detailed instructions"
    echo ""
}

# Main execution
main() {
    check_prerequisites
    select_build_type
    install_python_deps
    clean_build
    build_apk
    sign_apk
    generate_summary
}

# Run
main
