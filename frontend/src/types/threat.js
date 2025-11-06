// Type definitions for threat intelligence data structures

export const ABUSE_CATEGORIES = {
  3: 'Fraud Orders',
  4: 'DDoS Attack',
  5: 'FTP Brute-Force',
  6: 'Ping of Death',
  7: 'Phishing',
  8: 'Fraud VoIP',
  9: 'Open Proxy',
  10: 'Web Spam',
  11: 'Email Spam',
  12: 'Blog Spam',
  13: 'VPN IP',
  14: 'Port Scan',
  15: 'Hacking',
  16: 'SQL Injection',
  17: 'Spoofing',
  18: 'Brute-Force',
  19: 'Bad Web Bot',
  20: 'Exploited Host',
  21: 'Web App Attack',
  22: 'SSH',
  23: 'IoT Targeted',
};

export const getThreatLevel = (score) => {
  if (score >= 75) return { label: 'CRITICAL', color: 'red' };
  if (score >= 50) return { label: 'HIGH', color: 'orange' };
  if (score >= 25) return { label: 'MEDIUM', color: 'yellow' };
  return { label: 'LOW', color: 'green' };
};

export const getThreatColor = (score) => {
  if (score >= 75) return '#E53E3E';
  if (score >= 50) return '#DD6B20';
  if (score >= 25) return '#D69E2E';
  return '#38A169';
};
