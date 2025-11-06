import React, { useState } from 'react';
import {
  ChakraProvider,
  Box,
  Container,
  Heading,
  Input,
  Button,
  VStack,
  HStack,
  Text,
  Spinner,
  Alert,
  AlertIcon,
  AlertDescription,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Grid,
  extendTheme,
} from '@chakra-ui/react';
import { checkIP } from './services/api';
import ThreatScore from './components/ThreatScore';
import DetectionChart from './components/DetectionChart';
import DataPanel from './components/DataPanel';
import ReportIPForm from './components/ReportIPForm';
import NewsCampaigns from './components/NewsCampaigns';
import NewsArticles from './components/NewsArticles';

// Dark mode theme configuration
const config = {
  initialColorMode: 'dark',
  useSystemColorMode: false,
};

const theme = extendTheme({
  config,
  styles: {
    global: {
      body: {
        bg: 'gray.900',
        color: 'white',
      },
    },
  },
});

function App() {
  const [ipAddress, setIPAddress] = useState('');
  const [threatData, setThreatData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!ipAddress.trim()) {
      setError('Please enter a valid IP address');
      return;
    }

    // Validate IP format
    const ipPattern = /^(\d{1,3}\.){3}\d{1,3}$/;
    if (!ipPattern.test(ipAddress.trim())) {
      setError('Invalid IP address format. Please enter a valid IPv4 address (e.g., 8.8.8.8)');
      return;
    }

    // Check for reserved/private IP ranges
    const octets = ipAddress.trim().split('.').map(Number);
    
    // Validate octet ranges
    if (octets.some(octet => octet < 0 || octet > 255)) {
      setError('Invalid IP address. Each octet must be between 0 and 255.');
      return;
    }

    // Block private/reserved ranges
    if (
      // 169.254.0.0/16 (Link-Local/AWS metadata)
      (octets[0] === 169 && octets[1] === 254) ||
      // 10.0.0.0/8 (Private)
      (octets[0] === 10) ||
      // 172.16.0.0/12 (Private)
      (octets[0] === 172 && octets[1] >= 16 && octets[1] <= 31) ||
      // 192.168.0.0/16 (Private)
      (octets[0] === 192 && octets[1] === 168) ||
      // 127.0.0.0/8 (Loopback)
      (octets[0] === 127) ||
      // 0.0.0.0/8 (Reserved)
      (octets[0] === 0) ||
      // 224.0.0.0/4 (Multicast)
      (octets[0] >= 224 && octets[0] <= 239) ||
      // 240.0.0.0/4 (Reserved)
      (octets[0] >= 240)
    ) {
      setError('Cannot analyze private, reserved, or link-local IP addresses. Please enter a public IP address.');
      return;
    }

    setLoading(true);
    setError(null);
    setThreatData(null);

    try {
      const data = await checkIP(ipAddress.trim());
      setThreatData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <ChakraProvider theme={theme}>
      <Box bg="gray.900" minH="100vh" py={8}>
        <Container maxW="container.xl">
          <VStack spacing={8} align="stretch">
            {/* Header */}
            <Box textAlign="center">
              <Heading 
                size="2xl" 
                mb={2} 
                bgGradient="linear(to-r, blue.400, cyan.400)"
                bgClip="text"
              >
                🛡️ IP Threat Aggregator
              </Heading>
              <Text color="gray.400" fontSize="lg">
                AI-Powered Multi-Source Threat Intelligence Analysis
              </Text>
              <Text color="gray.500" fontSize="sm" mt={2}>
                Powered by 8 threat intelligence sources + Google Gemini AI + News API
              </Text>
            </Box>

            {/* Search Bar */}
            <Box
              p={6}
              bg="gray.800"
              borderRadius="lg"
              shadow="2xl"
              borderWidth="1px"
              borderColor="gray.700"
            >
              <HStack spacing={4}>
                <Input
                  placeholder="Enter IP address (e.g., 8.8.8.8)"
                  size="lg"
                  value={ipAddress}
                  onChange={(e) => setIPAddress(e.target.value)}
                  onKeyPress={handleKeyPress}
                  bg="gray.900"
                  borderColor="gray.600"
                  _hover={{ borderColor: 'blue.500' }}
                  _focus={{ borderColor: 'blue.400', boxShadow: '0 0 0 1px #3182CE' }}
                  color="white"
                />
                <Button
                  colorScheme="blue"
                  size="lg"
                  onClick={handleSearch}
                  isLoading={loading}
                  loadingText="Analyzing..."
                  minW="150px"
                >
                  Analyze IP
                </Button>
              </HStack>
            </Box>

            {/* Loading State */}
            {loading && (
              <Box textAlign="center" py={12}>
                <Spinner size="xl" color="blue.500" thickness="4px" />
                <Text mt={4} fontSize="lg" color="gray.400">
                  Aggregating threat intelligence from 8 sources...
                </Text>
                <Text mt={2} fontSize="sm" color="gray.500">
                  AI analysis in progress
                </Text>
              </Box>
            )}

            {/* Error State */}
            {error && (
              <Alert status="error" borderRadius="lg" bg="red.900" borderColor="red.500" borderWidth="1px">
                <AlertIcon />
                <AlertDescription color="red.200">{error}</AlertDescription>
              </Alert>
            )}

            {/* Results */}
            {threatData && !loading && (
              <VStack spacing={6} align="stretch">
                {/* Main Threat Score - Full Width */}
                <ThreatScore
                  score={threatData.final_threat_score}
                  rationale={threatData.ai_rationale}
                />

                {/* News Campaigns - Full Width */}
                {threatData.related_campaign_news && threatData.related_campaign_news.length > 0 && (
                  <NewsCampaigns campaigns={threatData.related_campaign_news} />
                )}

                {/* News API Articles - Full Width */}
                {threatData.news_articles && threatData.news_articles.length > 0 && (
                  <NewsArticles articles={threatData.news_articles} />
                )}

                {/* Charts and Details in Grid */}
                <Grid templateColumns={{ base: '1fr', lg: 'repeat(2, 1fr)' }} gap={6}>
                  <DetectionChart virustotal={threatData.reputation.virustotal_detections} />
                  <DataPanel
                    reputation={threatData.reputation}
                    geolocation={threatData.geolocation}
                    ownership={threatData.ownership}
                  />
                </Grid>

                {/* Tabs for Additional Features */}
                <Tabs variant="enclosed" colorScheme="blue">
                  <TabList borderColor="gray.700">
                    <Tab _selected={{ bg: 'gray.800', color: 'blue.400' }} color="gray.400">Report IP</Tab>
                    <Tab _selected={{ bg: 'gray.800', color: 'blue.400' }} color="gray.400">Raw Data</Tab>
                  </TabList>

                  <TabPanels>
                    <TabPanel px={0}>
                      <ReportIPForm initialIP={threatData.ip_address} />
                    </TabPanel>
                    <TabPanel px={0}>
                      <Box
                        p={4}
                        bg="gray.900"
                        color="green.300"
                        borderRadius="md"
                        borderWidth="1px"
                        borderColor="gray.700"
                        overflowX="auto"
                        fontSize="sm"
                        fontFamily="monospace"
                      >
                        <pre>{JSON.stringify(threatData.raw_data, null, 2)}</pre>
                      </Box>
                    </TabPanel>
                  </TabPanels>
                </Tabs>
              </VStack>
            )}
          </VStack>
        </Container>
      </Box>
    </ChakraProvider>
  );
}

export default App;
