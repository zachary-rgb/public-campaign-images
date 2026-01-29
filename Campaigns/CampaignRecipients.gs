/**
 * Campaign Recipients Bulk Upload Script
 * 
 * SETUP INSTRUCTIONS:
 * 1. Replace placeholder values in the CONFIG object below
 * 2. Run testOptionsRequest() first to verify connectivity
 * 3. Run getAccessToken() to test authentication
 * 4. Run postRecipients() to send recipient data
 */

// ============================================
// CONFIGURATION - UPDATE THESE VALUES
// ============================================
const CONFIG = {
  // OAuth Settings
  TOKEN_ENDPOINT: 'https://staging.auth.curebase.com/api/v1/oauth/token',
  
  // API Settings
  RECIPIENTS_ENDPOINT: 'https://staging.campaigns.walgreens.curebase.com/api/v1/recipients/bulk',
  
  // ========================================
  // AUTHENTICATION MODE - Choose ONE:
  // ========================================
  
  // MODE 1: REFRESH TOKEN (works for ~30 days, but may be single-use)
  // Get this from the zero-auth cookie in your browser
  USE_REFRESH_TOKEN: false,  // Disabled - token was invalidated
  REFRESH_TOKEN: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL3N0YWdpbmcuYXV0aC5jdXJlYmFzZS5jb20iLCJzdWIiOiJ1c2VyfGNmMWRkY2E1LTAzNjAtNGMyYy1hODAxLTExYmQyNWM3MGNiYiIsImF6cCI6ImNhbXBhaWducz93YWxncmVlbnMiLCJvcmciOnsiaWQiOiJvcmd8MjUzY2MwNjAtMjVmNS00NzJkLThkMzktNjU4NWI1OGQ1NmJkIiwibmFtZSI6IldhbGdyZWVucyIsInNsdWciOiJ3YWxncmVlbnMiLCJkZXBsb3ltZW50R3JvdXBzIjpbImRwZ3x3YWxncmVlbnMiXX0sInR5cGUiOiJyZWZyZXNoIiwiZXhwIjoxNzY4NzY0OTM3LCJpYXQiOjE3NjYxNzI5Mzd9._vgdCfJvqOuM4ykH_JBnhg2zr4lVj8KXGd0WpDiZRgc',
  
  // MODE 2: MANUAL ACCESS TOKEN (Quick test - expires in 15 mins)
  // After logging in, get token from: DevTools → Application → Cookies → zero-auth
  // Decode base64, find "access_token" value
  USE_MANUAL_TOKEN: true,  // <-- ENABLED
  MANUAL_ACCESS_TOKEN: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL3N0YWdpbmcuYXV0aC5jdXJlYmFzZS5jb20iLCJzdWIiOiJ1c2VyfGNmMWRkY2E1LTAzNjAtNGMyYy1hODAxLTExYmQyNWM3MGNiYiIsImF6cCI6ImNhbXBhaWducz93YWxncmVlbnMiLCJvcmciOnsiaWQiOiJvcmd8MjUzY2MwNjAtMjVmNS00NzJkLThkMzktNjU4NWI1OGQ1NmJkIiwibmFtZSI6IldhbGdyZWVucyIsInNsdWciOiJ3YWxncmVlbnMiLCJkZXBsb3ltZW50R3JvdXBzIjpbImRwZ3x3YWxncmVlbnMiXX0sInR5cGUiOiJhY2Nlc3MiLCJleHAiOjE3NjYyNjE0MDAsImlhdCI6MTc2NjE3NTAwMH0.pKEvPTNJelp_HscbE2RLKynMPZ1YNDLOE099Y8MCI38',
  
  // MODE 3: CLIENT CREDENTIALS (For service accounts - requires client_id/secret)
  CLIENT_ID: 'YOUR_CLIENT_ID_HERE',
  CLIENT_SECRET: 'YOUR_CLIENT_SECRET_HERE',
};

// ============================================
// AUTHENTICATION
// ============================================

/**
 * Fetches an OAuth access token from the auth server
 * Supports: refresh_token flow, manual token, or client credentials
 * @returns {string} The access token
 */
function getAccessToken() {
  // MODE 1: Refresh token flow (recommended)
  if (CONFIG.USE_REFRESH_TOKEN && CONFIG.REFRESH_TOKEN && CONFIG.REFRESH_TOKEN !== 'PASTE_YOUR_REFRESH_TOKEN_HERE') {
    Logger.log('Using refresh token to get new access token...');
    return getAccessTokenFromRefreshToken();
  }
  
  // MODE 2: Manual token mode - for quick testing with browser-copied token
  if (CONFIG.USE_MANUAL_TOKEN) {
    if (CONFIG.MANUAL_ACCESS_TOKEN === 'PASTE_YOUR_TOKEN_HERE') {
      Logger.log('ERROR: USE_MANUAL_TOKEN is true but no token provided!');
      Logger.log('Copy token from browser Network tab → Authorization header');
      return null;
    }
    Logger.log('Using manually provided token (expires in ~15 mins from when you copied it)');
    return CONFIG.MANUAL_ACCESS_TOKEN;
  }
  
  // MODE 3: Client credentials flow - requires client_id and client_secret
  Logger.log('Using client credentials flow...');
  const payload = {
    grant_type: 'client_credentials',
    client_id: CONFIG.CLIENT_ID,
    client_secret: CONFIG.CLIENT_SECRET,
  };
  
  const options = {
    method: 'POST',
    contentType: 'application/x-www-form-urlencoded',
    payload: Object.keys(payload)
      .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(payload[key]))
      .join('&'),
    muteHttpExceptions: true,
  };
  
  try {
    const response = UrlFetchApp.fetch(CONFIG.TOKEN_ENDPOINT, options);
    const responseCode = response.getResponseCode();
    const responseBody = response.getContentText();
    
    Logger.log('Token Response Code: ' + responseCode);
    Logger.log('Token Response Body: ' + responseBody);
    
    if (responseCode === 200) {
      const tokenData = JSON.parse(responseBody);
      Logger.log('Access Token obtained successfully!');
      return tokenData.access_token;
    } else {
      Logger.log('ERROR: Failed to get access token');
      Logger.log('Response: ' + responseBody);
      return null;
    }
  } catch (error) {
    Logger.log('ERROR: ' + error.message);
    return null;
  }
}

/**
 * Uses refresh token to get a new access token
 * @returns {string} The access token
 */
function getAccessTokenFromRefreshToken() {
  const payload = {
    grant_type: 'refresh_token',
    refresh_token: CONFIG.REFRESH_TOKEN,
  };
  
  Logger.log('Sending to: ' + CONFIG.TOKEN_ENDPOINT);
  Logger.log('Payload: ' + JSON.stringify(payload, null, 2));
  
  const options = {
    method: 'POST',
    contentType: 'application/json',
    headers: {
      'Accept': 'application/json',
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true,
  };
  
  try {
    const response = UrlFetchApp.fetch(CONFIG.TOKEN_ENDPOINT, options);
    const responseCode = response.getResponseCode();
    const responseBody = response.getContentText();
    
    Logger.log('Response Code: ' + responseCode);
    Logger.log('Response: ' + responseBody);
    
    if (responseCode === 200) {
      const tokenData = JSON.parse(responseBody);
      Logger.log('✓ New access token obtained!');
      return tokenData.access_token;
    } else {
      Logger.log('');
      Logger.log('ERROR: Token refresh failed');
      return null;
    }
  } catch (error) {
    Logger.log('ERROR: ' + error.message);
    return null;
  }
}

/**
 * Debug function - test token endpoint with different formats
 */
function debugTokenEndpoint() {
  Logger.log('=== DEBUG: Testing Token Endpoint ===');
  Logger.log('');
  
  const payload = {
    grant_type: 'refresh_token',
    refresh_token: CONFIG.REFRESH_TOKEN,
  };
  
  // Test 1: JSON with Content-Type application/json
  Logger.log('--- Test 1: JSON body ---');
  try {
    const response1 = UrlFetchApp.fetch(CONFIG.TOKEN_ENDPOINT, {
      method: 'POST',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true,
    });
    Logger.log('Code: ' + response1.getResponseCode());
    Logger.log('Body: ' + response1.getContentText());
  } catch (e) {
    Logger.log('Error: ' + e.message);
  }
  
  Logger.log('');
  
  // Test 2: Form-urlencoded
  Logger.log('--- Test 2: Form-urlencoded ---');
  try {
    const response2 = UrlFetchApp.fetch(CONFIG.TOKEN_ENDPOINT, {
      method: 'POST',
      contentType: 'application/x-www-form-urlencoded',
      payload: 'grant_type=refresh_token&refresh_token=' + encodeURIComponent(CONFIG.REFRESH_TOKEN),
      muteHttpExceptions: true,
    });
    Logger.log('Code: ' + response2.getResponseCode());
    Logger.log('Body: ' + response2.getContentText());
  } catch (e) {
    Logger.log('Error: ' + e.message);
  }
  
  Logger.log('');
  
  // Test 3: Native payload object (let Apps Script handle encoding)
  Logger.log('--- Test 3: Native payload object ---');
  try {
    const response3 = UrlFetchApp.fetch(CONFIG.TOKEN_ENDPOINT, {
      method: 'POST',
      payload: payload,
      muteHttpExceptions: true,
    });
    Logger.log('Code: ' + response3.getResponseCode());
    Logger.log('Body: ' + response3.getContentText());
  } catch (e) {
    Logger.log('Error: ' + e.message);
  }
}

// ============================================
// RECIPIENTS API
// ============================================

/**
 * Test basic connectivity to the recipients endpoint with a GET request
 * (Apps Script doesn't support OPTIONS method)
 */
function testConnectivity() {
  Logger.log('Testing connectivity to: ' + CONFIG.RECIPIENTS_ENDPOINT);
  
  // First get an access token
  const accessToken = getAccessToken();
  if (!accessToken) {
    Logger.log('ERROR: Could not get access token');
    return null;
  }
  
  const options = {
    method: 'GET',
    headers: {
      'Authorization': 'Bearer ' + accessToken,
    },
    muteHttpExceptions: true,
  };
  
  try {
    const response = UrlFetchApp.fetch(CONFIG.RECIPIENTS_ENDPOINT, options);
    const responseCode = response.getResponseCode();
    const responseBody = response.getContentText();
    
    Logger.log('GET Response Code: ' + responseCode);
    Logger.log('Response: ' + responseBody.substring(0, 500)); // First 500 chars
    
    if (responseCode === 200 || responseCode === 405) {
      // 405 = Method Not Allowed, which means we reached the endpoint (it just doesn't support GET)
      Logger.log('✓ Connectivity confirmed! Endpoint is reachable.');
    }
    
    return responseCode;
  } catch (error) {
    Logger.log('Connectivity ERROR: ' + error.message);
    return null;
  }
}

/**
 * Posts recipient data to the bulk endpoint
 * @param {Array} recipientData - Array of recipient objects (optional, uses test data if not provided)
 */
function postRecipients(recipientData) {
  // Get access token first
  const accessToken = getAccessToken();
  
  if (!accessToken) {
    Logger.log('ERROR: Could not obtain access token. Aborting.');
    return null;
  }
  
  // Use provided data or fallback to test data
  const recipients = recipientData || getTestRecipientData();
  
  const options = {
    method: 'POST',
    contentType: 'application/json',
    headers: {
      'Authorization': 'Bearer ' + accessToken,
    },
    payload: JSON.stringify(recipients),
    muteHttpExceptions: true,
  };
  
  try {
    const response = UrlFetchApp.fetch(CONFIG.RECIPIENTS_ENDPOINT, options);
    const responseCode = response.getResponseCode();
    const responseBody = response.getContentText();
    
    Logger.log('POST Recipients Response Code: ' + responseCode);
    Logger.log('POST Recipients Response Body: ' + responseBody);
    
    return {
      code: responseCode,
      body: responseBody,
    };
  } catch (error) {
    Logger.log('POST ERROR: ' + error.message);
    return null;
  }
}

// ============================================
// TEST DATA
// ============================================

/**
 * Returns sample test recipient data
 * Based on API schema: Array of {recipient, journey} objects (max 100)
 * Required: recipient.customerId, journey.campaignId
 */
function getTestRecipientData() {
  return [
    {
      recipient: {
        customerId: 'test-customer-001',           // REQUIRED - external ID from your system
        email: 'test1@example.com',
        firstName: 'Test',
        lastName: 'User1',
        phone: '+15551234567',
        status: 'ACTIVE',                          // ACTIVE, UNSUBSCRIBED, or BOUNCED
        tags: ['test', 'api-import'],
        communicationPreferences: {
          optIn: true
        }
      },
      journey: {
        campaignId: 'YOUR_CAMPAIGN_ID_HERE',       // REQUIRED - get from campaigns list
        status: 'NOT_STARTED'                      // NOT_STARTED, PROCESSING, COMPLETED, etc.
      }
    },
    {
      recipient: {
        customerId: 'test-customer-002',
        email: 'test2@example.com',
        firstName: 'Test',
        lastName: 'User2',
        phone: '+15559876543',
        status: 'ACTIVE',
        communicationPreferences: {
          optIn: true
        }
      },
      journey: {
        campaignId: 'YOUR_CAMPAIGN_ID_HERE',       // Same campaign ID
        status: 'NOT_STARTED'
      }
    }
  ];
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Main entry point - runs the full flow
 */
function main() {
  Logger.log('=== Starting Campaign Recipients Upload ===');
  Logger.log('');
  
  // Step 1: Post recipients
  Logger.log('Step 1: Posting recipient data...');
  const result = postRecipients();
  Logger.log('');
  
  Logger.log('=== Complete ===');
  return result;
}

/**
 * Debug function to verify configuration
 */
function checkConfig() {
  Logger.log('=== Current Configuration ===');
  Logger.log('');
  Logger.log('--- Authentication Mode ---');
  
  if (CONFIG.USE_REFRESH_TOKEN) {
    Logger.log('Mode: REFRESH TOKEN (recommended)');
    Logger.log('Refresh Token: ' + (CONFIG.REFRESH_TOKEN ? '✓ Set' : '⚠️ NOT SET'));
    Logger.log('Token Endpoint: ' + CONFIG.TOKEN_ENDPOINT);
  } else if (CONFIG.USE_MANUAL_TOKEN) {
    Logger.log('Mode: MANUAL ACCESS TOKEN');
    Logger.log('Manual Token: ' + (CONFIG.MANUAL_ACCESS_TOKEN === 'PASTE_YOUR_TOKEN_HERE' ? '⚠️ NOT SET' : '✓ Set (expires in ~15 mins)'));
  } else {
    Logger.log('Mode: CLIENT CREDENTIALS');
    Logger.log('Token Endpoint: ' + CONFIG.TOKEN_ENDPOINT);
    Logger.log('Client ID: ' + (CONFIG.CLIENT_ID === 'YOUR_CLIENT_ID_HERE' ? '⚠️ NOT SET' : '✓ Set'));
    Logger.log('Client Secret: ' + (CONFIG.CLIENT_SECRET === 'YOUR_CLIENT_SECRET_HERE' ? '⚠️ NOT SET' : '✓ Set'));
  }
  
  Logger.log('');
  Logger.log('--- API Endpoint ---');
  Logger.log('Recipients Endpoint: ' + CONFIG.RECIPIENTS_ENDPOINT);
}

/**
 * Helper to decode and display JWT token expiry
 */
function checkTokenExpiry() {
  if (!CONFIG.REFRESH_TOKEN) {
    Logger.log('No refresh token configured');
    return;
  }
  
  try {
    // Decode JWT payload (middle part)
    const parts = CONFIG.REFRESH_TOKEN.split('.');
    const payload = JSON.parse(Utilities.newBlob(Utilities.base64Decode(parts[1])).getDataAsString());
    
    const expDate = new Date(payload.exp * 1000);
    const now = new Date();
    const daysRemaining = Math.floor((expDate - now) / (1000 * 60 * 60 * 24));
    
    Logger.log('=== Refresh Token Status ===');
    Logger.log('Expires: ' + expDate.toISOString());
    Logger.log('Days remaining: ' + daysRemaining);
    Logger.log('User: ' + payload.sub);
    Logger.log('App: ' + payload.azp);
    
    if (daysRemaining < 7) {
      Logger.log('⚠️ WARNING: Token expires soon! Get a new one from the browser.');
    } else {
      Logger.log('✓ Token is valid');
    }
  } catch (e) {
    Logger.log('Could not decode token: ' + e.message);
  }
}

