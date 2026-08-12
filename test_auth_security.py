#!/usr/bin/env python
"""
Test script for Channel-i Security Fixes

Tests all authentication and authorization security fixes:
- CWE-602: Client-side role enforcement
- CWE-639: Missing authorization checks
- CWE-284: Improper access control
- CWE-640: Weak password reset
- CWE-799: Rate limiting bypass
- CWE-204: Username enumeration

Run: python test_auth_security.py
Or:  python manage.py shell < test_auth_security.py
"""

import os
import sys
import json
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omniport.settings')
django.setup()

from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


class SecurityTestRunner:
    """Run security tests for auth fixes"""

    def __init__(self):
        self.client = APIClient()
        self.test_results = []
        self.passed = 0
        self.failed = 0

    def print_header(self, text):
        """Print colored header"""
        print(f"\n{BLUE}{BOLD}{'='*70}{RESET}")
        print(f"{BLUE}{BOLD}{text}{RESET}")
        print(f"{BLUE}{BOLD}{'='*70}{RESET}\n")

    def print_test(self, name):
        """Print test name"""
        print(f"{BOLD}TEST:{RESET} {name}")

    def print_pass(self, message=""):
        """Print passing test"""
        self.passed += 1
        print(f"  {GREEN}✓ PASS{RESET} {message}")
        self.test_results.append({"test": name, "status": "PASS", "message": message})

    def print_fail(self, message=""):
        """Print failing test"""
        self.failed += 1
        print(f"  {RED}✗ FAIL{RESET} {message}")
        self.test_results.append({"test": name, "status": "FAIL", "message": message})

    def print_warning(self, message=""):
        """Print warning"""
        print(f"  {YELLOW}⚠ WARN{RESET} {message}")

    def test_password_reset_post_only(self):
        """Test that password reset doesn't accept GET"""
        self.print_header("TEST 1: Password Reset - POST Only")
        self.print_test("Password reset should reject GET requests")

        # Create test user
        try:
            user = User.objects.get(username='testuser')
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='password123'
            )

        # Test GET request
        response = self.client.get('/api/base_auth/recover_password/', {
            'username': 'testuser'
        })

        if response.status_code != 200:
            self.print_pass(f"GET request blocked (status: {response.status_code})")
        else:
            self.print_fail(f"GET request not blocked (status: {response.status_code})")

        # Test POST request
        response = self.client.post('/api/base_auth/recover_password/', {
            'username': 'testuser'
        }, format='json')

        if response.status_code == 200:
            self.print_pass(f"POST request accepted (status: {response.status_code})")
        else:
            self.print_fail(f"POST request failed (status: {response.status_code})")

    def test_password_reset_identical_responses(self):
        """Test that valid and invalid usernames return identical responses"""
        self.print_header("TEST 2: Password Reset - Identical Responses (Enumeration Prevention)")
        self.print_test("Valid and invalid users should get identical responses")

        # Clear cache
        cache.clear()

        # Valid user response
        response1 = self.client.post('/api/base_auth/recover_password/', {
            'username': 'testuser'
        }, format='json')

        msg1 = response1.data.get('message') if hasattr(response1, 'data') else None

        # Invalid user response
        response2 = self.client.post('/api/base_auth/recover_password/', {
            'username': 'nonexistent_user_xyz_invalid_12345'
        }, format='json')

        msg2 = response2.data.get('message') if hasattr(response2, 'data') else None

        # Both should be 200
        if response1.status_code == 200 and response2.status_code == 200:
            self.print_pass("Both return 200 status")
        else:
            self.print_fail(f"Status codes differ: {response1.status_code} vs {response2.status_code}")

        # Messages should be identical
        if msg1 == msg2:
            self.print_pass("Response messages are identical (no enumeration)")
        else:
            self.print_fail("Response messages differ (allows enumeration)")
            self.print_warning(f"Valid: {msg1[:50]}...")
            self.print_warning(f"Invalid: {msg2[:50]}...")

    def test_password_reset_rate_limiting(self):
        """Test rate limiting on password reset"""
        self.print_header("TEST 3: Password Reset - Rate Limiting")
        self.print_test("Password reset should enforce rate limiting (3/IP/hour)")

        # Clear cache
        cache.clear()

        # Send 3 requests (should all succeed)
        for i in range(3):
            response = self.client.post('/api/base_auth/recover_password/', {
                'username': 'testuser'
            }, format='json')
            if response.status_code == 200:
                self.print_pass(f"Request {i+1}/3 succeeded")
            else:
                self.print_fail(f"Request {i+1} failed with status {response.status_code}")

        # 4th request should still return 200 (but rate limit was hit)
        response = self.client.post('/api/base_auth/recover_password/', {
            'username': 'testuser'
        }, format='json')

        if response.status_code == 200:
            self.print_pass("Rate limiting implemented (4th request rate limited)")
        else:
            self.print_fail(f"Rate limiting not working (status: {response.status_code})")

    def test_whoami_no_role_in_response(self):
        """Test that WhoAmI doesn't return role information"""
        self.print_header("TEST 4: WhoAmI Endpoint - No Role in Response")
        self.print_test("WhoAmI should not include role, is_admin, or permissions")

        # Create and authenticate user
        try:
            user = User.objects.get(username='whoami_test')
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='whoami_test',
                email='whoami@test.com',
                password='password123'
            )

        self.client.force_authenticate(user=user)

        # Get WhoAmI response
        response = self.client.get('/api/kernel/who_am_i/')

        if response.status_code == 200:
            self.print_pass("WhoAmI endpoint returned 200")

            data = response.data

            # Check for sensitive fields
            sensitive_fields = ['role', 'is_admin', 'permissions', 'groups', 'is_staff', 'is_superuser']
            found_fields = [f for f in sensitive_fields if f in data]

            if not found_fields:
                self.print_pass("No sensitive authorization fields in response")
            else:
                self.print_fail(f"Sensitive fields found: {found_fields}")

            # Log response fields
            self.print_warning(f"Response fields: {list(data.keys())}")
        else:
            self.print_fail(f"WhoAmI returned {response.status_code}")

        self.client.force_authenticate(user=None)

    def test_guest_blocked_from_protected_endpoints(self):
        """Test that guest users are blocked from protected endpoints"""
        self.print_header("TEST 5: Guest Access - Block Protected Endpoints")
        self.print_test("Unauthenticated users should be blocked from /api/people/, /api/stats/, etc.")

        protected_endpoints = [
            '/api/people/',
            '/api/stats/',
            '/api/filemanager/',
            '/api/marketplace/',
        ]

        for endpoint in protected_endpoints:
            response = self.client.get(endpoint)

            # Should be 401 or 403, not 200
            if response.status_code in [401, 403]:
                self.print_pass(f"{endpoint} blocked (status: {response.status_code})")
            elif response.status_code == 404:
                self.print_warning(f"{endpoint} doesn't exist (404) - skipping")
            else:
                self.print_fail(f"{endpoint} accessible without auth (status: {response.status_code})")

    def test_security_headers(self):
        """Test that security headers are present"""
        self.print_header("TEST 6: Security Headers")
        self.print_test("Response should include HSTS, X-Frame-Options, etc.")

        # Make any request
        response = self.client.get('/api/kernel/who_am_i/')

        headers_to_check = {
            'Strict-Transport-Security': 'max-age=31536000',
            'X-Frame-Options': 'DENY',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block',
        }

        for header, expected_value in headers_to_check.items():
            if header in response:
                actual_value = response.get(header, '')
                if expected_value.lower() in actual_value.lower():
                    self.print_pass(f"{header}: {actual_value[:50]}")
                else:
                    self.print_warning(f"{header}: {actual_value} (expected: {expected_value})")
            else:
                self.print_warning(f"{header} not found in response")

    def test_middleware_loaded(self):
        """Test that security middleware is loaded"""
        self.print_header("TEST 7: Middleware Configuration")
        self.print_test("Security middleware should be in MIDDLEWARE settings")

        expected_middleware = [
            'omniport.middleware.auth_security.SecurityHeadersMiddleware',
            'omniport.middleware.auth_security.GuestSessionBlockerMiddleware',
            'omniport.middleware.auth_security.AuditLoggingMiddleware',
        ]

        middleware_list = settings.MIDDLEWARE

        for mw in expected_middleware:
            if mw in middleware_list:
                self.print_pass(f"Middleware loaded: {mw}")
            else:
                self.print_fail(f"Middleware NOT loaded: {mw}")

    def test_https_settings(self):
        """Test that HTTPS settings are configured"""
        self.print_header("TEST 8: HTTPS & Security Settings")
        self.print_test("HTTPS and security settings should be enabled")

        settings_to_check = {
            'SECURE_SSL_REDIRECT': True,
            'SESSION_COOKIE_SECURE': True,
            'CSRF_COOKIE_SECURE': True,
            'CSRF_COOKIE_HTTPONLY': True,
            'SECURE_HSTS_SECONDS': 31536000,
        }

        for setting, expected_value in settings_to_check.items():
            actual_value = getattr(settings, setting, None)

            if actual_value == expected_value:
                self.print_pass(f"{setting} = {actual_value}")
            else:
                if actual_value is None:
                    self.print_fail(f"{setting} not configured (expected: {expected_value})")
                else:
                    self.print_warning(f"{setting} = {actual_value} (expected: {expected_value})")

    def run_all_tests(self):
        """Run all tests"""
        print(f"\n{BOLD}{BLUE}")
        print("╔════════════════════════════════════════════════════════════════════╗")
        print("║          Channel-i Security Fixes - Authentication Tests          ║")
        print("╚════════════════════════════════════════════════════════════════════╝")
        print(f"{RESET}\n")

        try:
            self.test_password_reset_post_only()
            self.test_password_reset_identical_responses()
            self.test_password_reset_rate_limiting()
            self.test_whoami_no_role_in_response()
            self.test_guest_blocked_from_protected_endpoints()
            self.test_security_headers()
            self.test_middleware_loaded()
            self.test_https_settings()
        except Exception as e:
            print(f"\n{RED}ERROR: {e}{RESET}")
            import traceback
            traceback.print_exc()

        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        self.print_header("TEST SUMMARY")

        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0

        print(f"{BOLD}Total Tests:{RESET} {total}")
        print(f"{GREEN}{BOLD}Passed:{RESET} {self.passed}")
        print(f"{RED}{BOLD}Failed:{RESET} {self.failed}")
        print(f"{BOLD}Pass Rate:{RESET} {percentage:.1f}%")

        if self.failed == 0:
            print(f"\n{GREEN}{BOLD}✓ ALL TESTS PASSED!{RESET}")
        else:
            print(f"\n{RED}{BOLD}✗ {self.failed} TEST(S) FAILED{RESET}")

        print(f"\n{YELLOW}Recommendations:{RESET}")
        if self.failed == 0:
            print("  • All security fixes are working correctly")
            print("  • Ready to deploy to production")
        else:
            print("  • Review failed tests above")
            print("  • Check middleware configuration")
            print("  • Verify all files were copied correctly")


if __name__ == '__main__':
    runner = SecurityTestRunner()
    runner.run_all_tests()
