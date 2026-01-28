/**
 * Campaign Recipients Bulk Upload Script
 * Uses OAuth 2.0 Client Credentials Flow
 * 
 * SETUP:
 * 1. Add your client_id and client_secret below
 * 2. Add a valid campaignId in the test data
 * 3. Run main() to execute
 */

// ============================================
// CONFIGURATION
// ============================================
const CONFIG = {
  // OAuth Credentials (get from your platform team)
  CLIENT_ID: 'YOUR_CLIENT_ID_HERE',
  CLIENT_SECRET: 'YOUR_CLIENT_SECRET_HERE',
  
  // Endpoints
  TOKEN_ENDPOINT: 'https://staging.auth.curebase.com/api/v1/oauth/token',
  RECIPIENTS_ENDPOINT: 'https://staging.campaigns.walgreens.curebase.com/api/v1/recipients/bulk',
  
  // Campaign ID for test recipients
  CAMPAIGN_ID: 'YOUR_CAMPAIGN_ID_HERE',
};

// ============================================
// AUTHENTICATION
// ============================================

/**
 * Gets an access token using client credentials flow
 * @returns {string|null} Access token or null if failed
 */
function getAccessToken() {
  const payload = {
    grant_type: 'client_credentials',
    client_id: CONFIG.CLIENT_ID,
    client_secret: CONFIG.CLIENT_SECRET,
  };
  
  const options = {
    method: 'POST',
    contentType: 'application/json',
    headers: { 'Accept': 'application/json' },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true,
  };
  
  try {
    const response = UrlFetchApp.fetch(CONFIG.TOKEN_ENDPOINT, options);
    const code = response.getResponseCode();
    const body = response.getContentText();
    
    if (code === 200) {
      const data = JSON.parse(body);
      Logger.log('✓ Access token obtained');
      return data.access_token;
    } else {
      Logger.log('✗ Token request failed: ' + code);
      Logger.log('Response: ' + body);
      return null;
    }
  } catch (error) {
    Logger.log('✗ Error: ' + error.message);
    return null;
  }
}

// ============================================
// API CALLS
// ============================================

/**
 * Posts recipient data to the bulk endpoint
 * @param {Array} data - Optional custom recipient data
 * @returns {Object|null} Response data or null if failed
 */
function postRecipients(data) {
  const token = getAccessToken();
  if (!token) {
    Logger.log('Aborting: No access token');
    return null;
  }
  
  const recipients = data || getTestData();
  
  const options = {
    method: 'POST',
    contentType: 'application/json',
    headers: { 'Authorization': 'Bearer ' + token },
    payload: JSON.stringify(recipients),
    muteHttpExceptions: true,
  };
  
  try {
    const response = UrlFetchApp.fetch(CONFIG.RECIPIENTS_ENDPOINT, options);
    const code = response.getResponseCode();
    const body = response.getContentText();
    
    Logger.log('Response: ' + code);
    Logger.log(body);
    
    if (code === 201) {
      Logger.log('✓ Recipients created successfully');
      return JSON.parse(body);
    } else {
      Logger.log('✗ Request failed');
      return null;
    }
  } catch (error) {
    Logger.log('✗ Error: ' + error.message);
    return null;
  }
}

// ============================================
// TEST DATA
// ============================================

/**
 * Sample recipient data matching API schema
 * Array of {recipient, journey} objects (max 100)
 */
function getTestData() {
  return [
    {
      recipient: {
        customerId: 'test-001',
        email: 'test1@example.com',
        firstName: 'Test',
        lastName: 'User1',
        status: 'ACTIVE',
        communicationPreferences: { optIn: true }
      },
      journey: {
        campaignId: CONFIG.CAMPAIGN_ID,
        status: 'NOT_STARTED'
      }
    },
    {
      recipient: {
        customerId: 'test-002',
        email: 'test2@example.com',
        firstName: 'Test',
        lastName: 'User2',
        status: 'ACTIVE',
        communicationPreferences: { optIn: true }
      },
      journey: {
        campaignId: CONFIG.CAMPAIGN_ID,
        status: 'NOT_STARTED'
      }
    }
  ];
}

// ============================================
// ENTRY POINTS
// ============================================

/**
 * Main function - run this to upload test recipients
 */
function main() {
  Logger.log('=== Campaign Recipients Upload ===');
  Logger.log('Endpoint: ' + CONFIG.RECIPIENTS_ENDPOINT);
  Logger.log('');
  
  const result = postRecipients();
  
  if (result) {
    Logger.log('');
    Logger.log('Created ' + result.recipients.length + ' recipients');
    Logger.log('Created ' + result.journeys.length + ' journeys');
  }
  
  Logger.log('=== Done ===');
  return result;
}

/**
 * Verify configuration before running
 */
function checkConfig() {
  Logger.log('=== Configuration Check ===');
  Logger.log('Client ID: ' + (CONFIG.CLIENT_ID === 'YOUR_CLIENT_ID_HERE' ? '⚠ NOT SET' : '✓ Set'));
  Logger.log('Client Secret: ' + (CONFIG.CLIENT_SECRET === 'YOUR_CLIENT_SECRET_HERE' ? '⚠ NOT SET' : '✓ Set'));
  Logger.log('Campaign ID: ' + (CONFIG.CAMPAIGN_ID === 'YOUR_CAMPAIGN_ID_HERE' ? '⚠ NOT SET' : '✓ Set'));
  Logger.log('');
  Logger.log('Token Endpoint: ' + CONFIG.TOKEN_ENDPOINT);
  Logger.log('Recipients Endpoint: ' + CONFIG.RECIPIENTS_ENDPOINT);
}

