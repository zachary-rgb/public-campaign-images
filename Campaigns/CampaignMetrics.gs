/**
 * Campaign Metrics Report Script
 * 
 * Pulls metrics from the Campaigns API, populates a sheet, and emails the report.
 * 
 * SETUP:
 * 1. Add client_id and client_secret
 * 2. Create an "Input" sheet with Campaign ID in B1 and Recipients in B2
 * 3. Run fetchAndEmailMetrics() from the menu or trigger
 */

// ============================================
// CONFIGURATION
// ============================================
const CONFIG = {
  // OAuth Credentials
  CLIENT_ID: 'YOUR_CLIENT_ID_HERE',
  CLIENT_SECRET: 'YOUR_CLIENT_SECRET_HERE',
  
  // Endpoints
  TOKEN_ENDPOINT: 'https://staging.auth.curebase.com/api/v1/oauth/token',
  METRICS_ENDPOINT: 'https://staging.campaigns.walgreens.curebase.com/api/v1/metrics',
  
  // Sheet Names
  INPUT_SHEET: 'Input',
  GRANULAR_SHEET: 'Granular Metrics',  // Where API data gets written
  
  // Granular Sheet Row Mapping (Notification Type + Metric → Row offset from table start)
  // These are OFFSETS from the table's data start row (after header rows)
  GRANULAR_MAPPING: {
    'email_sent': 0,
    'email_delivered': 1,
    'email_opened': 2,
    'email_clicked': 3,
    'text_sent': 4,
    'text_delivered': 5,
    'reminder_email_sent': 6,
    'reminder_email_delivered': 7,
    'reminder_email_opened': 8,
    'reminder_email_clicked': 9,
    'reminder_text_sent': 10,
    'reminder_text_delivered': 11,
  },
  
  // Column where weekly data starts (D = column 4)
  GRANULAR_DATA_START_COL: 4,
  
  // Table dimensions for multi-campaign support
  TABLE_TOTAL_ROWS: 15,        // Name row + header row + 12 metrics + blank gap row
  METRIC_ROW_COUNT: 12,        // Fixed 12 metric rows per table
  NAME_ROW_OFFSET: 0,          // Campaign name row (relative to table start)
  HEADER_ROW_OFFSET: 1,        // Column headers row (relative to table start)
  DATA_START_ROW_OFFSET: 2,    // First metric row (relative to table start)
  
  // Input Cell Locations (on Input sheet)
  // Row 1: Headers (Campaign ID | Email Recipients | Metrics Start Date | Metrics End Date)
  // Row 2+: Campaign IDs in column A, other values in row 2
  CAMPAIGN_ID_START_ROW: 2,    // First row with campaign ID
  RECIPIENTS_CELL: 'B2',       // Comma-separated emails
  START_DATE_CELL: 'C2',       // Optional
  END_DATE_CELL: 'D2',         // Optional
};

// ============================================
// MENU & TRIGGERS
// ============================================

/**
 * Creates custom menu when spreadsheet opens
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Campaign Metrics')
    .addItem('Fetch & Update Granular Sheet', 'fetchMetrics')
    .addItem('Fetch & Update Granular + Email', 'fetchAndEmailMetrics')
    .addSeparator()
    .addItem('Email Current Spreadsheet', 'emailCurrentSpreadsheet')
    .addSeparator()
    .addItem('Check Configuration', 'checkConfig')
    .addToUi();
}

// ============================================
// AUTHENTICATION
// ============================================

/**
 * Gets access token using client credentials
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
    if (response.getResponseCode() === 200) {
      return JSON.parse(response.getContentText()).access_token;
    }
    Logger.log('Token error: ' + response.getContentText());
    return null;
  } catch (e) {
    Logger.log('Auth error: ' + e.message);
    return null;
  }
}

// ============================================
// API CALLS
// ============================================

/**
 * Fetches metrics from the API for one or more campaigns
 * @param {string|string[]} campaignIds - Single campaign ID or array of IDs
 * @param {string} startDate - Optional start date
 * @param {string} endDate - Optional end date
 */
function getMetricsFromAPI(campaignIds, startDate, endDate) {
  const token = getAccessToken();
  if (!token) {
    throw new Error('Failed to get access token');
  }
  
  // Normalize to array
  const ids = Array.isArray(campaignIds) ? campaignIds : [campaignIds];
  
  // Build URL with multiple campaignId params
  let url = CONFIG.METRICS_ENDPOINT + '?limit=100';
  ids.forEach(id => {
    url += '&campaignId=' + encodeURIComponent(id);
  });
  
  if (startDate) url += '&startDate=' + encodeURIComponent(startDate);
  if (endDate) url += '&endDate=' + encodeURIComponent(endDate);
  
  Logger.log('Fetching metrics for ' + ids.length + ' campaign(s)');
  
  const options = {
    method: 'GET',
    headers: { 'Authorization': 'Bearer ' + token },
    muteHttpExceptions: true,
  };
  
  const response = UrlFetchApp.fetch(url, options);
  const code = response.getResponseCode();
  const body = response.getContentText();
  
  Logger.log('Metrics API Response: ' + code);
  
  if (code === 200) {
    return JSON.parse(body);
  } else {
    Logger.log('Error: ' + body);
    throw new Error('API returned ' + code + ': ' + body);
  }
}

/**
 * Extracts campaign name from API response (for single campaign)
 * @param {Object} data - API response data
 * @returns {string} Campaign name or empty string
 */
function getCampaignNameFromResponse(data) {
  const items = data.items || [];
  if (items.length > 0 && items[0].campaign && items[0].campaign.name) {
    return items[0].campaign.name;
  }
  return '';
}

/**
 * Groups API response items by campaign ID
 * @param {Object} data - API response data
 * @returns {Object} Map of campaignId -> { name, language, items }
 */
function groupMetricsByCampaign(data) {
  const grouped = {};
  const items = data.items || [];
  
  items.forEach(item => {
    const campId = item.campaign?._id;
    const campName = item.campaign?.name || '';
    
    if (!campId) return;
    
    if (!grouped[campId]) {
      grouped[campId] = {
        id: campId,
        name: campName,
        language: parseLanguageFromName(campName),
        items: []
      };
    }
    grouped[campId].items.push(item);
  });
  
  Logger.log('Grouped metrics into ' + Object.keys(grouped).length + ' campaign(s)');
  return grouped;
}

/**
 * Parses language from campaign name
 * Format expected: "<Sponsor><Protocol> Campaign XN (<Language>)"
 * @param {string} campaignName - Full campaign name
 * @returns {string} Extracted language or 'Unknown'
 */
function parseLanguageFromName(campaignName) {
  if (!campaignName) return 'Unknown';
  
  // Look for text in parentheses at the end of the name
  const match = campaignName.match(/\(([^)]+)\)\s*$/);
  return match ? match[1].trim() : 'Unknown';
}

// ============================================
// DATE HELPERS
// ============================================

/**
 * Gets the most recent Tuesday (including today if Tuesday)
 * @returns {Date} Last Tuesday at midnight
 */
function getLastTuesday() {
  const today = new Date();
  const dayOfWeek = today.getDay(); // 0=Sun, 1=Mon, 2=Tue, ...
  
  // Calculate days since last Tuesday
  // Tuesday = 2, so: (dayOfWeek - 2 + 7) % 7 gives days since Tuesday
  let daysSinceTuesday = (dayOfWeek - 2 + 7) % 7;
  
  // If today is Tuesday, use last week's Tuesday (to get a full week of data)
  if (daysSinceTuesday === 0) {
    daysSinceTuesday = 7;
  }
  
  const lastTuesday = new Date(today);
  lastTuesday.setDate(today.getDate() - daysSinceTuesday);
  lastTuesday.setHours(0, 0, 0, 0);
  
  return lastTuesday;
}

/**
 * Gets the Monday following the given start date (start + 6 days)
 * @param {Date} startDate - The start date (should be a Tuesday)
 * @returns {Date} Following Monday at end of day
 */
function getFollowingMonday(startDate) {
  const start = startDate instanceof Date ? startDate : new Date(startDate);
  const monday = new Date(start);
  monday.setDate(start.getDate() + 6); // Tuesday + 6 = Monday
  monday.setHours(23, 59, 59, 999);
  
  return monday;
}

/**
 * Formats a Date object to yyyy-MM-dd string
 * @param {Date|string} date - Date to format
 * @returns {string} Formatted date string
 */
function formatDateForAPI(date) {
  if (!date) return '';
  if (typeof date === 'string' && date.trim() !== '') return date;
  if (date instanceof Date) {
    return Utilities.formatDate(date, Session.getScriptTimeZone(), 'yyyy-MM-dd');
  }
  return '';
}

/**
 * Validates date range and returns validation result
 * @param {Date|string} startDate 
 * @param {Date|string} endDate 
 * @returns {Object} { valid: boolean, error: string|null, warning: string|null }
 */
function validateDateRange(startDate, endDate) {
  const result = { valid: true, error: null, warning: null };
  
  if (!startDate || !endDate) {
    return result; // No validation needed if dates are empty (will use defaults)
  }
  
  const start = startDate instanceof Date ? startDate : new Date(startDate);
  const end = endDate instanceof Date ? endDate : new Date(endDate);
  const today = new Date();
  today.setHours(23, 59, 59, 999); // End of today
  
  // Check if dates are valid
  if (isNaN(start.getTime())) {
    result.valid = false;
    result.error = 'Invalid start date format';
    return result;
  }
  
  if (isNaN(end.getTime())) {
    result.valid = false;
    result.error = 'Invalid end date format';
    return result;
  }
  
  // Check startDate > endDate
  if (start > end) {
    result.valid = false;
    result.error = 'Start date (' + formatDateForAPI(start) + ') cannot be after end date (' + formatDateForAPI(end) + ')';
    return result;
  }
  
  // Check for future dates (warning, not error - API may still accept)
  if (start > today) {
    result.warning = 'Start date is in the future. Results may be empty.';
  } else if (end > today) {
    result.warning = 'End date is in the future. Only data up to today will be included.';
  }
  
  return result;
}

// ============================================
// SHEET OPERATIONS
// ============================================

/**
 * Reads input values from the Input sheet
 * Reads multiple campaign IDs from column A (A2, A3, A4, ...)
 * Applies default dates (last Tuesday to following Monday) if blank
 * Validates date range
 */
function getInputValues() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(CONFIG.INPUT_SHEET);
  
  if (!sheet) {
    throw new Error('Input sheet not found. Create an "Input" sheet first.');
  }
  
  // Read all non-empty campaign IDs from column A (A2, A3, A4, ...)
  const lastRow = sheet.getLastRow();
  const campaignIds = [];
  for (let row = CONFIG.CAMPAIGN_ID_START_ROW; row <= lastRow; row++) {
    const id = sheet.getRange(row, 1).getValue();  // Column A
    if (id && id.toString().trim()) {
      campaignIds.push(id.toString().trim());
    }
  }
  
  Logger.log('Found ' + campaignIds.length + ' campaign ID(s): ' + campaignIds.join(', '));
  
  // Read other values from row 2
  const recipients = sheet.getRange(CONFIG.RECIPIENTS_CELL).getValue();
  let startDate = sheet.getRange(CONFIG.START_DATE_CELL).getValue();
  let endDate = sheet.getRange(CONFIG.END_DATE_CELL).getValue();
  
  // Apply defaults if dates are blank
  const startIsBlank = !startDate || startDate === '';
  const endIsBlank = !endDate || endDate === '';
  
  if (startIsBlank) {
    startDate = getLastTuesday();
    Logger.log('Using default start date (last Tuesday): ' + formatDateForAPI(startDate));
  }
  
  if (endIsBlank) {
    // If start was also blank, calculate Monday from the default Tuesday
    // If only end is blank, calculate Monday from the provided start
    const startForMonday = startIsBlank ? startDate : (startDate instanceof Date ? startDate : new Date(startDate));
    endDate = getFollowingMonday(startForMonday);
    Logger.log('Using default end date (following Monday): ' + formatDateForAPI(endDate));
  }
  
  // Validate the date range
  const validation = validateDateRange(startDate, endDate);
  
  if (!validation.valid) {
    throw new Error(validation.error);
  }
  
  // Show warning if applicable (but continue)
  if (validation.warning) {
    Logger.log('Date warning: ' + validation.warning);
  }
  
  return {
    campaignIds: campaignIds,
    recipients: recipients,
    startDate: formatDateForAPI(startDate),
    endDate: formatDateForAPI(endDate),
    dateWarning: validation.warning,
  };
}

// ============================================
// TABLE HELPERS (Multi-Campaign Support)
// ============================================

/**
 * Finds the starting row of an existing campaign table by searching for its name
 * @param {Sheet} sheet - The Granular Metrics sheet
 * @param {string} campaignName - Campaign name to find
 * @returns {number|null} Starting row of table, or null if not found
 */
function findCampaignTableRow(sheet, campaignName) {
  const lastRow = sheet.getLastRow();
  if (lastRow === 0) return null;
  
  // Search column A for the campaign name
  const searchRange = sheet.getRange(1, 1, lastRow, 1);
  const values = searchRange.getValues();
  
  for (let i = 0; i < values.length; i++) {
    if (values[i][0] && values[i][0].toString().trim() === campaignName.trim()) {
      return i + 1;  // Convert to 1-based row number
    }
  }
  
  return null;
}

/**
 * Creates a new table structure for a campaign
 * @param {Sheet} sheet - The Granular Metrics sheet
 * @param {string} campaignName - Campaign name for header
 * @param {string} language - Language label for first column
 * @param {number} startRow - Row to start the table
 * @returns {number} Starting row of the created table
 */
function createCampaignTable(sheet, campaignName, language, startRow) {
  Logger.log('Creating table for "' + campaignName + '" at row ' + startRow);
  
  // Row 0 (relative): Campaign Name
  sheet.getRange(startRow + CONFIG.NAME_ROW_OFFSET, 1).setValue(campaignName);
  
  // Row 1 (relative): Headers - Language | Notification Type | Metric
  const headerRow = startRow + CONFIG.HEADER_ROW_OFFSET;
  sheet.getRange(headerRow, 1).setValue('Language');
  sheet.getRange(headerRow, 2).setValue('Notification Type');
  sheet.getRange(headerRow, 3).setValue('Metric');
  
  // Rows 2-13 (relative): Metric rows
  const dataStartRow = startRow + CONFIG.DATA_START_ROW_OFFSET;
  
  // Email metrics (4 rows)
  sheet.getRange(dataStartRow + 0, 1).setValue(language);
  sheet.getRange(dataStartRow + 0, 2).setValue('Email');
  sheet.getRange(dataStartRow + 0, 3).setValue('Sent');
  sheet.getRange(dataStartRow + 1, 3).setValue('Delivered');
  sheet.getRange(dataStartRow + 2, 3).setValue('Opened');
  sheet.getRange(dataStartRow + 3, 3).setValue('Clicked');
  
  // Text metrics (2 rows)
  sheet.getRange(dataStartRow + 4, 2).setValue('Text');
  sheet.getRange(dataStartRow + 4, 3).setValue('Sent');
  sheet.getRange(dataStartRow + 5, 3).setValue('Delivered');
  
  // Reminder Email metrics (4 rows)
  sheet.getRange(dataStartRow + 6, 2).setValue('Reminder Email');
  sheet.getRange(dataStartRow + 6, 3).setValue('Sent');
  sheet.getRange(dataStartRow + 7, 3).setValue('Delivered');
  sheet.getRange(dataStartRow + 8, 3).setValue('Opened');
  sheet.getRange(dataStartRow + 9, 3).setValue('Clicked');
  
  // Reminder Text metrics (2 rows)
  sheet.getRange(dataStartRow + 10, 2).setValue('Reminder Text');
  sheet.getRange(dataStartRow + 10, 3).setValue('Sent');
  sheet.getRange(dataStartRow + 11, 3).setValue('Delivered');
  
  return startRow;
}

/**
 * Gets the next empty data column for a specific table
 * @param {Sheet} sheet - The Granular Metrics sheet
 * @param {number} tableStartRow - Starting row of the table
 * @returns {number} Next empty column number
 */
function getNextDataColumn(sheet, tableStartRow) {
  const headerRow = tableStartRow + CONFIG.HEADER_ROW_OFFSET;
  const startCol = CONFIG.GRANULAR_DATA_START_COL;
  const lastCol = Math.max(sheet.getLastColumn(), startCol);
  
  for (let col = startCol; col <= lastCol + 1; col++) {
    const cellValue = sheet.getRange(headerRow, col).getValue();
    if (!cellValue || cellValue === '') {
      return col;
    }
  }
  
  return lastCol + 1;
}

/**
 * Writes metrics data to a specific table
 * @param {Sheet} sheet - The Granular Metrics sheet
 * @param {number} tableStartRow - Starting row of the table
 * @param {number} column - Column to write data to
 * @param {Object} metrics - Aggregated metrics object
 * @param {string} dateRange - Date range for column header (e.g., "2025-01-13 - 2025-01-19")
 */
function writeMetricsToTable(sheet, tableStartRow, column, metrics, dateRange) {
  // Write date range header
  const headerRow = tableStartRow + CONFIG.HEADER_ROW_OFFSET;
  sheet.getRange(headerRow, column).setValue(dateRange);
  
  // Write each metric value
  const dataStartRow = tableStartRow + CONFIG.DATA_START_ROW_OFFSET;
  
  for (const [key, offset] of Object.entries(CONFIG.GRANULAR_MAPPING)) {
    const value = metrics[key] || 0;
    const row = dataStartRow + offset;
    sheet.getRange(row, column).setValue(value);
  }
  
  Logger.log('Wrote metrics to table at row ' + tableStartRow + ', column ' + column);
}

/**
 * Finds the last row used by any table in the sheet
 * @param {Sheet} sheet - The Granular Metrics sheet
 * @returns {number} Last used row, or 0 if empty
 */
function findLastTableRow(sheet) {
  const lastRow = sheet.getLastRow();
  return lastRow;
}

// ============================================
// GRANULAR SHEET POPULATION (Multi-Campaign)
// ============================================

/**
 * Populates the Granular Metrics sheet with API data for multiple campaigns
 * Creates or updates tables for each campaign
 * @param {Object} data - API response data
 * @param {string} startDate - Start date for header
 * @param {string} endDate - End date for header
 */
function populateGranularSheet(data, startDate, endDate) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(CONFIG.GRANULAR_SHEET);
  
  if (!sheet) {
    Logger.log('Granular sheet "' + CONFIG.GRANULAR_SHEET + '" not found');
    throw new Error('Granular Metrics sheet not found. Create a sheet named "' + CONFIG.GRANULAR_SHEET + '"');
  }
  
  // Group API data by campaign
  const grouped = groupMetricsByCampaign(data);
  const campaignIds = Object.keys(grouped);
  
  if (campaignIds.length === 0) {
    Logger.log('No campaign data to write');
    return;
  }
  
  // Format date range for column header
  const dateRange = startDate + ' - ' + endDate;
  
  // Process each campaign
  campaignIds.forEach((campId, index) => {
    const campaign = grouped[campId];
    Logger.log('Processing campaign: ' + campaign.name + ' (' + campaign.language + ')');
    
    // Find existing table or determine where to create new one
    let tableStartRow = findCampaignTableRow(sheet, campaign.name);
    
    if (!tableStartRow) {
      // Create new table
      const lastRow = findLastTableRow(sheet);
      tableStartRow = lastRow === 0 ? 1 : lastRow + 2;  // Add gap after last table
      createCampaignTable(sheet, campaign.name, campaign.language, tableStartRow);
    }
    
    // Find next empty column for this table
    const nextCol = getNextDataColumn(sheet, tableStartRow);
    
    // Aggregate metrics for this campaign
    const metrics = aggregateMetricsByType(campaign.items);
    
    // Write data
    writeMetricsToTable(sheet, tableStartRow, nextCol, metrics, dateRange);
  });
  
  Logger.log('Granular sheet updated for ' + campaignIds.length + ' campaign(s)');
}

/**
 * Aggregates API metrics by notification type
 * Maps API step data to granular sheet categories
 * @param {Array} items - API response items
 * @returns {Object} Aggregated metrics by type
 */
function aggregateMetricsByType(items) {
  const metrics = {
    'email_sent': 0,
    'email_delivered': 0,
    'email_opened': 0,
    'email_clicked': 0,
    'text_sent': 0,
    'text_delivered': 0,
    'reminder_email_sent': 0,
    'reminder_email_delivered': 0,
    'reminder_email_opened': 0,
    'reminder_email_clicked': 0,
    'reminder_text_sent': 0,
    'reminder_text_delivered': 0,
  };
  
  items.forEach(item => {
    const stepName = (item.step?.name || '').toLowerCase();
    const stepMethod = (item.step?.method || '').toLowerCase();
    const stats = item.stats || {};
    
    // Determine if this is a reminder
    const isReminder = stepName.includes('reminder');
    
    // Determine notification type (email vs text/sms)
    const isEmail = stepMethod === 'email' || stepMethod.includes('email');
    const isText = stepMethod === 'sms' || stepMethod === 'text' || stepMethod.includes('sms');
    
    // Build the key prefix
    let prefix = '';
    if (isReminder) {
      prefix = isEmail ? 'reminder_email_' : 'reminder_text_';
    } else {
      prefix = isEmail ? 'email_' : 'text_';
    }
    
    // Aggregate the metrics
    const sent = stats.sent?.total || 0;
    const delivered = stats.delivered?.total || 0;
    const opened = stats.opened?.total || 0;
    const clicked = stats.clicked?.total || 0;
    
    metrics[prefix + 'sent'] += sent;
    metrics[prefix + 'delivered'] += delivered;
    
    // Only email has opened/clicked
    if (isEmail || prefix.includes('email')) {
      metrics[prefix + 'opened'] += opened;
      metrics[prefix + 'clicked'] += clicked;
    }
  });
  
  Logger.log('Aggregated metrics: ' + JSON.stringify(metrics));
  return metrics;
}

// ============================================
// EMAIL (shared helpers)
// ============================================

/**
 * Gets recipients from B2 or prompts if blank
 * @returns {string[]|null} Array of emails or null if cancelled
 */
function getRecipients() {
  const ui = SpreadsheetApp.getUi();
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const inputSheet = ss.getSheetByName(CONFIG.INPUT_SHEET);
  
  // Try to read from B2
  let recipients = '';
  if (inputSheet) {
    recipients = inputSheet.getRange(CONFIG.RECIPIENTS_CELL).getValue() || '';
  }
  
  // If blank, prompt user
  if (!recipients.toString().trim()) {
    const response = ui.prompt(
      'Email Report',
      'Enter recipient email addresses (comma-separated):',
      ui.ButtonSet.OK_CANCEL
    );
    
    if (response.getSelectedButton() !== ui.Button.OK) {
      return null;  // User cancelled
    }
    recipients = response.getResponseText();
  }
  
  if (!recipients || recipients.toString().trim() === '') {
    return null;
  }
  
  return recipients.toString().split(',').map(e => e.trim()).filter(e => e);
}

/**
 * Emails the spreadsheet as XLSX to recipients
 * @param {string[]} emailList - Array of email addresses
 * @param {string} subjectSuffix - Optional suffix for subject line
 */
function sendSpreadsheetEmail(emailList, subjectSuffix) {
  if (!emailList || emailList.length === 0) {
    Logger.log('No recipients, skipping email');
    return;
  }
  
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const spreadsheetName = ss.getName();
  
  // Generate XLSX
  const url = 'https://docs.google.com/spreadsheets/d/' + ss.getId() + '/export?format=xlsx';
  const token = ScriptApp.getOAuthToken();
  const xlsxBlob = UrlFetchApp.fetch(url, {
    headers: { 'Authorization': 'Bearer ' + token }
  }).getBlob().setName(spreadsheetName + '.xlsx');
  
  // Build email
  const subject = spreadsheetName + (subjectSuffix ? ' - ' + subjectSuffix : '');
  const body = 'Please find the attached spreadsheet report.\n\n' +
    'Generated: ' + new Date().toLocaleString() + '\n\n' +
    'View online: ' + ss.getUrl();
  
  // Send to all recipients in one email
  try {
    MailApp.sendEmail({
      to: emailList.join(', '),
      subject: subject,
      body: body,
      attachments: [xlsxBlob]
    });
    Logger.log('Emailed to: ' + emailList.join(', '));
  } catch (e) {
    Logger.log('Failed to send email: ' + e.message);
    throw e;
  }
}

// ============================================
// MAIN FUNCTIONS
// ============================================

/**
 * Main function: Fetch metrics, populate Granular sheet, and email report
 */
function fetchAndEmailMetrics() {
  Logger.log('=== Starting Metrics Fetch & Email ===');
  
  try {
    // Get inputs
    const inputs = getInputValues();
    
    if (!inputs.campaignIds || inputs.campaignIds.length === 0) {
      SpreadsheetApp.getUi().alert('Please enter at least one Campaign ID in the Input sheet (column A).');
      return;
    }
    
    Logger.log('Campaign IDs: ' + inputs.campaignIds.join(', '));
    Logger.log('Date range: ' + inputs.startDate + ' to ' + inputs.endDate);
    
    // Fetch metrics for all campaigns
    Logger.log('Fetching metrics...');
    const data = getMetricsFromAPI(inputs.campaignIds, inputs.startDate, inputs.endDate);
    
    // Get campaign names for email subject
    const grouped = groupMetricsByCampaign(data);
    const campaignNames = Object.values(grouped).map(c => c.name).filter(n => n);
    const emailSubject = campaignNames.length > 0 
      ? campaignNames.join(', ') 
      : inputs.campaignIds.join(', ');
    
    Logger.log('Campaign Names: ' + (campaignNames.join(', ') || '(none found)'));
    
    // Populate Granular sheet (creates/updates tables for each campaign)
    Logger.log('Populating Granular Metrics sheet...');
    populateGranularSheet(data, inputs.startDate, inputs.endDate);
    
    // Get recipients and email
    const emailList = getRecipients();
    if (emailList) {
      Logger.log('Emailing report...');
      sendSpreadsheetEmail(emailList, emailSubject);
      SpreadsheetApp.getUi().alert(
        'Done! Metrics fetched for ' + inputs.campaignIds.length + ' campaign(s) ' +
        'and report emailed to ' + emailList.length + ' recipient(s).'
      );
    } else {
      SpreadsheetApp.getUi().alert(
        'Metrics fetched and Granular sheet updated for ' + inputs.campaignIds.length + ' campaign(s)! ' +
        'No recipients specified for email.'
      );
    }
    
  } catch (error) {
    Logger.log('Error: ' + error.message);
    SpreadsheetApp.getUi().alert('Error: ' + error.message);
  }
  
  Logger.log('=== Complete ===');
}

/**
 * Fetch metrics only (no email) - populates Granular sheet
 */
function fetchMetrics() {
  Logger.log('=== Fetching Metrics ===');
  
  try {
    const inputs = getInputValues();
    
    if (!inputs.campaignIds || inputs.campaignIds.length === 0) {
      SpreadsheetApp.getUi().alert('Please enter at least one Campaign ID in the Input sheet (column A).');
      return;
    }
    
    Logger.log('Campaign IDs: ' + inputs.campaignIds.join(', '));
    Logger.log('Date range: ' + inputs.startDate + ' to ' + inputs.endDate);
    
    const data = getMetricsFromAPI(inputs.campaignIds, inputs.startDate, inputs.endDate);
    
    // Populate Granular sheet
    populateGranularSheet(data, inputs.startDate, inputs.endDate);
    
    SpreadsheetApp.getUi().alert(
      'Metrics fetched and Granular sheet updated for ' + inputs.campaignIds.length + ' campaign(s)!'
    );
    
  } catch (error) {
    Logger.log('Error: ' + error.message);
    SpreadsheetApp.getUi().alert('Error: ' + error.message);
  }
}

/**
 * Emails the current spreadsheet as-is (no API fetch)
 */
function emailCurrentSpreadsheet() {
  const ui = SpreadsheetApp.getUi();
  
  const emailList = getRecipients();
  if (!emailList) {
    ui.alert('No recipients specified.');
    return;
  }
  
  try {
    sendSpreadsheetEmail(emailList);
    ui.alert('Spreadsheet emailed to ' + emailList.length + ' recipient(s)!');
  } catch (error) {
    Logger.log('Error: ' + error.message);
    ui.alert('Error: ' + error.message);
  }
}

/**
 * Tests the token endpoint and returns status
 * @returns {Object} { status: string, error: string|null, token: string|null }
 */
function testTokenEndpoint() {
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
    
    if (code === 200) {
      return { status: '✓ Connected (200 OK)', error: null, token: JSON.parse(response.getContentText()).access_token };
    } else if (code === 401 || code === 403) {
      return { status: '⚠ Auth Failed (' + code + ')', error: 'Invalid credentials', token: null };
    } else {
      const body = response.getContentText();
      return { status: '⚠ Error (' + code + ')', error: body.substring(0, 100), token: null };
    }
  } catch (e) {
    return { status: '❌ Connection Failed', error: e.message, token: null };
  }
}

/**
 * Tests the metrics endpoint reachability
 * @param {string} token - Access token (optional)
 * @returns {Object} { status: string, error: string|null }
 */
function testMetricsEndpoint(token) {
  const options = {
    method: 'GET',
    headers: token ? { 'Authorization': 'Bearer ' + token } : {},
    muteHttpExceptions: true,
  };
  
  try {
    const response = UrlFetchApp.fetch(CONFIG.METRICS_ENDPOINT, options);
    const code = response.getResponseCode();
    
    if (code >= 200 && code < 300) {
      return { status: '✓ Reachable (200 OK)', error: null };
    } else if (code === 400) {
      return { status: '✓ Reachable (400 - expected without campaignId)', error: null };
    } else if (code === 401) {
      return { status: '⚠ Unauthorized (401)', error: 'Token invalid or expired' };
    } else if (code === 403) {
      return { status: '⚠ Forbidden (403)', error: 'Token lacks required permissions' };
    } else if (code === 404) {
      return { status: '⚠ Not Found (404)', error: 'Check endpoint URL' };
    } else if (code >= 500) {
      return { status: '❌ Server Error (' + code + ')', error: response.getContentText().substring(0, 100) };
    } else {
      return { status: '⚠ Client Error (' + code + ')', error: response.getContentText().substring(0, 100) };
    }
  } catch (e) {
    return { status: '❌ Connection Failed', error: e.message };
  }
}

/**
 * Check configuration and test API connectivity
 */
function checkConfig() {
  const ui = SpreadsheetApp.getUi();
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  
  let msg = '=== Configuration ===\n\n';
  
  // API Credentials
  msg += '--- API Credentials ---\n';
  const hasClientId = CONFIG.CLIENT_ID !== 'YOUR_CLIENT_ID_HERE';
  const hasClientSecret = CONFIG.CLIENT_SECRET !== 'YOUR_CLIENT_SECRET_HERE';
  msg += 'Client ID: ' + (hasClientId ? '✓ Set' : '⚠ NOT SET') + '\n';
  msg += 'Client Secret: ' + (hasClientSecret ? '✓ Set' : '⚠ NOT SET') + '\n\n';
  
  // API Connection Test
  msg += '--- API Connection ---\n';
  if (hasClientId && hasClientSecret) {
    const tokenResult = testTokenEndpoint();
    msg += 'Auth Server: ' + tokenResult.status + '\n';
    if (tokenResult.error) msg += '  → ' + tokenResult.error + '\n';
    
    const metricsResult = testMetricsEndpoint(tokenResult.token);
    msg += 'Metrics Server: ' + metricsResult.status + '\n';
    if (metricsResult.error) msg += '  → ' + metricsResult.error + '\n';
  } else {
    msg += 'Auth Server: ⏭ Skipped (credentials not set)\n';
    msg += 'Metrics Server: ⏭ Skipped (no token)\n';
  }
  msg += '\n';
  
  // Sheets
  msg += '--- Required Sheets ---\n';
  const inputSheet = ss.getSheetByName(CONFIG.INPUT_SHEET);
  const granularSheet = ss.getSheetByName(CONFIG.GRANULAR_SHEET);
  msg += 'Input sheet: ' + (inputSheet ? '✓ Found' : '⚠ MISSING') + '\n';
  msg += 'Granular Metrics sheet: ' + (granularSheet ? '✓ Found' : '⚠ MISSING') + '\n\n';
  
  // Input Values
  if (inputSheet) {
    msg += '--- Input Values ---\n';
    
    // Count campaign IDs in column A
    const lastRow = inputSheet.getLastRow();
    const campaignIds = [];
    for (let row = CONFIG.CAMPAIGN_ID_START_ROW; row <= lastRow; row++) {
      const id = inputSheet.getRange(row, 1).getValue();
      if (id && id.toString().trim()) {
        campaignIds.push(id.toString().trim());
      }
    }
    
    const recipients = inputSheet.getRange(CONFIG.RECIPIENTS_CELL).getValue();
    const startDate = inputSheet.getRange(CONFIG.START_DATE_CELL).getValue();
    const endDate = inputSheet.getRange(CONFIG.END_DATE_CELL).getValue();
    
    msg += 'Campaign IDs: ' + (campaignIds.length > 0 ? '✓ ' + campaignIds.length + ' found' : '⚠ NONE') + '\n';
    if (campaignIds.length > 0) {
      campaignIds.forEach((id, i) => {
        msg += '  ' + (i + 1) + '. ' + id + '\n';
      });
    }
    msg += 'Recipients: ' + (recipients ? '✓ Set' : '(blank - will prompt)') + '\n';
    msg += 'Start Date: ' + (startDate ? '✓ ' + startDate : '(blank - defaults to last Tuesday)') + '\n';
    msg += 'End Date: ' + (endDate ? '✓ ' + endDate : '(blank - defaults to following Monday)') + '\n';
  }
  
  ui.alert('Configuration Check', msg, ui.ButtonSet.OK);
}

