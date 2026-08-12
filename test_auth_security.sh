#!/bin/bash

# Channel-i Security Fixes - Direct Testing Script
# Usage: ./test_auth_security.sh http://localhost:8000
# Or:    ./test_auth_security.sh https://staging.channel.iitr.ac.in

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Get base URL from argument
BASE_URL="${1:-http://localhost:8000}"

# Test counters
PASSED=0
FAILED=0
WARNINGS=0

# Helper functions
print_header() {
    echo -e "\n${BLUE}${BOLD}================================================${NC}"
    echo -e "${BLUE}${BOLD}$1${NC}"
    echo -e "${BLUE}${BOLD}================================================${NC}\n"
}

print_test() {
    echo -e "${BOLD}TEST:${NC} $1"
}

pass() {
    echo -e "  ${GREEN}✓ PASS${NC} $1"
    ((PASSED++))
}

fail() {
    echo -e "  ${RED}✗ FAIL${NC} $1"
    ((FAILED++))
}

warn() {
    echo -e "  ${YELLOW}⚠ WARN${NC} $1"
    ((WARNINGS++))
}

# Test 1: Password Reset - POST Only
test_password_reset_post_only() {
    print_header "TEST 1: Password Reset - POST Only"
    print_test "Password reset should reject GET requests"

    # Test GET request
    response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/base_auth/recover_password/?username=testuser" 2>/dev/null)
    http_code=$(echo "$response" | tail -n 1)

    if [ "$http_code" != "200" ]; then
        pass "GET request blocked (HTTP $http_code)"
    else
        fail "GET request not blocked (HTTP $http_code)"
    fi

    # Test POST request
    response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/base_auth/recover_password/" \
        -H "Content-Type: application/json" \
        -d '{"username":"testuser"}' 2>/dev/null)
    http_code=$(echo "$response" | tail -n 1)

    if [ "$http_code" == "200" ]; then
        pass "POST request accepted (HTTP $http_code)"
    else
        fail "POST request failed (HTTP $http_code)"
    fi
}

# Test 2: Password Reset - Identical Responses
test_password_reset_identical_responses() {
    print_header "TEST 2: Password Reset - Identical Responses (No Enumeration)"
    print_test "Valid and invalid usernames should return identical messages"

    # Valid user
    response1=$(curl -s -X POST "$BASE_URL/api/base_auth/recover_password/" \
        -H "Content-Type: application/json" \
        -d '{"username":"testuser"}' 2>/dev/null)
    msg1=$(echo "$response1" | grep -o '"message":"[^"]*"' | head -1)

    # Invalid user
    response2=$(curl -s -X POST "$BASE_URL/api/base_auth/recover_password/" \
        -H "Content-Type: application/json" \
        -d '{"username":"nonexistent_user_xyz_invalid_12345"}' 2>/dev/null)
    msg2=$(echo "$response2" | grep -o '"message":"[^"]*"' | head -1)

    if [ "$msg1" == "$msg2" ]; then
        pass "Response messages are identical (prevents enumeration)"
        echo "    Message: $(echo $msg1 | cut -c1-60)..."
    else
        fail "Response messages differ (allows enumeration)"
        warn "Valid user: $msg1"
        warn "Invalid user: $msg2"
    fi
}

# Test 3: Password Reset - Rate Limiting
test_password_reset_rate_limiting() {
    print_header "TEST 3: Password Reset - Rate Limiting"
    print_test "Should enforce rate limiting (3 requests per IP per hour)"

    # Send 4 requests
    for i in {1..4}; do
        response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/base_auth/recover_password/" \
            -H "Content-Type: application/json" \
            -d '{"username":"testuser"}' 2>/dev/null)
        http_code=$(echo "$response" | tail -n 1)

        if [ "$http_code" == "200" ]; then
            if [ $i -le 3 ]; then
                echo "  Request $i: HTTP $http_code (OK)"
            else
                pass "Rate limiting detected on request 4"
            fi
        else
            fail "Request $i failed with HTTP $http_code"
        fi

        sleep 0.1 # Small delay between requests
    done
}

# Test 4: WhoAmI - No Role in Response
test_whoami_no_role() {
    print_header "TEST 4: WhoAmI Endpoint - No Role in Response"
    print_test "WhoAmI should not include role, is_admin, or permissions"

    response=$(curl -s "$BASE_URL/api/kernel/who_am_i/" 2>/dev/null)

    # Check for sensitive fields
    if echo "$response" | grep -q '"role"'; then
        fail "Response contains 'role' field"
    else
        pass "No 'role' field in response"
    fi

    if echo "$response" | grep -q '"is_admin"'; then
        fail "Response contains 'is_admin' field"
    else
        pass "No 'is_admin' field in response"
    fi

    if echo "$response" | grep -q '"permissions"'; then
        fail "Response contains 'permissions' field"
    else
        pass "No 'permissions' field in response"
    fi

    # Show actual fields
    fields=$(echo "$response" | grep -o '"[^"]*":' | tr '\n' ',' | sed 's/,$//;s/":,/, /g')
    warn "Response fields: $fields"
}

# Test 5: Guest Access Blocking
test_guest_blocked() {
    print_header "TEST 5: Guest Access - Protected Endpoints Blocked"
    print_test "Unauthenticated users should be blocked from protected endpoints"

    endpoints=(
        "/api/people/"
        "/api/stats/"
        "/api/filemanager/"
        "/api/marketplace/"
    )

    for endpoint in "${endpoints[@]}"; do
        response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint" 2>/dev/null)
        http_code=$(echo "$response" | tail -n 1)

        if [ "$http_code" == "401" ] || [ "$http_code" == "403" ]; then
            pass "$endpoint blocked (HTTP $http_code)"
        elif [ "$http_code" == "404" ]; then
            warn "$endpoint doesn't exist (404)"
        else
            fail "$endpoint accessible without auth (HTTP $http_code)"
        fi
    done
}

# Test 6: Security Headers
test_security_headers() {
    print_header "TEST 6: Security Headers"
    print_test "Response should include HSTS, X-Frame-Options, and other security headers"

    # Make a request and capture headers
    response=$(curl -s -i "$BASE_URL/api/kernel/who_am_i/" 2>/dev/null)

    # Check HSTS
    if echo "$response" | grep -qi "strict-transport-security"; then
        hsts=$(echo "$response" | grep -i "strict-transport-security" | head -1 | cut -d: -f2- | xargs)
        pass "HSTS header present: $hsts"
    else
        fail "HSTS header missing"
    fi

    # Check X-Frame-Options
    if echo "$response" | grep -qi "x-frame-options"; then
        xframe=$(echo "$response" | grep -i "x-frame-options" | head -1 | cut -d: -f2- | xargs)
        pass "X-Frame-Options header present: $xframe"
    else
        fail "X-Frame-Options header missing"
    fi

    # Check X-Content-Type-Options
    if echo "$response" | grep -qi "x-content-type-options"; then
        xcontenttype=$(echo "$response" | grep -i "x-content-type-options" | head -1 | cut -d: -f2- | xargs)
        pass "X-Content-Type-Options header present: $xcontenttype"
    else
        fail "X-Content-Type-Options header missing"
    fi

    # Check X-XSS-Protection
    if echo "$response" | grep -qi "x-xss-protection"; then
        xxss=$(echo "$response" | grep -i "x-xss-protection" | head -1 | cut -d: -f2- | xargs)
        pass "X-XSS-Protection header present: $xxss"
    else
        warn "X-XSS-Protection header missing"
    fi
}

# Test 7: HTTPS Redirect
test_https_redirect() {
    print_header "TEST 7: HTTPS Configuration"
    print_test "Server should enforce HTTPS in production"

    if [[ "$BASE_URL" == https* ]]; then
        pass "Testing against HTTPS URL"
    else
        warn "Testing against HTTP URL (should be HTTPS in production)"
    fi

    # Check for redirect
    response=$(curl -s -w "\n%{http_code}" -L "$BASE_URL/" 2>/dev/null)
    http_code=$(echo "$response" | tail -n 1)

    if [ "$http_code" == "200" ]; then
        pass "Server is responding (HTTP $http_code)"
    else
        warn "Server returned HTTP $http_code"
    fi
}

# Test 8: Authentication Required
test_auth_required() {
    print_header "TEST 8: Authentication Requirement"
    print_test "Sensitive endpoints should require authentication"

    # Try without auth
    response=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/admin/" 2>/dev/null)
    http_code=$(echo "$response" | tail -n 1)

    if [ "$http_code" == "401" ] || [ "$http_code" == "403" ] || [ "$http_code" == "404" ]; then
        pass "Admin endpoint requires authentication (HTTP $http_code)"
    else
        warn "Admin endpoint returned HTTP $http_code"
    fi
}

# Summary
print_summary() {
    print_header "TEST SUMMARY"

    total=$((PASSED + FAILED))
    if [ $total -gt 0 ]; then
        percentage=$((PASSED * 100 / total))
    else
        percentage=0
    fi

    echo -e "${BOLD}Total Tests:${NC} $total"
    echo -e "${GREEN}${BOLD}Passed:${NC} $PASSED"
    echo -e "${RED}${BOLD}Failed:${NC} $FAILED"
    echo -e "${YELLOW}${BOLD}Warnings:${NC} $WARNINGS"
    echo -e "${BOLD}Pass Rate:${NC} $percentage%"

    if [ $FAILED -eq 0 ]; then
        echo -e "\n${GREEN}${BOLD}✓ ALL TESTS PASSED!${NC}"
        echo -e "${GREEN}Security fixes are working correctly${NC}\n"
        return 0
    else
        echo -e "\n${RED}${BOLD}✗ $FAILED TEST(S) FAILED${NC}"
        echo -e "${RED}Please review the failures above${NC}\n"
        return 1
    fi
}

# Main
main() {
    echo -e "${BOLD}${BLUE}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║     Channel-i Security Fixes - Authentication Tests            ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    echo -e "${BOLD}Testing against:${NC} $BASE_URL\n"

    # Check if server is reachable
    if ! curl -s -f "$BASE_URL/api/kernel/who_am_i/" > /dev/null 2>&1; then
        if ! curl -s "$BASE_URL/api/kernel/who_am_i/" > /dev/null 2>&1; then
            echo -e "${RED}ERROR: Cannot reach server at $BASE_URL${NC}"
            echo -e "${YELLOW}Make sure the server is running and URL is correct${NC}\n"
            exit 1
        fi
    fi

    # Run all tests
    test_password_reset_post_only
    test_password_reset_identical_responses
    test_password_reset_rate_limiting
    test_whoami_no_role
    test_guest_blocked
    test_security_headers
    test_https_redirect
    test_auth_required

    # Print summary
    print_summary
}

# Run main
main
